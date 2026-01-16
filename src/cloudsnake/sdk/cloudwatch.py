from __future__ import annotations

import re
import time

import jmespath
from typing import Any, Dict, Optional, Iterator

from rich.console import Console
from rich.text import Text

from cloudsnake.sdk.aws import App
from botocore.exceptions import ClientError

console = Console()


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

    # TODO: implement get_historical_logs
    def get_historical_logs(self):
        pass


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
