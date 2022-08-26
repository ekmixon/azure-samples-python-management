# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import ResourceManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    DISK_NAME = "disknamex"
    SNAPSHOT_NAME = "snapshotx"
    IMAGE_NAME = "imagex"


    # Create client
    # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    compute_client = ComputeManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # Create disk
    disk = compute_client.disks.begin_create_or_update(
        GROUP_NAME,
        DISK_NAME,
        {
          "location": "eastus",
          "creation_data": {
            "create_option": "Empty"
          },
          "disk_size_gb": "200"
        }
    ).result()
    print(f"Create disk:\n{disk}")

    # Create snapshot
    snapshot = compute_client.snapshots.begin_create_or_update(
        GROUP_NAME,
        SNAPSHOT_NAME,
        {
            "location": "eastus",
            "creation_data": {
                "create_option": "Copy",
                "source_uri": f"/subscriptions/{SUBSCRIPTION_ID}/resourceGroups/{GROUP_NAME}/providers/Microsoft.Compute/disks/{DISK_NAME}",
            },
        },
    ).result()

    print(f"Create snapshot:\n{snapshot}")

    # Create a virtual machine image form a snapshot
    image = compute_client.images.begin_create_or_update(
        GROUP_NAME,
        IMAGE_NAME,
        {
            "location": "eastus",
            "storage_profile": {
                "os_disk": {
                    "os_type": "Linux",
                    "snapshot": {
                        "id": f"subscriptions/{SUBSCRIPTION_ID}/resourceGroups/{GROUP_NAME}/providers/Microsoft.Compute/snapshots/{SNAPSHOT_NAME}"
                    },
                    "os_state": "Generalized",
                },
                "zone_resilient": False,
            },
            "hyper_v_generation": "V1",
        },
    ).result()

    print(f"Create image:\n{image}")

    # Get disk
    disk = compute_client.disks.get(
        GROUP_NAME,
        DISK_NAME
    )
    print(f"Get disk:\n{disk}")

    # Get snapshot
    snapshot = compute_client.snapshots.get(
        GROUP_NAME,
        SNAPSHOT_NAME
    )
    print(f"Get snapshot:\n{snapshot}")

    # Get image
    image = compute_client.images.get(
        GROUP_NAME,
        IMAGE_NAME
    )
    print(f"Get image:\n{image}")

    # Update disk
    disk = compute_client.disks.begin_update(
        GROUP_NAME,
        DISK_NAME,
        {
          "disk_size_gb": "200"
        }
    ).result()
    print(f"Update disk:\n{disk}")

    # Update snapshot
    snapshot = compute_client.snapshots.begin_update(
        GROUP_NAME,
        SNAPSHOT_NAME,
        {
            "creation_data": {
                "create_option": "Copy",
                "source_uri": f"/subscriptions/{SUBSCRIPTION_ID}/resourceGroups/{GROUP_NAME}/providers/Microsoft.Compute/disks/{DISK_NAME}",
            }
        },
    ).result()

    print(f"Update snap shot:\n{snapshot}")

    # Update image
    image = compute_client.images.begin_update(
        GROUP_NAME,
        IMAGE_NAME,
        {
          "tags": {
            "department": "HR"
          }
        }
    ).result()
    print(f"Update image:\n{image}")

    # Delete image
    compute_client.images.begin_delete(
        GROUP_NAME,
        IMAGE_NAME
    ).result()
    print("Delete image.\n")

    # Delete snapshot
    compute_client.snapshots.begin_delete(
        GROUP_NAME,
        SNAPSHOT_NAME
    ).result()
    print("Delete snap shot.\n")

    # Delete disk
    compute_client.disks.begin_delete(
        GROUP_NAME,
        DISK_NAME
    ).result()
    print("Delete disk.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()
