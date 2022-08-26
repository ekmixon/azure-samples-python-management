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
    DATABASE = "databasexxyyzz"
    SERVER = "serverxxyyzz"

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
    # - end -

    # Create database
    database = sql_client.databases.begin_create_or_update(
        GROUP_NAME,
        SERVER,
        DATABASE,
        {
          "location": "eastus",
          "read_scale": "Disabled"
        }
    ).result()
    print(f"Create database:\n{database}")

    # Get database
    database = sql_client.databases.get(
        GROUP_NAME,
        SERVER,
        DATABASE
    )
    print(f"Get database:\n{database}")

    # Update database
    database = sql_client.databases.begin_update(
        GROUP_NAME,
        SERVER,
        DATABASE,
        {
          "sku": {
            "name": "S1",
            "tier": "Standard"
          },
          "collation": "SQL_Latin1_General_CP1_CI_AS",
          "max_size_bytes": "1073741824"
        }
    ).result()
    print(f"Update database:\n{database}")

    # Delete database
    database = sql_client.databases.begin_delete(
        GROUP_NAME,
        SERVER,
        DATABASE
    ).result()
    print("Delete database.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()
