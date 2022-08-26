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
    ACTIVITY_LOG_ALERT_NAME = "activitylogalertx"

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

    # Create activity log alert
    log_alert = monitor_client.activity_log_alerts.create_or_update(
        GROUP_NAME,
        ACTIVITY_LOG_ALERT_NAME,
        {
            "location": "Global",
            "scopes": [f"subscriptions/{SUBSCRIPTION_ID}"],
            "enabled": True,
            "condition": {
                "all_of": [
                    {"field": "category", "equals": "Administrative"},
                    {"field": "level", "equals": "Error"},
                ]
            },
            "actions": {"action_groups": []},
            "description": "Sample activity log alert description",
        },
    )

    print(f"Create activity log alert:\n{log_alert}")

    # Get activity log alert
    log_alert = monitor_client.activity_log_alerts.get(
        GROUP_NAME,
        ACTIVITY_LOG_ALERT_NAME
    )
    print(f"Get activity log alert:\n{log_alert}")

    # Patch acitivity log alert
    log_alert = monitor_client.activity_log_alerts.update(
        GROUP_NAME,
        ACTIVITY_LOG_ALERT_NAME,
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
    print(f"Update activity log alert:\n{log_alert}")

    # Delete activate log alert
    monitor_client.activity_log_alerts.delete(
        GROUP_NAME,
        ACTIVITY_LOG_ALERT_NAME
    )
    print("Delete activity log alert.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()
