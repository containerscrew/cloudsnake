import jmespath
from cloudsnake.helpers import parse_filters
from cloudsnake.tui import Tui
from cloudsnake.app_class import App


class EC2InstanceWrapper(App):
    """Encapsulates Amazon Elastic Compute Cloud (Amazon EC2) instance actions."""

    def __init__(self, session, client, instances=None, **kwargs):
        # Inheriting the properties of parent class
        super().__init__(session, client, **kwargs)
        self.instances = instances
        self.filters = self.kwargs.get("filters")
        self.query = self.kwargs.get("query")

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
        paginator = self.client.get_paginator("describe_instances")

        for page in paginator.paginate(Filters=parsed_filters):
            if self.query is not None:
                result = jmespath.search(self.query, page)
                self.instances = result
            else:
                self.instances = page

    def print_ec2_instances(self) -> None:
        """
        Print the result of describe-instances operation (with filers & query) in the console
        :param output: Output mode. See available options running: cloudsnake ec2 describe-instances --help
        :return: None
        """
        self.describe_ec2_instances()
        tui = Tui(self.kwargs.get("output"))
        tui.pretty_print(self.instances)
