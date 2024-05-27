import logging
import sys
from dataclasses import dataclass
from dacite import from_dict


@dataclass
class InstanceData:
    name: str
    instance_id: str
    instance_type: str
    platform_details: str
    private_ip_address: str
    vpc_id: str


class Instances:
    """A class to manage EC2 instance API calls"""

    def __init__(self, session):
        self.log = logging.getLogger("awstools")
        self.client = session.client("ec2")

    def _get_instance_data(self):
        all_instance_data = []
        filters = [{"Name": "instance-state-name", "Values": ["running"]}]
        paginator = self.client.get_paginator("describe_instances")
        for page in paginator.paginate(Filters=filters):
            if page["Reservations"]:
                self.log.info("Fetching EC2 instance data")
                for res in page["Reservations"]:
                    for inst in res["Instances"]:
                        self.log.debug(f"Fetching instance data for {inst}")
                        all_instance_data.append(inst)
            else:
                self.log.warning("No instances in your region. Exiting")
                sys.exit(0)

        return all_instance_data

    def get_custom_instance_data(self) -> list[InstanceData]:
        """
        From all the instance data returner in _get_instance_data, filter the necessary values you need
        :return:
        """
        filtered_ec2_data = []
        for inst in self._get_instance_data():
            # TODO pending to test that this variable name is not empty
            name = next(
                (
                    item["Value"]
                    for item in inst.get("Tags", [])
                    if item["Key"] == "Name"
                ),
                None,
            )
            #  TODO: decide what data want to retrieve the user.
            #  By the moment this is hardcoded
            data = dict(
                name=name if name else "unknown-name",
                instance_id=inst["InstanceId"],
                instance_type=inst["InstanceType"],
                platform_details=inst["PlatformDetails"],
                private_ip_address=inst["PrivateIpAddress"],
                vpc_id=inst["VpcId"],
            )
            filtered_ec2_data.append(from_dict(data_class=InstanceData, data=data))

        return filtered_ec2_data
