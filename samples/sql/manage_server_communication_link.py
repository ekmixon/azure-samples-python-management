# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.sql import SqlManagementClient
from azure.mgmt.resource import ResourceManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    PASSWORD = os.environ.get("PASSWORD", None)
    GROUP_NAME = "testgroupx"
    SERVER_COMMUNICATION_LINK = "servercommunicationlinkxxyyzz"
    SERVER = "serverxx"
    PARTNER_SERVER = "partnerserver"

    # Create client
    # # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    sql_client = SqlManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # - init depended resources -
    # Create Server
    server = sql_client.servers.begin_create_or_update(
        GROUP_NAME,
        SERVER,
        {
          "location": "eastus",
          "administrator_login": "dummylogin",
          "administrator_login_password": PASSWORD
        }
    ).result()
    print(f"Create server:\n{server}")

    # Create Server
    partner_server = sql_client.servers.begin_create_or_update(
        GROUP_NAME,
        PARTNER_SERVER,
        {
          "location": "eastus2",
          "administrator_login": "dummylogin",
          "administrator_login_password": PASSWORD
        }
    ).result()
    print(f"Create server:\n{partner_server}")
    # - end -

    # Create server communication link
    server_communication_link = sql_client.server_communication_links.begin_create_or_update(
        GROUP_NAME,
        SERVER,
        SERVER_COMMUNICATION_LINK,
        {
          "partner_server": PARTNER_SERVER
        }
    ).result()
    print(f"Create server communication link:\n{server_communication_link}")

    # Get server communication link
    server_communication_link = sql_client.server_communication_links.get(
        GROUP_NAME,
        SERVER,
        SERVER_COMMUNICATION_LINK
    )
    print(f"Get server communication link:\n{server_communication_link}")

    # Delete server communication link
    server_communication_link = sql_client.server_communication_links.delete(
        GROUP_NAME,
        SERVER,
        SERVER_COMMUNICATION_LINK
    )
    print("Delete server communication link.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()
