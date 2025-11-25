#!/usr/bin/env python3

# Copyright (c) 2025 Antmicro <www.antmicro.com>
# SPDX-License-Identifier: Apache-2.0

import yaml
import argparse
import requests
from format import format_vendors

ZEPHYR_VENDOR_LIST_URL = "https://raw.githubusercontent.com/zephyrproject-rtos/zephyr/refs/heads/main/dts/bindings/vendor-prefixes.txt"


def get_zephyr_vendors():
    response = requests.get(ZEPHYR_VENDOR_LIST_URL)
    response.raise_for_status()
    lines = response.text.splitlines()
    return {
        prefix: full_name
        for line in lines
        if line.strip()
        and not line.lstrip().startswith("#")
        and not line.startswith("vnd")
        for prefix, full_name in [line.split("\t")]
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("vendor_list")
    parser.add_argument("-f", "--fix", action="store_true")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    if not (args.fix or args.verbose):
        parser.error("You must provide at least one of --fix or --verbose.")

    with open(args.vendor_list) as f:
        vendors = yaml.safe_load(f) or {}

    zephyr_vendors = get_zephyr_vendors()
    missing = [(p, name) for p, name in zephyr_vendors.items() if p not in vendors]

    if args.verbose:
        for p, name in missing:
            print(f"{name} ({p}) is in Zephyr but missing locally")

    if args.fix and missing:
        for p, name in missing:
            vendors[p] = {"display_name": name, "logo": False}

        with open(args.vendor_list, "w") as f:
            f.write(format_vendors(vendors).decode("utf-8"))


if __name__ == "__main__":
    main()
