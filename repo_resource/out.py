#!/usr/bin/env python

# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 (c) BayLibre, SAS
# Author: Mattijs Korpershoek <mkorpershoek@baylibre.com>

import json
import sys


def out(instream):
    return []


def main():
    print(json.dumps(out(sys.stdin)))


if __name__ == '__main__':
    main()
