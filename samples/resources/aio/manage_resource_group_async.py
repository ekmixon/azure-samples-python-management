# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import asyncio
import os

from azure.identity.aio import DefaultAzureCredential
from azure.mgmt.resource.resources.aio import ResourceManagementClient


async def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"

    # Create client
    # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    credential = DefaultAzureCredential()
    resource_client = ResourceManagementClient(
        credential=credential,
        subscription_id=SUBSCRIPTION_ID
    )

    # Check resource group existence
    result_check = await resource_client.resource_groups.check_existence(
        GROUP_NAME
    )
    print(f"Whether resource group exists:\n{result_check}")

    # Create resource group
    resource_group = await resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )
    print(f"Create resource group:\n{resource_group}")

    # Get resource group
    resource_group = await resource_client.resource_groups.get(
        GROUP_NAME
    )
    print(f"Get resource group:\n{resource_group}")

    # List resource group
    resource_groups = []
    async for g in resource_client.resource_groups.list():
        resource_groups.append(g)
    print(f"List resource groups:\n{resource_groups}")

    # Update resource group
    resource_group = await resource_client.resource_groups.update(
        GROUP_NAME,
        {
            "tags":{
                "tag1": "valueA",
                "tag2": "valueB"
            }
        }
    )
    print(f"Update resource group:\n{resource_group}")

    # Delete Group
    async_poller = await resource_client.resource_groups.begin_delete(
        GROUP_NAME
    )
    await async_poller.result()
    print("Delete resource group.\n")

    # [Warning] All clients and credentials need to be closed.
    # link: https://github.com/Azure/azure-sdk-for-python/issues/8990
    await resource_client.close()
    await credential.close()


if __name__ == "__main__":
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(
        main()
    )
    event_loop.close()
