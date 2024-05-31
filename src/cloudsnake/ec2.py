import logging

import jmespath
from botocore.config import Config
from cloudsnake.helpers import parse_filters
from cloudsnake.tui import Tui


class EC2:
    def __init__(self, session, *args, **kwargs):
        self.log = logging.getLogger("cloudsnake")
        self.args = args
        self.kwargs = kwargs
        self.ec2_client = self.create_ec2_client(session)

    @staticmethod
    def create_ec2_client(session):
        config = Config(retries={"max_attempts": 10, "mode": "standard"})
        return session.client("ec2", config=config)


class InstanceWrapper(EC2):
    """Encapsulates Amazon Elastic Compute Cloud (Amazon EC2) instance actions."""

    def __init__(self, session, instances=None, *args, **kwargs):
        # Inheriting the properties of parent class
        super().__init__(session, *args, **kwargs)
        self.instances = instances

    def describe_ec2_instances(self):
        """
        AWS EC2 describe instances.
        :param filters: filter the output. Available filters: https://awscli.amazonaws.com/v2/documentation/api/2.0.33/reference/ec2/describe-instances.html#options
        :param query: Parse the output using json query language. Example: --query "Reservations[*].Instances[*].{Instance:InstanceId,Subnet:SubnetId}"
        :return:
        """
        filters = self.kwargs.get("filters")
        query = self.kwargs.get("query")
        if filters:
            parsed_filters = parse_filters(filters)
        else:
            parsed_filters = []

        self.log.info("Describing EC2 instances")
        paginator = self.ec2_client.get_paginator("describe_instances")

        for page in paginator.paginate(Filters=parsed_filters):
            if query is not None:
                result = jmespath.search(query, page)
                self.instances = result
            else:
                self.instances = page

    def print_console(self) -> None:
        """
        Print the result of describe-instances operation (with filers & query) in the console
        :param output: Output mode. See available options running: cloudsnake ec2 describe-instances --help
        :return: None
        """
        self.describe_ec2_instances()
        tui = Tui(self.kwargs.get("output"))
        tui.pretty_print(self.instances)
