import boto3
from moto import mock_aws
import pytest
from cloudsnake.sdk.ec2 import EC2InstanceWrapper


@pytest.fixture(scope="function")
def ec2_client(aws_credentials):
    with mock_aws():
        yield boto3.client("ec2", region_name="eu-west-1")


class TestEC2InstanceWrapper:
    @pytest.fixture(autouse=True)
    def setup_method(self, ec2_client):
        self.ec2_client = ec2_client
        self.instance = self.ec2_client.run_instances(
            ImageId="ami-1234abcd",
            MinCount=1,
            MaxCount=1,
            InstanceType="t2.micro",
        )

    @mock_aws
    def test_describe_ec2_instances(self):
        """Test the custom ec2 describe instances function mocking EC2 with moto"""
        ec2 = EC2InstanceWrapper(self.ec2_client)
        ec2.describe_ec2_instances()

        assert len(ec2.instances["Reservations"]) == 1
        assert (
            ec2.instances["Reservations"][0]["Instances"][0]["InstanceId"]
            == self.instance["Instances"][0]["InstanceId"]
        )

    @mock_aws
    def test_describe_ec2_instances_with_filters(self):
        filters = "Name=instance-type,Values=t2.micro"
        ec2 = EC2InstanceWrapper(self.ec2_client, filters=filters)
        ec2.describe_ec2_instances()

        assert (
            ec2.instances["Reservations"][0]["Instances"][0]["InstanceType"]
            == self.instance["Instances"][0]["InstanceType"]
        )


# TODO: pending to test output query
# @mock_aws
# def test_describe_ec2_instances_with_query(ec2_client):
#     query="Reservations[*].Instances[*].Tags[?Key==`Name`].Value[][]"
#     instance = ec2_client.run_instances(
#         ImageId="ami-1234abcd",
#         MinCount=1,
#         MaxCount=1,
#         InstanceType="t2.micro",
#         Tags=[
#         {
#             'Key': 'Name',
#             'Value': 'instance-test',
#         },
#     ],
#     )

#     # Instance custom EC2 model
#     ec2 = EC2InstanceWrapper(ec2_client, query=query)

#     # Initialize EC2InstanceWrapper with the mock client
#     ec2.describe_ec2_instances()

#     assert (
#         ec2.instances["Reservations"][0]["Instances"][0]["InstanceType"]
#         == instance["Instances"][0]["InstanceType"]
#     )
