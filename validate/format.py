#!/usr/bin/env python3

# Copyright (c) 2024 Antmicro <www.antmicro.com>
# SPDX-License-Identifier: Apache-2.0

import argparse
import os
import subprocess
import sys
import tempfile
import yaml


def show_difference(original_file, formatted):
    _, tmp_file = tempfile.mkstemp(".yaml")
    with open(tmp_file, "wb") as f:
        f.write(formatted)
    subprocess.run(["diff", "-u", "--color=always", original_file, tmp_file])
    os.remove(tmp_file)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("vendor_list")
    parser.add_argument("-f", "--fix", action="store_true")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()
    prog_name = parser.prog

    with open(args.vendor_list, "rb") as f:
        original_content = f.read()

    vendors = yaml.safe_load(original_content)

    header = (
        "# Copyright (c) 2024 Antmicro <www.antmicro.com>\n"
        "# SPDX-License-Identifier: Apache-2.0\n\n"
    )

    if args.fix:
        with open("vendors.yaml", "w") as f:
            f.write(header)
            yaml.dump(vendors, f, sort_keys=True, allow_unicode=True, encoding=("utf-8"))
        return

    formatted = header.encode("utf-8") + yaml.dump(vendors, sort_keys=True, allow_unicode=True, encoding=("utf-8"))
    if formatted != original_content:
        if args.verbose:
            show_difference(args.vendor_list, formatted)
        print(
            f"The {args.vendor_list} is not formatted correctly. "
            f"Run {prog_name} -f to fix formatting."
        )
        sys.exit(1)
    else:
        print(f"Formatting in {args.vendor_list} correct.")


if __name__ == "__main__":
    main()
