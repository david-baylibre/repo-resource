#!/usr/bin/env python

# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 (c) BayLibre, SAS
# Author: Mattijs Korpershoek <mkorpershoek@baylibre.com>

import json
import sys

from pathlib import Path

from repo_resource import common


def in_(instream, dest_dir='.'):
    """Fetch the resource and place it in dest_dir

    We receive on stdin the configured source
    and a precise version of the resource to fetch.

    If the desired resource version is unavailable (for example, if it was
    deleted), the script must exit with error.

    The script must emit the fetched version, and may emit metadata as a list
    of key-value pairs. This data is intended for public consumption and will
    make it upstream, intended to be shown on the build's page.
    """
    payload = json.load(instream)

    if payload['version'].get('version') is None:
        raise RuntimeError('Did not receive any version')

    config = common.source_config_from_payload(payload)
    requested_version = common.Version(payload['version']['version'])

    standard_requested_version = common.Version(payload['version']['version']).standard()

    standard_versions = []
    current_version = None
    for v in payload.get('versions', []):
        standard_versions.append(common.Version(v['version']).standard())

    if config.private_key != '_invalid':
        common.add_private_key_to_agent(config.private_key)

    try:
        repo = common.Repo(config.url, config.revision, config.name, config.depth, workdir=Path(dest_dir))
        repo.init()
        repo.sync(requested_version, config.jobs)
        fetched_version = repo.currentVersion()
    except Exception as e:
        raise e
    finally:
        # always remove the key from the agent
        if config.private_key != '_invalid':
            common.remove_private_key_from_agent()

    # save a copy of the manifest alongside the sources
    repo.save_manifest('.repo_manifest.xml')

    metadata = repo.metadata()

    return {"version": {"version": str(requested_version)},
            "metadata": metadata}


def main():
    print(json.dumps(in_(sys.stdin, sys.argv[1])))


if __name__ == '__main__':
    main()
