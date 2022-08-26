# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.eventhub import EventHubManagementClient
from azure.mgmt.loganalytics import LogAnalyticsManagementClient
from azure.mgmt.monitor import MonitorClient
from azure.mgmt.logic import LogicManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    STORAGE_ACCOUNT_NAME = "storageaccountxyzxyzxx"
    NAMESPACE = "namespacex"
    EVENTHUB = "eventhub"
    AUTHORIZATION_RULE = "authorizationx"
    INSIGHT = "insightx"
    WORKSPACE_NAME = "workspacex"
    WORKFLOW_NAME = "workflow"

    # Create client
    # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    storage_client = StorageManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    eventhub_client = EventHubManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    monitor_client = MonitorClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    loganalytics_client = LogAnalyticsManagementClient(
        credentials=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    logic_client = LogicManagementClient(
        credentials=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # Create Storage
    storage_account = storage_client.storage_accounts.begin_create(
        GROUP_NAME,
        STORAGE_ACCOUNT_NAME,
        {
            "sku":{
                "name": "Standard_LRS"
            },
            "kind": "Storage",
            "location": "eastus",
            "enable_https_traffic_only": True
        }
    ).result()

    # Create eventhub authorization rule
    eventhub_client.namespaces.begin_create_or_update(
        GROUP_NAME,
        NAMESPACE,
        {
          "sku": {
            "name": "Standard",
            "tier": "Standard"
          },
          "location": "eastus",
          "tags": {
            "tag1": "value1",
            "tag2": "value2"
          }
        }
    ).result()

    eventhub_client.namespaces.create_or_update_authorization_rule(
        GROUP_NAME,
        NAMESPACE,
        AUTHORIZATION_RULE,
        {
          "rights": [
            "Listen",
            "Send",
            "Manage"
          ]
        }
    )

    eventhub_client.event_hubs.create_or_update(
        GROUP_NAME,
        NAMESPACE,
        EVENTHUB,
        {
          "message_retention_in_days": "4",
          "partition_count": "4",
          "status": "Active",
          "capture_description": {
            "enabled": True,
            "encoding": "Avro",
            "interval_in_seconds": "120",
            "size_limit_in_bytes": "10485763",
            "destination": {
              "name": "EventHubArchive.AzureBlockBlob",
              "storage_account_resource_id": storage_account.id,
              "blob_container": "container",
              "archive_name_format": "{Namespace}/{EventHub}/{PartitionId}/{Year}/{Month}/{Day}/{Hour}/{Minute}/{Second}"
            }
          }
        }
    )

    eventhub_client.event_hubs.create_or_update_authorization_rule(
        GROUP_NAME,
        NAMESPACE,
        EVENTHUB,
        AUTHORIZATION_RULE,
        {
          "rights": [
            "Listen",
            "Send",
            "Manage"
          ]
        }
    )

    # Create workspace
    workspace = loganalytics_client.workspaces.create_or_update(
        GROUP_NAME,
        WORKSPACE_NAME,
        {
          "sku": {
            "name": "PerNode"
          },
          "retention_in_days": 30,
          "location": "eastus",
          "tags": {
            "tag1": "val1"
          }
        }
    ).result()

    # Create workflow
    workflow = logic_client.workflows.create_or_update(
        GROUP_NAME,
        WORKFLOW_NAME,
        {
            "location": "eastus",
            "definition":{
                "$schema": "https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#",
                "contentVersion": "1.0.0.0",
                "parameters": {},
                "triggers": {},
                "actions": {},
                "outputs": {}
            }
        }
    )
    RESOURCE_URI = workflow.id

    # Create diagnostic setting
    diagnostic_setting = monitor_client.diagnostic_settings.create_or_update(
        RESOURCE_URI,
        INSIGHT,
        {
            "storage_account_id": f"/subscriptions/{SUBSCRIPTION_ID}/resourceGroups/{GROUP_NAME}/providers/Microsoft.Storage/storageAccounts/{STORAGE_ACCOUNT_NAME}",
            "workspace_id": workspace.id,
            "event_hub_authorization_rule_id": f"/subscriptions/{SUBSCRIPTION_ID}/resourceGroups/{GROUP_NAME}/providers/microsoft.eventhub/namespaces/{NAMESPACE}/authorizationrules/{AUTHORIZATION_RULE}",
            "event_hub_name": EVENTHUB,
            "metrics": [],
            "logs": [
                {
                    "category": "WorkflowRuntime",
                    "enabled": True,
                    "retention_policy": {"enabled": False, "days": "0"},
                }
            ],
        },
    )

    print(f"Create diagnostic setting:\n{diagnostic_setting}")

    # Get diagnostic setting
    diagnostic_setting = monitor_client.diagnostic_settings.get(
        RESOURCE_URI,
        INSIGHT
    )
    print(f"Get diagnostic setting:\n{diagnostic_setting}")

    # Delete diagnostic setting
    monitor_client.diagnostic_settings.delete(
        RESOURCE_URI,
        INSIGHT
    )
    print("Delete diagnostic setting.")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()
