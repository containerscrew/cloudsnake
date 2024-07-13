import boto3
from moto import mock_aws
import pytest


@pytest.fixture(scope="function")
def rds_client(aws_credentials):
    with mock_aws():
        yield boto3.client("rds", region_name="eu-west-1")


# class TestRDSInstanceConnectWrapper:
#     @pytest.fixture(autouse=True)
#     def setup_method(self, rds_client):
#         self.rds_client = rds_client
#         self.rds_instance = self.rds_client.create_db_instance(
#             DBInstanceIdentifier="test-instance",
#             Engine="mysql",
#             AllocatedStorage=20,
#             DBInstanceClass="db.t2.micro",
#             MasterUsername="admin",
#             MasterUserPassword="password",
#             VpcSecurityGroupIds=["sg-12345678"],
#         )

#     def test_get_db_auth_token(self):
#         """Test get db auth token function"""
#         rds = RDSInstanceConnectWrapper(self.rds_client)
#         token = rds.get_db_auth_token()

#         assert token != ""
