#!/usr/bin/env python

# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 (c) BayLibre, SAS
# Author: Mattijs Korpershoek <mkorpershoek@baylibre.com>
"""
Check step for an Android repo resource

This is done in a couple of steps
1. Repo init the manifest
2. Repo sync it
3. Generate a manifest snapshot
4. Compute the version of that snapshot
"""

import json
import sys

from repo_resource import common


def check(instream) -> list:
    """Checks a json formatted IOstream for new versions

    must print the array of new versions, in chronological order
    (oldest first), to stdout, including the requested version
    if it's still valid.
    """
    payload = json.load(instream)

    if payload['source'].get('url') is None:
        raise RuntimeError('manifest url is mandatory')

    config = common.source_config_from_payload(payload)

    standard_versions = []
    for v in payload.get('versions', []):
        standard_versions.append(common.Version(v['version']).standard())

    if config.private_key != '_invalid':
        common.add_private_key_to_agent(config.private_key)

    jobs = config.jobs
    check_jobs = config.check_jobs or jobs*2 or common.DEFAULT_CHECK_JOBS

    try:
        repo = common.Repo(config.url,
                           config.revision,
                           config.name,
                           config.depth)
        version = repo \
            .set_rewrite(config.rewrite) \
            .init() \
            .update_manifest(jobs=check_jobs) \
            .currentVersion()
    except Exception as e:
        raise e
    finally:
        # always remove the key from the agent
        if config.private_key != '_invalid':
            common.remove_private_key_from_agent()

    versions = payload.get('versions', [])
    if version.standard() not in standard_versions:
        versions.append({'version': str(version)})

    return versions


def main():
    print(json.dumps(check(sys.stdin)))


if __name__ == '__main__':
    main()
