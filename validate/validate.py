#!/usr/bin/env python3

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

    for v_name, v_data in vendors.items():
        logo = v_data.get("logo", True)
        if not logo:
            no_logo.append(v_name)
            continue

        logo_path = logos_dir / f"{v_name}.svg"
        icon_path = icons_dir / f"{v_name}.svg"
        if not logo_path.exists():
            missing_logos.append(logo_path)

        if not icon_path.exists():
            missing_icons.append(icon_path)

    return missing_logos, missing_icons, no_logo


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

    return_code = 0

    missing_logos, missing_icons, no_logo = validate_vendor_images(vendors, args.logos, args.icons)

    # Print information about missing logos, but the ones that are expected.
    if no_logo:
        print(f"There are {len(no_logo)} vendors without logo.")

    if missing_logos:
        print(f"There are {len(missing_logos)} missing logos:")
        print("\n".join(f" - {p}" for p in missing_logos))
        return_code = 1

    if missing_icons:
        print(f"There are {len(missing_icons)} missing icons:")
        print("\n".join(f" - {p}" for p in missing_icons))
        return_code = 1

    if not_assigned := find_not_assigned_logos(vendors, args.logos, args.icons):
        print(f"There are {len(not_assigned)} not assigned logos:")
        print("\n".join(f" - {v}" for v in not_assigned))
        return_code = 1

    sys.exit(return_code)


if __name__ == "__main__":
    main()
