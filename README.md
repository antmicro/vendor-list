# Unified vendors list

Copyright (c) 2024 [Antmicro](https://www.antmicro.com)

This repo contains information about vendors that are used on [designer.antmicro.com](https://designer.antmicro.com) and on [openhardware.antmicro.com](https://openhardware.antmicro.com).

## Data format

The main file, `vendors.yaml` contains the description of vendors.
Each entry, indexed by vendor ID, contains following information:

- `display-name` -- Printable name of the vendor.
- `logo` -- Information if the vendor logo is present (default: `True`)
- `website` -- A URL to vendor website.
- `see` -- Reference to another id (e.g. when one vendor is acquired by another).

For more information see the [schema for this format](./validate/vendor-list-schema.yaml).

Additionally, the `vendor-icons` and `vendor-logos` directories contain the images for each vendor.
If the `logo` property is true, then the vendor is supposed to have images in both directories.

## Validation

In order to help extending this repo with new information there is a script which validates the information.
To use it run:

```sh
./validate/validate.py vendors.yaml --schema ./validate/vendor-list-schema.yaml --logos ./vendor-logos/ --icons ./vendor-icons/
```

This script verifies if data is in correct format and if all vendors have their respective images, or the `logo` property set to `false`.
