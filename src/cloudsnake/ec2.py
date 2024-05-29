import logging
from dataclasses import dataclass
import jmespath

from cloudsnake.helpers import parse_filters
from cloudsnake.tui import Tui


@dataclass
class InstanceData:
    name: str
    instance_id: str
    instance_type: str
    platform_details: str
    private_ip_address: str
    vpc_id: str


class InstanceWrapper:
    """Encapsulates Amazon Elastic Compute Cloud (Amazon EC2) instance actions."""

    def __init__(self, ec2_client, instances=None):
        self.log = logging.getLogger("cloudsnake")
        self.ec2_client = ec2_client
        self.instances = instances

    @classmethod
    def from_session(cls, session):
        ec2_client = session.client("ec2")
        return cls(ec2_client)

    def describe_ec2_instances(self, filters, query):
        """
        AWS EC2 describe instances.
        :param filters: filter the output. Available filters: https://awscli.amazonaws.com/v2/documentation/api/2.0.33/reference/ec2/describe-instances.html#options
        :param query: Parse the output using json query language. Example: --query "Reservations[*].Instances[*].{Instance:InstanceId,Subnet:SubnetId}"
        :return:
        """
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

    def print_console(self, output) -> None:
        """
        Print the result of describe-instances operation (with filers & query) in the console
        :param output: Output mode. See available options running: cloudsnake ec2 describe-instances --help
        :return: None
        """
        tui = Tui(output)
        tui.pretty_print(self.instances)
