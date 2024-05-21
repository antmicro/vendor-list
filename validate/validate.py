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


def validate_vendor_logos(vendors, logos_dir):
    missing_logos = []
    for v_name, v_data in vendors.items():
        logo = v_data.get("logo", True)
        if not logo:
            continue

        logo_path = logos_dir / f"{v_name}.svg"
        if not logo_path.exists():
            missing_logos.append(logo_path)

    return missing_logos


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("vendor_list")
    parser.add_argument("-l", "--logos", type=Path, default=Path("logos/"))
    parser.add_argument("-s", "--schema", type=Path, default=Path("validate/vendor-list-schema.yaml"))
    args = parser.parse_args()

    with open(args.schema) as f:
        schema = yaml.safe_load(f)

    with open(args.vendor_list) as f:
        vendors = yaml.safe_load(f)

    if not validate_schema(vendors, schema):
        print(f"Format of {args.vendor_list} is invalid!", file=sys.stderr)
        sys.exit(1)

    if missing := validate_vendor_logos(vendors, args.logos):
        print(f"There are {len(missing)} missing logos:")
        print("\n".join(f" - {p}" for p in missing))
        sys.exit(1)


if __name__ == "__main__":
    main()
