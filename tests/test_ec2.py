import boto3
from moto import mock_aws
import pytest
from cloudsnake.sdk.ec2 import EC2InstanceWrapper


@pytest.fixture
def ec2_boto():
    """Create an EC2 boto3 client and return the client object"""
    ec2 = boto3.client("ec2", region_name="eu-west-1")
    return ec2


@mock_aws
def test_describe_ec2_instances(ec2_boto):
    """Test the custom ec2 describe instances function mocking EC2 with moto"""
    instance = ec2_boto.run_instances(
        ImageId="ami-1234abcd",
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro",
    )

    # Instance custom EC2 model
    ec2 = EC2InstanceWrapper(ec2_boto)

    # Initialize EC2InstanceWrapper with the mock client
    ec2.describe_ec2_instances()

    # Check if instances are correctly described
    assert len(ec2.instances["Reservations"]) == 1
    assert (
        ec2.instances["Reservations"][0]["Instances"][0]["InstanceId"]
        == instance["Instances"][0]["InstanceId"]
    )


# TODO Test passing query output
