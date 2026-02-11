import logging

from cloudsnake.sdk.aws import App


class ResourceGroupTaggingApiWrapper(App):
    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.log = logging.getLogger("cloudsnake.resource_groups_tagging_api")

    @property
    def client_name(self) -> str:
        return "resourcegroupstaggingapi"

    def get_resources(self):
        try:
            paginator = self.client.get_paginator("get_resources")
            resources = []
            for page in paginator.paginate():
                if "ResourceTagMappingList" in page:
                    resources.extend(page["ResourceTagMappingList"])
            return resources

        except Exception as err:
            self.log.error(
                "Couldn't get resources",
                str(err),
            )
            raise
