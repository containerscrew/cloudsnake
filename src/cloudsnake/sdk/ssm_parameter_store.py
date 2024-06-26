from botocore.exceptions import ClientError

from cloudsnake.sdk.aws import App
from cloudsnake.tui import Tui


class SSMParameterStoreWrapper(App):
    def __init__(self, client, **kwargs):
        # Call the superclass __init__ method
        super().__init__(client, **kwargs)
        self.parameters = {}

    def describe_parameters(self):
        try:
            paginator = self.client.get_paginator("describe_parameters")
            for page in paginator.paginate():
                for page in paginator.paginate():
                    self.parameters.update(page)
        except ClientError as err:
            self.log.error(
                "Couldn't register device",
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise

    3

    def print_parameters(self, output, colored) -> None:
        """
        Print the result of describe-instances operation (with filers & query) in the console
        :param output: Output mode. See available options running: cloudsnake ec2 describe-instances --help
        :return: None
        """
        tui = Tui()
        tui.pretty_print(self.parameters, output, colored)
