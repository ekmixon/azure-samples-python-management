# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

import os
import time
from azure.identity import DefaultAzureCredential
from azure.mgmt.consumption import ConsumptionManagementClient
from azure.mgmt.resource import ResourceManagementClient

# - other dependence -
# - end -


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    TIME = str(time.time()).replace('.','')
    GROUP_NAME = f"testconsumption{TIME}"
    CONSUMPTION = f"consumption{TIME}"

    # Create client
    # # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    consumption_client = ConsumptionManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    # - init depended client -
    # - end -

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # - init depended resources -
    # - end -

    # Create consumption
    SCOPE = f'/subscriptions/{SUBSCRIPTION_ID}/resourceGroups/{GROUP_NAME}'
    consumption = consumption_client.budgets.create_or_update(
        SCOPE,
        CONSUMPTION,
        {
            "category": "Cost",
            "amount": '100',
            "timeGrain": "Monthly",
            "timePeriod": {
                "startDate": "2020-10-01T00:00:00Z",
                "endDate": "2021-10-31T00:00:00Z"
            }
        }
    )
    print(f"Create consumption:\n{consumption}\n")

    # Get consumption
    consumption = consumption_client.budgets.get(
        SCOPE,
        CONSUMPTION
    )
    print(f"Get consumption:\n{consumption}\n")

    # Delete consumption
    consumption_client.budgets.delete(
        SCOPE,
        CONSUMPTION
    )
    print("Delete consumption.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()
