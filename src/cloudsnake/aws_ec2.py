import logging
import sys
from dataclasses import dataclass

from cloudsnake.helpers import parse_filters


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

    def __init__(self, ec2_client):
        self.log = logging.getLogger("cloudsnake")
        self.ec2_client = ec2_client

    @classmethod
    def from_session(cls, session):
        ec2_client = session.client("ec2")
        return cls(ec2_client)

    def describe_ec2_instances(self, filters):
        all_instance_data = []
        if filters:
            parsed_filters = parse_filters(filters)
        else:
            parsed_filters = []
        paginator = self.ec2_client.get_paginator("describe_instances")
        for page in paginator.paginate(Filters=parsed_filters):
            if page["Reservations"]:
                self.log.info("Fetching EC2 instance data")
                for res in page["Reservations"]:
                    for inst in res["Instances"]:
                        self.log.debug(f"Fetching instance data for {inst}")
                        all_instance_data.append(inst)
            else:
                self.log.warning("No instances in your region. Exiting")
                sys.exit(0)

        print("All instances retrieved!")

        # return all_instance_data

    # def get_custom_instance_data(self) -> list[InstanceData]:
    #     """
    #     From all the instance data returner in _get_instance_data, filter the necessary values you need
    #     :return:
    #     """
    #     filtered_ec2_data = []
    #     for inst in self._get_instance_data():
    #         # TODO pending to test that this variable name is not empty
    #         name = next(
    #             (
    #                 item["Value"]
    #                 for item in inst.get("Tags", [])
    #                 if item["Key"] == "Name"
    #             ),
    #             None,
    #         )
    #         #  TODO: decide what data want to retrieve the user
    #         #  By the moment this is hardcoded
    #         data = dict(
    #             name=name if name else "unknown-name",
    #             instance_id=inst["InstanceId"],
    #             instance_type=inst["InstanceType"],
    #             platform_details=inst["PlatformDetails"],
    #             private_ip_address=inst["PrivateIpAddress"],
    #             vpc_id=inst["VpcId"],
    #         )
    #         filtered_ec2_data.append(from_dict(data_class=InstanceData, data=data))
    #
    #     return filtered_ec2_data
