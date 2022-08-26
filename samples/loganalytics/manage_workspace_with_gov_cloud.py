import os
from msrestazure.azure_cloud import AZURE_US_GOV_CLOUD
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.loganalytics import LogAnalyticsManagementClient


def main():
    subscription_id = os.environ["AZURE_SUBSCRIPTION_ID"]
    credentials = DefaultAzureCredential()
    GROUP_NAME = "test"
    workspace_name="testWorkspace"
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=subscription_id
    )
    #
    loganalytics_client_gov = LogAnalyticsManagementClient(
        credentials,
        subscription_id,
        base_url=AZURE_US_GOV_CLOUD.endpoints.resource_manager,
        credential_scopes=[
            f"{AZURE_US_GOV_CLOUD.endpoints.resource_manager}.default"
        ],
    )

    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    loganalytics = loganalytics_client_gov.workspaces.begin_create_or_update(
        GROUP_NAME,
        workspace_name,
        {"location": "eastus"}
    ).result()
    print(f"Create consumption:\n{loganalytics}\n")

    loganalytics = loganalytics_client_gov.workspaces.list()
    print("List consumption:")
    for loganalytics_list in loganalytics:
        print(loganalytics_list)

    loganalytics = loganalytics_client_gov.workspaces.get(
        GROUP_NAME,
        workspace_name
    )
    print(f"\nGet consumption:\n{loganalytics}\n")

    loganalytics = loganalytics_client_gov.workspaces.begin_delete(
        GROUP_NAME,
        workspace_name
    ).result()
    print(f"Delete consumption:\n{loganalytics}\n")


if __name__ == "__main__":
    main()
