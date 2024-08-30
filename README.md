# Unified vendors list

Copyright (c) 2024 [Antmicro](https://www.antmicro.com)

This repo contains information about vendors featured on [designer.antmicro.com](https://designer.antmicro.com) and [openhardware.antmicro.com](https://openhardware.antmicro.com).

## Data format

The main file, `vendors.yaml` contains descriptions of vendors.
Each entry, indexed by vendor ID, contains the following information:

- `display-name` -- printable name of the vendor
- `logo` -- information whether the vendor logo is present (default: `True`)
- `website` -- URL to vendor website
- `see` -- reference to another ID (used, for instance, when a vendor gets acquired by another).

For more information, see the [schema for this format](./validate/vendor-list-schema.yaml).

Additionally, the `vendor-icons` and `vendor-logos` directories contain the images for each vendor.
When the `logo` property is true for a vendor, both directories need to contain images.

## Validation

To help extend this repo with new information, there is a script which validates the information.
To use it, run:

```sh
./validate/validate.py vendors.yaml --schema ./validate/vendor-list-schema.yaml --logos ./vendor-logos/ --icons ./vendor-icons/
```

This script verifies the data format, and whether all necessary images are present (based on the `logo` property values).

## Creating Logos

Each vendor has two corresponding images:

- icon -- located in the `vendor-icons` directory. Recommended icon size is 90px by 90px. If the vendor does not have a dedicated icon, you can use the favicon from their website. If there is no favicon or recognizable symbol, you should use the vendor's full logo and downscale it to 90px by 90 px.
- logo -- vendor logo, stored in the `vendor-logos` directory. The size of the full logo is flexible, but it should follow the guidelines provided on the [Figma](https://www.figma.com/design/Wf4Cvbhi6La6eHtJqCzasQ/logo-base?node-id=0-1&t=BVDTDKXveaTkarW6-1) page.

Both the icon and full logo need to be vector-based, designed for a dark background, and saved in .svg format.
