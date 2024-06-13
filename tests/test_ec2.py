import os
import boto3
from moto import mock_aws
import pytest
from cloudsnake.sdk.ec2 import EC2InstanceWrapper


@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


@pytest.fixture(scope="function")
def ec2_client(aws_credentials):
    with mock_aws():
        yield boto3.client("ec2", region_name="eu-west-1")


@mock_aws
def test_describe_ec2_instances(ec2_client):
    """Test the custom ec2 describe instances function mocking EC2 with moto"""
    instance = ec2_client.run_instances(
        ImageId="ami-1234abcd",
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro",
    )

    # Instance custom EC2 model
    ec2 = EC2InstanceWrapper(ec2_client)

    # Initialize EC2InstanceWrapper with the mock client
    ec2.describe_ec2_instances()

    # Check if instances are correctly described
    assert len(ec2.instances["Reservations"]) == 1
    assert (
        ec2.instances["Reservations"][0]["Instances"][0]["InstanceId"]
        == instance["Instances"][0]["InstanceId"]
    )


@mock_aws
def test_describe_ec2_instances_with_filters(ec2_client):
    filters = "Name=instance-type,Values=t2.micro"
    instance = ec2_client.run_instances(
        ImageId="ami-1234abcd",
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro",
    )
    # Instance custom EC2 model
    ec2 = EC2InstanceWrapper(ec2_client, filters=filters)

    # Initialize EC2InstanceWrapper with the mock client
    ec2.describe_ec2_instances()

    assert (
        ec2.instances["Reservations"][0]["Instances"][0]["InstanceType"]
        == instance["Instances"][0]["InstanceType"]
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
