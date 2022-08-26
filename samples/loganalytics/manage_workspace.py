import os
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
    loganalytics_client = LogAnalyticsManagementClient(credentials, subscription_id,)
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}

    )

    loganalytics=loganalytics_client.workspaces.begin_create_or_update(
        GROUP_NAME,
        workspace_name,
        {"location": "eastus"}
    ).result()
    print(f"Create consumption:\n{loganalytics}\n")

    loganalytics=loganalytics_client.workspaces.list()
    print("List consumption:")
    for loganalytics_list in loganalytics:
        print(loganalytics_list)

    loganalytics=loganalytics_client.workspaces.get(
        GROUP_NAME,
        workspace_name
    )
    print(f"\nGet consumption:\n{loganalytics}\n")


    loganalytics=loganalytics_client.workspaces.begin_delete(
        GROUP_NAME,
        workspace_name
    ).result()
    print(f"Delete consumption:\n{loganalytics}\n")

    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()
