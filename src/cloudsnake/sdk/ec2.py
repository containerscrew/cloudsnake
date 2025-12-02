from __future__ import annotations

import jmespath
from typing import Any, Dict, Optional

from cloudsnake.helpers import parse_filters
from cloudsnake.sdk.aws import App
from botocore.exceptions import ClientError


class EC2InstanceWrapper(App):
    def __init__(
        self,
        filters: Optional[str] = None,
        query: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(filters=filters, query=query, **kwargs)
        self.instances: Dict[str, Any] = {}

    @property
    def client_name(self) -> str:
        return "ec2"

    def describe_ec2_instances(self) -> Any:
        parsed_filters = parse_filters(self.filters) if self.filters else []

        try:
            paginator = self.client.get_paginator("describe_instances")
            for page in paginator.paginate(Filters=parsed_filters):
                for reservation in page.get("Reservations", []):
                    for instance in reservation.get("Instances", []):
                        iid = instance.get("InstanceId")
                        if iid:
                            self.instances[iid] = instance

            return (
                jmespath.search(self.query, list(self.instances.values()))
                if self.query
                else list(self.instances.values())
            )

        except ClientError as err:
            self.log.error(
                f"EC2 describe_instances failed: {err.response['Error']['Code']} - {err.response['Error']['Message']}"
            )
            raise
