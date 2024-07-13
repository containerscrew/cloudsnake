import jmespath
from cloudsnake.helpers import parse_filters
from cloudsnake.sdk.aws import App
from botocore.exceptions import ClientError


class EC2InstanceWrapper(App):
    """
    Wrapper class for managing EC2 instances.
    """

    def __init__(self, client="ec2", filters=None, query=None, **kwargs):
        """
        Initialize the EC2 class.

        Args:
            client (EC2Client): The EC2 client object.
            instances (list, optional): A list of EC2 instances. Defaults to None.
            filters (str, optional): Additional filters for querying instances. Defaults to "".
            query (str, optional): A query string for filtering instances. Defaults to "".
            **kwargs: Additional keyword arguments.

        """
        super().__init__(client, filters, query, **kwargs)
        self.instances = {}

    def describe_ec2_instances(self):
        """
        AWS EC2 describe instances.
        """
        if self.filters:
            parsed_filters = parse_filters(self.filters)
        else:
            parsed_filters = []

        self.log.info("Describing EC2 instances")
        try:
            paginator = self.client.get_paginator("describe_instances")

            for page in paginator.paginate(Filters=parsed_filters):
                self.instances.update(page)

            if self.query is not None:
                result = jmespath.search(self.query, self.instances)
                return result
            else:
                return self.instances
        except ClientError as err:
            self.log.error(
                "Couldn't register device",
                err.response["Error"]["Code"],
                err.response["Error"]["Message"],
            )
            raise
