from __future__ import annotations
import re
import time
import jmespath
from typing import Any, Dict, Optional, Iterator
from rich.text import Text

from cloudsnake.console import console
from cloudsnake.sdk.aws import App
from botocore.exceptions import ClientError


class CloudWatchLogsWrapper(App):
    def __init__(
        self,
        filters: Optional[str] = None,
        query: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(filters=filters, query=query, **kwargs)
        self.log_groups: Dict[str, Any] = {}

    @property
    def client_name(self) -> str:
        return "logs"

    def list_log_groups(self) -> Any:
        self.log_groups = {}
        try:
            paginator = self.client.get_paginator("describe_log_groups")

            pagination_args = {}

            if self.filters:
                pagination_args["logGroupNamePrefix"] = self.filters

            for page in paginator.paginate(**pagination_args):
                for group in page.get("logGroups", []):
                    name = group.get("logGroupName")
                    if name:
                        self.log_groups[name] = group

            result = list(self.log_groups.values())

            return jmespath.search(self.query, result) if self.query else result

        except ClientError as err:
            self.log.error(
                f"CloudWatch Logs describe_log_groups failed: "
                f"{err.response['Error']['Code']} - "
                f"{err.response['Error']['Message']}"
            )
            raise

    def tail_log_group_live(
        self,
        log_group_arn: str,
        filter_pattern: Optional[str] = None,
    ) -> Iterator[dict]:
        """
        Live tail a CloudWatch log group using start_live_tail (push-based).
        """
        try:
            kwargs = {
                "logGroupIdentifiers": [log_group_arn],
            }

            if filter_pattern:
                kwargs["logEventFilterPattern"] = filter_pattern

            response = self.client.start_live_tail(**kwargs)
            stream = response["responseStream"]

            for event in stream:
                if "sessionUpdate" in event:
                    for log_event in event["sessionUpdate"]["sessionResults"]:
                        yield log_event

        except ClientError as err:
            self.log.error(
                f"CloudWatch Logs start_live_tail failed: "
                f"{err.response['Error']['Code']} - "
                f"{err.response['Error']['Message']}"
            )
            raise

    def _parse_time_str(self, time_str: str) -> int:
        """
        Parses a time string (e.g., '1h', '2d', '30m') into a Unix timestamp in milliseconds.
        """
        now_ms = int(time.time() * 1000)

        # Clean string: remove "ago" or spaces if present (e.g. "1h ago" -> "1h")
        clean_str = time_str.lower().replace("ago", "").strip()

        if not clean_str:
            return 0

        # Extract unit and value
        try:
            unit = clean_str[-1]
            # Handle cases where user might type just "100" (assume minutes or handle error)
            if unit.isdigit():
                value = int(clean_str)
                unit = "m"  # Default to minutes if no unit provided
            else:
                value = int(clean_str[:-1])
        except ValueError:
            self.log.warning(f"Could not parse time '{time_str}', defaulting to 1h ago")
            value = 1
            unit = "h"

        multiplier = 1000  # Seconds
        if unit == "m":  # Minutes
            multiplier *= 60
        elif unit == "h":  # Hours
            multiplier *= 3600
        elif unit == "d":  # Days
            multiplier *= 86400
        elif unit == "w":  # Weeks
            multiplier *= 604800

        delta_ms = value * multiplier
        return now_ms - delta_ms

    def get_historical_logs(
        self,
        log_group_arn: str,
        since: str,
        end: Optional[str] = None,
        filter_pattern: Optional[str] = None,
    ) -> Iterator[dict]:
        """
        Fetches historical logs using filter_log_events with pagination.
        """
        parts = log_group_arn.split(":")

        if "log-group" in parts:
            idx = parts.index("log-group")
            if idx + 1 < len(parts):
                log_group_name = parts[idx + 1]
            else:
                log_group_name = log_group_arn
        else:
            log_group_name = parts[-1]

        if log_group_name.endswith("*"):
            log_group_name = log_group_name[:-1]
            if log_group_name.endswith(":"):
                log_group_name = log_group_name[:-1]

        start_time_ms = self._parse_time_str(since)
        end_time_ms = self._parse_time_str(end) if end else int(time.time() * 1000)

        self.log.debug(
            f"Fetching logs for {log_group_name} from {start_time_ms} to {end_time_ms}"
        )
        paginator = self.client.get_paginator("filter_log_events")

        kwargs = {
            "logGroupName": log_group_name,
            "startTime": start_time_ms,
            "endTime": end_time_ms,
            "interleaved": True,
        }

        if filter_pattern:
            kwargs["filterPattern"] = filter_pattern

        try:
            for page in paginator.paginate(**kwargs):
                for event in page.get("events", []):
                    yield event

        except ClientError as err:
            self.log.error(
                f"CloudWatch Logs filter_log_events failed: "
                f"{err.response['Error']['Code']} - "
                f"{err.response['Error']['Message']}"
            )
            raise


def print_colored_log(event: dict, highlight_term: str | None = None) -> None:
    stream = event.get("logStreamName", "unknown-stream")
    message = event.get("message", "").rstrip()
    timestamp = event.get("timestamp", 0)

    time_str = time.strftime("%H:%M:%S", time.localtime(timestamp / 1000))

    line = Text()
    line.append(f"[{time_str}] ", style="yellow")
    line.append(f"[{stream}] ", style="cyan")

    if highlight_term:
        pattern = re.compile(re.escape(highlight_term), re.IGNORECASE)
        last = 0
        for match in pattern.finditer(message):
            line.append(message[last : match.start()])
            line.append(match.group(), style="bold red on white")
            last = match.end()
        line.append(message[last:])
    else:
        line.append(message)

    console.print(line)
