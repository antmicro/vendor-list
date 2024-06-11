#!/usr/bin/env python3

# Copyright (c) 2024 Antmicro <www.antmicro.com>
# SPDX-License-Identifier: Apache-2.0

import argparse
import sys
import yaml

from pathlib import Path

from jsonschema import validate
from jsonschema.exceptions import ValidationError


def validate_schema(validate_dict, schema):
    try:
        validate(instance=validate_dict, schema=schema)
        return True
    except ValidationError as e:
        print(e)
        return False


def validate_vendor_images(vendors, logos_dir, icons_dir):
    missing_logos = []
    missing_icons = []
    no_logo = []
    extra_images = []

    for v_name, v_data in vendors.items():
        logo_path = logos_dir / f"{v_name}.svg"
        icon_path = icons_dir / f"{v_name}.svg"

        # Node with 'see' property should not have images
        if "see" in v_data:
            if logo_path.exists():
                extra_images.append(logo_path)
            if icon_path.exists():
                extra_images.append(icon_path)
            continue

        logo = v_data.get("logo", True)

        # When 'logo' is False we expect vendor to have no images
        if not logo:
            if logo_path.exists():
                extra_images.append(logo_path)
            if icon_path.exists():
                extra_images.append(icon_path)
            no_logo.append(v_name)
            continue

        # When 'logo' is True vendor must have both icon and logo
        if not logo_path.exists():
            missing_logos.append(logo_path)
        if not icon_path.exists():
            missing_icons.append(icon_path)

    return_code = 0

    print_missing_img(no_logo, "vendors without logo", show=False)

    if print_missing_img(extra_images, "extra images"):
        return_code = 1

    if print_missing_img(missing_logos, "missing logos"):
        return_code = 1

    if print_missing_img(missing_icons, "missing icons"):
        return_code = 1

    return return_code

def print_missing_img(images, msg, show=True):
    if images:
        print(f"There are {len(images)} {msg}")
        if show:
            print("\n".join(f" - {p}" for p in images))
        return True
    return False


def find_not_assigned_logos(vendors, logos_dir, icons_dir):
    not_assigned = []

    for logo in logos_dir.glob("*.svg"):
        if logo.stem not in vendors:
            not_assigned.append(str(logo))

    for logo in icons_dir.glob("*.svg"):
        if logo.stem not in vendors:
            not_assigned.append(str(logo))

    return not_assigned


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("vendor_list")
    parser.add_argument("-l", "--logos", type=Path, default=Path("vendor-logos/"))
    parser.add_argument("-i", "--icons", type=Path, default=Path("vendor-icons/"))
    parser.add_argument("-s", "--schema", type=Path, default=Path("validate/vendor-list-schema.yaml"))
    args = parser.parse_args()

    with open(args.schema) as f:
        schema = yaml.safe_load(f)

    with open(args.vendor_list) as f:
        vendors = yaml.safe_load(f)

    if not validate_schema(vendors, schema):
        print(f"Format of {args.vendor_list} is invalid!", file=sys.stderr)
        sys.exit(1)

    return_code = validate_vendor_images(vendors, args.logos, args.icons)

    not_assigned = find_not_assigned_logos(vendors, args.logos, args.icons)
    if print_missing_img(not_assigned, "not assigned images"):
        return_code = 1

    sys.exit(return_code)


if __name__ == "__main__":
    main()
