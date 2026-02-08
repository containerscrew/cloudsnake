from unittest.mock import MagicMock, patch

from cloudsnake.sdk.cloudtrail import CloudTrailWrapper


def test_tail_events_sorting():
    """
    Verifies that even if the API returns events unordered or in reverse,
    the wrapper yields them sorted by time (Chronological).
    """
    # Setup Mock Session & Client
    mock_session = MagicMock()
    mock_client = mock_session.client.return_value

    # Simulated events (API usually returns newest first)
    event_late = {"EventId": "id_2", "EventTime": 2000, "EventName": "LateEvent"}
    event_early = {"EventId": "id_1", "EventTime": 1000, "EventName": "EarlyEvent"}

    mock_client.lookup_events.return_value = {
        "Events": [event_late, event_early]  # Returned unordered/reversed
    }

    wrapper = CloudTrailWrapper(session=mock_session)

    # Execute with a trick to break the infinite loop
    # Use patch on time.sleep to raise an exception and stop the test
    results = []
    with patch("time.sleep", side_effect=InterruptedError):
        try:
            # Request events
            gen = wrapper.tail_events(start_time_ms=0, poll_interval=1)
            results.append(next(gen))
            results.append(next(gen))
            next(gen)  # This call triggers sleep -> InterruptedError
        except InterruptedError:
            pass

    # Assert
    assert len(results) == 2
    # First must be the event with time 1000 (Early)
    assert results[0]["EventId"] == "id_1"
    assert results[0]["EventName"] == "EarlyEvent"
    # Second must be the event with time 2000 (Late)
    assert results[1]["EventId"] == "id_2"


def test_tail_events_deduplication():
    """
    Verifies that if the API returns the same event in two consecutive calls,
    the wrapper ignores it the second time.
    """
    mock_session = MagicMock()
    mock_client = mock_session.client.return_value

    event_a = {"EventId": "id_a", "EventTime": 1000}
    event_b = {"EventId": "id_b", "EventTime": 2000}

    mock_client.lookup_events.side_effect = [
        {"Events": [event_a]},
        {"Events": [event_b, event_a]},
    ]

    wrapper = CloudTrailWrapper(session=mock_session)

    results = []
    with patch("time.sleep", side_effect=[None, InterruptedError]):
        try:
            for event in wrapper.tail_events(start_time_ms=0):
                results.append(event)
        except InterruptedError:
            pass

    assert len(results) == 2
    assert results[0]["EventId"] == "id_a"
    assert results[1]["EventId"] == "id_b"


def test_parse_time_str_inheritance():
    """
    Verifies that CloudTrailWrapper correctly inherits _parse_time_str from App.
    """
    wrapper = CloudTrailWrapper(session=MagicMock())  # Empty mock session

    ts = wrapper._parse_time_str("1h")
    assert isinstance(ts, int)
    assert ts > 0
