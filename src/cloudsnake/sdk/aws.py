import logging
from botocore.config import Config


class App:
    """
    Encapsulate some logic will be used in all the nested wrappers (EC2,SSM,VPC,ROUTE53...)
    """

    def __init__(self, client, **kwargs):
        """
        :param filters: filter the output. Available filters: https://awscli.amazonaws.com/v2/documentation/api/2.0.33/reference/ec2/describe-instances.html#options
        :param query: Parse the output using json query language. Example: --query "Reservations[*].Instances[*].{Instance:InstanceId,Subnet:SubnetId}"
        """
        self.log = logging.getLogger("cloudsnake")
        self.filters = kwargs.get("filters", None)
        self.query = kwargs.get("query", None)
        self.client = client

    @classmethod
    def with_client(cls, client_type, session, **kwargs):
        """
        Create a boto3 client from a boto3 session
        """
        # TODO this should be parametrized: max_attempts & mode
        config = Config(retries={"max_attempts": 10, "mode": "standard"})
        client = session.client(client_type, config=config)
        return cls(client, **kwargs)
