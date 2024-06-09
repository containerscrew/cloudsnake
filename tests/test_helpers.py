from datetime import datetime
import pytest
from cloudsnake.helpers import parse_filters, serialize_datetime


"""Testing function parse_filters"""


def test_single_filter():
    filters = "Name=instance-state-name,Values=running"
    expected_output = [{"Name": "instance-state-name", "Values": ["running"]}]
    assert parse_filters(filters) == expected_output


def test_multiple_values():
    filters = "Name=instance-state-name,Values=running,Values=stopped"
    expected_output = [
        {"Name": "instance-state-name", "Values": ["running", "stopped"]}
    ]
    assert parse_filters(filters) == expected_output


def test_no_values():
    filters = "Name=instance-state-name"
    expected_output = [{"Name": "instance-state-name", "Values": []}]
    assert parse_filters(filters) == expected_output


def test_invalid_format():
    filters = "Name=instance-state-name,Value=running"
    with pytest.raises(ValueError):
        parse_filters(filters)


"""Testing function serialize_datetime"""


def test_serialize_datetime():
    # Test para asegurarse de que una instancia de datetime se serializa correctamente.
    dt = datetime(2024, 6, 8, 12, 0, 0)
    result = serialize_datetime(dt)
    assert result == "2024-06-08T12:00:00"


def test_serialize_non_datetime():
    # Test para asegurarse de que un objeto que no es datetime lanza un TypeError.
    with pytest.raises(TypeError, match="Type not serializable"):
        serialize_datetime("2024-06-08T12:00:00")
