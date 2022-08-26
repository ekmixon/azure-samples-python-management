# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.monitor import MonitorClient
from azure.mgmt.resource import ResourceManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    ACTION_GROUP_NAME = "actiongroupx"

    # Create client
    # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    monitor_client = MonitorClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # Create action group
    action_group = monitor_client.action_groups.create_or_update(
        GROUP_NAME,
        ACTION_GROUP_NAME,
        {
          "location": "Global",
          "group_short_name": "sample",
          "enabled": True,
          "email_receivers": [
            {
              "name": "John Doe's email",
              "email_address": "johndoe@email.com",
              "use_common_alert_schema": False
            }
          ],
          "sms_receivers": [
            {
              "name": "John Doe's mobile",
              "country_code": "1",
              "phone_number": "1234567890"
            }
          ]
        }
    )
    print(f"Create action group:\n{action_group}")

    # Get action group
    action_group = monitor_client.action_groups.get(
        GROUP_NAME,
        ACTION_GROUP_NAME
    )
    print(f"Get action group:\n{action_group}")

    # Update action group
    action_group = monitor_client.action_groups.update(
        GROUP_NAME,
        ACTION_GROUP_NAME,
        {
          "tags": {
            "key1": "value1",
            "key2": "value2"
          },
          "properties": {
            "enabled": False
          }
        }
    )
    print(f"Update action group:\n{action_group}")

    # Delete action group
    monitor_client.action_groups.delete(
        GROUP_NAME,
        ACTION_GROUP_NAME
    )
    print(f"Delete action group:\n{action_group}")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()
