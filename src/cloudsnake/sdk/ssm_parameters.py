from __future__ import annotations
import logging
from typing import Optional

from botocore.exceptions import ClientError
from cloudsnake.sdk.aws import App


class SSMParameterStoreWrapper(App):
    def __init__(
        self,
        session_response_output: Optional[dict] = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.session_response_output = session_response_output
        self.parameters = []
        self.log = logging.getLogger("cloudsnake.ssm")

    @property
    def client_name(self) -> str:
        return "ssm"

    def describe_parameters(self):
        try:
            paginator = self.client.get_paginator("describe_parameters")
            self.parameters = []
            for page in paginator.paginate():
                if "Parameters" in page:
                    self.parameters.extend(page["Parameters"])
            return self.parameters

        except ClientError as err:
            self.log.error(
                "Couldn't register device",
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise

    def get_parameter_by_name(self, name: str):
        try:
            response = self.client.get_parameter(Name=name, WithDecryption=True)
            return response["Parameter"]["Value"]
        except ClientError as err:
            self.log.error(
                "Couldn't get parameter",
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
