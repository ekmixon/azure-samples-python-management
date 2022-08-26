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
    JOB = "jobxxyyzz"
    SERVER = "serverxxyz"
    DATABASE = "databasexxyz"
    JOB_AGENT = "jobagentxx"
    CREDENTIAL = "credentialxx"
    JOB_STEP = "jobstepxx"
    TARGET_GROUP = "targetgroupxx"
    JOB_EXECUTION_ID = "622ffff7-c4be-4c62-8098-3867c5db6427"

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
    # - end -

    # Create job agent
    agent = sql_client.job_agents.begin_create_or_update(
        GROUP_NAME,
        SERVER,
        JOB_AGENT,
        {
            "location": "eastus",
            "database_id": f"/subscriptions/{SUBSCRIPTION_ID}/resourceGroups/{GROUP_NAME}/providers/Microsoft.Sql/servers/{SERVER}/databases/{DATABASE}",
        },
    ).result()

    print(f"Create job agent:\n{agent}")

    # Create job credential
    credential = sql_client.job_credentials.create_or_update(
        GROUP_NAME,
        SERVER,
        JOB_AGENT,
        CREDENTIAL,
        {
          "username": "myuser",
          "password": "<password>"
        }
    )
    print(f"Create job credential:\n{credential}")

    # Create job target group
    group = sql_client.job_target_groups.create_or_update(
        GROUP_NAME,
        SERVER,
        JOB_AGENT,
        TARGET_GROUP,
        {
          "members": []
        }
    )
    print(f"Create job target group:\n{group}")

    # Create job
    job = sql_client.jobs.create_or_update(
        GROUP_NAME,
        SERVER,
        JOB_AGENT,
        JOB,
        {
          "description": "my favourite job",
          "schedule": {
            "start_time": "2020-10-24T18:30:01Z",
            "end_time": "2020-10-24T23:59:59Z",
            "type": "Recurring",
            "interval": "PT5M",
            "enabled": True
          }
        }
    )
    print(f"Create job:\n{job}")

    # Create job step
    step = sql_client.job_steps.create_or_update(
        GROUP_NAME,
        SERVER,
        JOB_AGENT,
        JOB,
        JOB_STEP,
        {
            "target_group": f"/subscriptions/{SUBSCRIPTION_ID}/resourceGroups/{GROUP_NAME}/providers/Microsoft.Sql/servers/{SERVER}/jobAgents/{JOB_AGENT}/targetGroups/{TARGET_GROUP}",
            "credential": f"/subscriptions/{SUBSCRIPTION_ID}/resourceGroups/{GROUP_NAME}/providers/Microsoft.Sql/servers/{SERVER}/jobAgents/{JOB_AGENT}/credentials/{CREDENTIAL}",
            "action": {"value": "select 1"},
        },
    )

    print(f"Create job step:\n{step}")

    # Create job execution
    execution = sql_client.job_executions.begin_create_or_update(
        GROUP_NAME,
        SERVER,
        JOB_AGENT,
        JOB,
        JOB_EXECUTION_ID
    ).result()
    print(f"Create execution:\n{execution}")

    # Get job
    job = sql_client.jobs.get(
        GROUP_NAME,
        SERVER,
        JOB_AGENT,
        JOB
    )
    print(f"Get job:\n{job}")

    # Delete job
    job = sql_client.jobs.delete(
        GROUP_NAME,
        SERVER,
        JOB_AGENT,
        JOB
    )
    print("Delete job.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()
