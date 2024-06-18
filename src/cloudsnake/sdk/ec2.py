import jmespath
from cloudsnake.helpers import parse_filters
from cloudsnake.sdk.aws import App
from cloudsnake.tui import Tui
from botocore.exceptions import ClientError


class EC2InstanceWrapper(App):
    """Encapsulates Amazon Elastic Compute Cloud (Amazon EC2) instance actions."""

    def __init__(self, client, instances=None, **kwargs):
        # Call the superclass __init__ method
        super().__init__(client, **kwargs)
        self.instances = instances

    def describe_ec2_instances(self):
        """
        AWS EC2 describe instances.
        :param filters: filter the output. Available filters: https://awscli.amazonaws.com/v2/documentation/api/2.0.33/reference/ec2/describe-instances.html#options
        :param query: Parse the output using json query language. Example: --query "Reservations[*].Instances[*].{Instance:InstanceId,Subnet:SubnetId}"
        :return:
        """
        if self.filters:
            parsed_filters = parse_filters(self.filters)
        else:
            parsed_filters = []

        self.log.info("Describing EC2 instances")
        try:
            paginator = self.client.get_paginator("describe_instances")

            for page in paginator.paginate(Filters=parsed_filters):
                if self.query is not None:
                    result = jmespath.search(self.query, page)
                    self.instances = result
                else:
                    self.instances = page
        except ClientError as err:
            self.log.error(
                "Couldn't register device",
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise

    def print_ec2_instances(self, output, colored) -> None:
        """
        Print the result of describe-instances operation (with filers & query) in the console
        :param output: Output mode. See available options running: cloudsnake ec2 describe-instances --help
        :return: None
        """
        self.describe_ec2_instances()
        tui = Tui()
        tui.pretty_print(self.instances, output, colored)
