import time
from datetime import datetime, timezone
from typing import Dict, Iterator, Optional

from botocore.exceptions import ClientError

from cloudsnake.sdk.aws import App


class CloudTrailWrapper(App):
    @property
    def client_name(self) -> str:
        return "cloudtrail"

    def tail_events(
        self,
        start_time_ms: int,
        lookup_attr: Optional[Dict[str, str]] = None,
        poll_interval: int = 5,
        once: bool = False,
        seen_cache_size: int = 10_000,
    ) -> Iterator[dict]:
        seen_event_ids: Dict[str, None] = {}

        current_start_time = datetime.fromtimestamp(
            start_time_ms / 1000, tz=timezone.utc
        )

        try:
            while True:
                batch_events = []
                next_token = None
                while True:
                    kwargs = {
                        "StartTime": current_start_time,
                        "MaxResults": 50,
                    }

                    if lookup_attr:
                        kwargs["LookupAttributes"] = [lookup_attr]

                    if next_token:
                        kwargs["NextToken"] = next_token

                    response = self.client.lookup_events(**kwargs)

                    batch_events.extend(response.get("Events", []))

                    next_token = response.get("NextToken")
                    if not next_token:
                        break

                batch_events.sort(key=lambda e: e["EventTime"])

                last_event_time = None
                events_yielded_count = 0

                for event in batch_events:
                    event_id = event["EventId"]

                    if event_id in seen_event_ids:
                        continue

                    seen_event_ids[event_id] = None
                    if len(seen_event_ids) > seen_cache_size:
                        seen_event_ids.pop(next(iter(seen_event_ids)))

                    yield event

                    last_event_time = event["EventTime"]
                    events_yielded_count += 1

                if last_event_time:
                    current_start_time = last_event_time

                if once:
                    return

                time.sleep(poll_interval)

        except KeyboardInterrupt:
            self.log.info("CloudTrail tail stopped by user")

        except ClientError as err:
            self.log.error(f"CloudTrail lookup failed: {err}")
            raise
