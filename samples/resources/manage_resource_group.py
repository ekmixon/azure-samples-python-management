# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"

    # Create client
    # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    # Check resource group existence
    result_check = resource_client.resource_groups.check_existence(
        GROUP_NAME
    )
    print(f"Whether resource group exists:\n{result_check}")

    # Create resource group
    resource_group = resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )
    print(f"Create resource group:\n{resource_group}")

    # Get resource group
    resource_group = resource_client.resource_groups.get(
        GROUP_NAME
    )
    print(f"Get resource group:\n{resource_group}")

    # Update resource group
    resource_group = resource_client.resource_groups.update(
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
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()
    print("Delete resource group.\n")


if __name__ == "__main__":
    main()
