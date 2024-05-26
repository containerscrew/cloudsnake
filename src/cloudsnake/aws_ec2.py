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


class EC2Data:
    def __init__(self, ec2_client, logger):
        self.client = ec2_client
        self.log = logger

    def get_instance_data(self):
        """
        Pending to add doc
        :return:
        """
        instance_data = []
        filters = [{"Name": "instance-state-name", "Values": ["running"]}]

        paginator = self.client.get_paginator("describe_instances")
        for page in paginator.paginate(Filters=filters):
            if page["Reservations"]:
                for res in page["Reservations"]:
                    for inst in res["Instances"]:
                        instance_data.append(inst)
            else:
                self.log.info("No instances in your region")

        return instance_data

    def filter_ec2_data(self) -> list[InstanceData]:
        """
        Pending to add doc
        :return:
        """
        filtered_ec2_data = []
        for inst in self.get_instance_data():
            name = next(
                (
                    item["Value"]
                    for item in inst.get("Tags", [])
                    if item["Key"] == "Name"
                ),
                None,
            )
            data = dict(
                name=name,
                instance_id=inst["InstanceId"],
                instance_type=inst["InstanceType"],
                platform_details=inst["PlatformDetails"],
                private_ip_address=inst["PrivateIpAddress"],
                vpc_id=inst["VpcId"],
            )
            filtered_ec2_data.append(from_dict(data_class=InstanceData, data=data))

        return filtered_ec2_data
