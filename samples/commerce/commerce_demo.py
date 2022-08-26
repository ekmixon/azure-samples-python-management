# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import os
import datetime as dt

from azure.identity import DefaultAzureCredential
from azure.mgmt.commerce import UsageManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)

    # Create client
    # # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    usage_client = UsageManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    # List usage aggregates
    output = usage_client.usage_aggregates.list(
        f'{str(dt.date.today() - dt.timedelta(days=1))}T00:00:00Z',
        f'{str(dt.date.today())}T00:00:00Z',
    )

    print(f"List usage aggregate:\n{output}")

    # Get rate card
    rate = usage_client.rate_card.get(
        "OfferDurableId eq 'MS-AZR-0062P' and Currency eq 'USD' and Locale eq 'en-US' and RegionInfo eq 'US'"
    )
    print(f"Get rate card:\n{rate}")


if __name__ == "__main__":
    main()
