# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.redis import RedisManagementClient
from azure.mgmt.resource import ResourceManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupxy"
    REDIS = "redisxxyyzzz"
    NETWORK_NAME = "networknamexx"
    SUBNET_NAME = "subnetnamexx"

    # Create client
    # # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    redis_client = RedisManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    network_client = NetworkManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # - init depended resources -
    # Create virtual network
    network_client.virtual_networks.begin_create_or_update(
        GROUP_NAME,
        NETWORK_NAME,
        {
            'location': "eastus",
            'address_space': {
                'address_prefixes': ['10.0.0.0/16']
            }
        }
    ).result()

    subnet = network_client.subnets.begin_create_or_update(
        GROUP_NAME,
        NETWORK_NAME,
        SUBNET_NAME,
        {'address_prefix': '10.0.0.0/24'}
    ).result()

    # Create redis
    redis = redis_client.redis.begin_create(
        GROUP_NAME,
        REDIS,
        {
            "location": "eastus",
            "zones": ["1"],
            "sku": {"name": "Premium", "family": "P", "capacity": "1"},
            "enable_non_ssl_port": True,
            "shard_count": "2",
            "redis_configuration": {"maxmemory-policy": "allkeys-lru"},
            "subnet_id": f"/subscriptions/{SUBSCRIPTION_ID}/resourceGroups/{GROUP_NAME}/providers/Microsoft.Network/virtualNetworks/{NETWORK_NAME}/subnets/{SUBNET_NAME}",
            "static_ip": "10.0.0.5",
            "minimum_tls_version": "1.2",
        },
    ).result()

    print(f"Create redis:\n{redis}")
    # - end -

    # Create patch schedule
    patch_schedule = redis_client.patch_schedules.create_or_update(
        GROUP_NAME,
        REDIS,
        "default",
        {
          "schedule_entries": [
            {
              "day_of_week": "Monday",
              "start_hour_utc": "12",
              "maintenance_window": "PT5H"
            },
            {
              "day_of_week": "Tuesday",
              "start_hour_utc": "12"
            }
          ]
        }
    )
    print(f"Create patch schedule:\n{patch_schedule}")

    # Get patch schedule
    patch_schedule = redis_client.patch_schedules.get(
        GROUP_NAME,
        REDIS,
        "default"
    )
    print(f"Get patch schedule:\n{patch_schedule}")

    # Delete patch schedule
    patch_schedule = redis_client.patch_schedules.delete(
        GROUP_NAME,
        REDIS,
        "default"
    )
    print("Delete patch schedule.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()
