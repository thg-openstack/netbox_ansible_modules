#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2023, Andrii Konts (@andrii-konts) <andrew.konts@uk2group.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: netbox_asn_range
short_description: Create, update or delete ASN ranges within NetBox
description:
  - Creates, updates or removes ASN ranges from NetBox
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Andrii Konts (@andrii-konts)
requirements:
  - pynetbox
seealso:
  - name: ASN Range Model reference
    description: NetBox Documentation for ASN Range Model.
    link: https://docs.netbox.dev/en/stable/models/ipam/asnrange/
version_added: '3.12.0'
extends_documentation_fragment:
  - netbox.netbox.common
options:
  data:
    type: dict
    description:
      - Defines the ASN Range configuration
    suboptions:
      name:
        description:
          - ASN Range name
        required: true
        type: str
      slug:
        description:
          - A unique URL-friendly identifier
        type: str
      rir:
        description:
          - The Regional Internet Registry or similar authority responsible for the allocation of AS numbers within this range
        type: int
      start:
        description:
          - The starting numeric boundary of the range (inclusive)
        type: int
      end:
        description:
          - The ending numeric boundary of the range (inclusive)
        type: int
      tenant:
        description:
          - Tenant
        type: int
      description:
        description:
          - Description (max length 200)
        required: false
        type: str
      tags:
        description:
          - Any tags that the ASN Range may need to be associated with
        required: false
        type: list
        elements: raw
      custom_fields:
        description:
          - Must exist in NetBox
        required: false
        type: dict
    required: true
"""

EXAMPLES = r"""
- hosts: localhost
  connection: local
  module_defaults:
    group/netbox.netbox.netbox:
      netbox_url: "http://netbox.local"
      netbox_token: "thisIsMyToken"

  tasks:
    - name: "Create ASN range within netbox"
      netbox.netbox.netbox_asn_range:
        data:
          name: Test ASN range
          slug: test-asn-range
          rir: 1
          start: 1
          end: 1000
          description: test ASN range
        state: present

    - name: Delete ASN Range within netbox
      netbox.netbox.netbox_asn_range:
        data:
          name: Test ASN range
        state: absent
"""

RETURN = r"""
ans_range:
  description: Serialized object as created or already existent within NetBox
  returned: success (when I(state=present))
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from ansible_collections.netbox.netbox.plugins.module_utils.netbox_utils import (
    NetboxAnsibleModule,
    NETBOX_ARG_SPEC,
)
from ansible_collections.netbox.netbox.plugins.module_utils.netbox_ipam import (
    NetboxIpamModule,
    NB_ASN_RANGES,
)

from copy import deepcopy


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NETBOX_ARG_SPEC)
    argument_spec.update(
        dict(
            data=dict(
                type="dict",
                required=True,
                options=dict(
                    name=dict(type="str", required=True),
                    slug=dict(type="str"),
                    rir=dict(type="int"),
                    start=dict(type="int"),
                    end=dict(type="int"),
                    description=dict(type="str"),
                    tags=dict(required=False, type="list", elements="raw"),
                    custom_fields=dict(required=False, type="dict"),
                ),
            ),
        )
    )
    required_if = [("state", "present", ["name", "slug", "rir", "start", "end"])]
    module = NetboxAnsibleModule(argument_spec=argument_spec, required_if=required_if)
    netbox_asn_range = NetboxIpamModule(module, NB_ASN_RANGES)
    netbox_asn_range.run()


if __name__ == "__main__":
    main()
