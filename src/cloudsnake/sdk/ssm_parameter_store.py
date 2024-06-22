import logging
from botocore.exceptions import ClientError
from botocore.config import Config

from cloudsnake.sdk.aws import App

class SSMParameterStoreWrapper(App):
    def __init__(self, client, **kwargs):
        # Call the superclass __init__ method
        super().__init__(client, **kwargs)
        self.parameter_response = []
        self.parameter_response = []

    def describe_parameters(self):
        try:
            paginator = self.client.get_paginator("describe_parameters")
            for page in paginator.paginate():
                self.parameter_response.append(page)
            print(self.parameter_response)
        except ClientError as err:
            self.log.error(
                "Couldn't register device",
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
    
