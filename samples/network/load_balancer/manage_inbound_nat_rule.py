# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import os

from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.resource import ResourceManagementClient


def main():

    SUBSCRIPTION_ID = os.environ.get("SUBSCRIPTION_ID", None)
    GROUP_NAME = "testgroupx"
    INBOUND_NAT_RULE = "inbound_nat_rulexxyyzz"
    LOAD_BALANCER_NAME = LOAD_BALANCER = "load_balancerxxyyzz"
    PUBLIC_IP_ADDRESS_NAME = "public_ip_address_name"
    FRONTEND_IPCONFIGURATION_NAME = "myFrontendIpconfiguration"
    BACKEND_ADDRESS_POOL_NAME = "myBackendAddressPool"
    LOAD_BALANCING_RULE_NAME = "myLoadBalancingRule"
    OUTBOUND_RULE_NAME = "myOutboundRule"
    PROBE_NAME = "myProbe"

    # Create client
    # For other authentication approaches, please see: https://pypi.org/project/azure-identity/
    resource_client = ResourceManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )
    network_client = NetworkManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id=SUBSCRIPTION_ID
    )

    # Create resource group
    resource_client.resource_groups.create_or_update(
        GROUP_NAME,
        {"location": "eastus"}
    )

    # - init depended resources -
    # Create public ip address
    network_client.public_ip_addresses.begin_create_or_update(
        GROUP_NAME,
        PUBLIC_IP_ADDRESS_NAME,
        {
            'location': "eastus",
            'public_ip_allocation_method': 'Static',
            'idle_timeout_in_minutes': 4,
            'sku': {
              'name': 'Standard'
            }
        }
    ).result()

    # Create load balancer
    network_client.load_balancers.begin_create_or_update(
        GROUP_NAME,
        LOAD_BALANCER,
        {
            "location": "eastus",
            "sku": {"name": "Standard"},
            "frontendIPConfigurations": [
                {
                    "name": FRONTEND_IPCONFIGURATION_NAME,
                    "public_ip_address": {
                        "id": f"/subscriptions/{SUBSCRIPTION_ID}/resourceGroups/{GROUP_NAME}/providers/Microsoft.Network/publicIPAddresses/{PUBLIC_IP_ADDRESS_NAME}"
                    },
                }
            ],
            "backend_address_pools": [{"name": BACKEND_ADDRESS_POOL_NAME}],
            "load_balancing_rules": [
                {
                    "name": LOAD_BALANCING_RULE_NAME,
                    "frontend_ip_configuration": {
                        "id": f"/subscriptions/{SUBSCRIPTION_ID}/resourceGroups/{GROUP_NAME}/providers/Microsoft.Network/loadBalancers/{LOAD_BALANCER_NAME}/frontendIPConfigurations/{FRONTEND_IPCONFIGURATION_NAME}"
                    },
                    "frontend_port": "80",
                    "backend_port": "80",
                    "enable_floating_ip": True,
                    "idle_timeout_in_minutes": "15",
                    "protocol": "Tcp",
                    "load_distribution": "Default",
                    "disable_outbound_snat": True,
                    "backend_address_pool": {
                        "id": f"/subscriptions/{SUBSCRIPTION_ID}/resourceGroups/{GROUP_NAME}/providers/Microsoft.Network/loadBalancers/{LOAD_BALANCER_NAME}/backendAddressPools/{BACKEND_ADDRESS_POOL_NAME}"
                    },
                    "probe": {
                        "id": f"/subscriptions/{SUBSCRIPTION_ID}/resourceGroups/{GROUP_NAME}/providers/Microsoft.Network/loadBalancers/{LOAD_BALANCER_NAME}/probes/{PROBE_NAME}"
                    },
                }
            ],
            "probes": [
                {
                    "name": PROBE_NAME,
                    "protocol": "Http",
                    "port": "80",
                    "request_path": "healthcheck.aspx",
                    "interval_in_seconds": "15",
                    "number_of_probes": "2",
                }
            ],
            "outbound_rules": [
                {
                    "name": OUTBOUND_RULE_NAME,
                    "backend_address_pool": {
                        "id": f"/subscriptions/{SUBSCRIPTION_ID}/resourceGroups/{GROUP_NAME}/providers/Microsoft.Network/loadBalancers/{LOAD_BALANCER_NAME}/backendAddressPools/{BACKEND_ADDRESS_POOL_NAME}"
                    },
                    "frontend_ip_configurations": [
                        {
                            "id": f"/subscriptions/{SUBSCRIPTION_ID}/resourceGroups/{GROUP_NAME}/providers/Microsoft.Network/loadBalancers/{LOAD_BALANCER_NAME}/frontendIPConfigurations/{FRONTEND_IPCONFIGURATION_NAME}"
                        }
                    ],
                    "protocol": "All",
                }
            ],
        },
    ).result()

    # - end -

    # Create inbound nat rule
    inbound_nat_rule = network_client.inbound_nat_rules.begin_create_or_update(
        GROUP_NAME,
        LOAD_BALANCER,
        INBOUND_NAT_RULE,
        {
            "protocol": "Tcp",
            "frontend_ip_configuration": {
                "id": f"/subscriptions/{SUBSCRIPTION_ID}/resourceGroups/{GROUP_NAME}/providers/Microsoft.Network/loadBalancers/{LOAD_BALANCER_NAME}/frontendIPConfigurations/{FRONTEND_IPCONFIGURATION_NAME}"
            },
            "frontend_port": "3390",
            "backend_port": "3389",
            "idle_timeout_in_minutes": "4",
            "enable_tcp_reset": False,
            "enable_floating_ip": False,
        },
    ).result()

    print(f"Create inbound nat rule:\n{inbound_nat_rule}")

    # Get inbound nat rule
    inbound_nat_rule = network_client.inbound_nat_rules.get(
        GROUP_NAME,
        LOAD_BALANCER,
        INBOUND_NAT_RULE
    )
    print(f"Get inbound nat rule:\n{inbound_nat_rule}")

    # Delete inbound nat rule
    inbound_nat_rule = network_client.inbound_nat_rules.begin_delete(
        GROUP_NAME,
        LOAD_BALANCER,
        INBOUND_NAT_RULE
    ).result()
    print("Delete inbound nat rule.\n")

    # Delete Group
    resource_client.resource_groups.begin_delete(
        GROUP_NAME
    ).result()


if __name__ == "__main__":
    main()
