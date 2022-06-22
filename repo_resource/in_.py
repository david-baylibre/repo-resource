#!/usr/bin/env python

# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 (c) BayLibre, SAS
# Author: Mattijs Korpershoek <mkorpershoek@baylibre.com>

import json
import sys


def in_(instream):
    return []


def main():
    print(json.dumps(in_(sys.stdin)))


if __name__ == '__main__':
    main()
