#!/bin/env python3

# Code for reducing list of paths in arguments to minimal list of mounts they are on
# Copyright (C) 2024 Noel Kuntze
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


"""
Code for reducing list of paths in arguments to minimal list of mounts they are on
"""

import argparse
import logging
import os
import psutil
import sys
import subprocess

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s: %(message)s")
logger = logging.getLogger()


# we exclude these because we will never need to sync them
dirs_to_exclude = ["/dev", "/proc", "/run", "/sys", "/tmp"]

# we exclude these too so the script can run faster on a system with lots of virtual filesystems
types_to_exclude = ["overlay", "ramfs", "tmpfs", ]

# we use this approach instead of checking os.path.mountpoint because that way we only
# need to cross the userspace to kernelspace boundary here, where we get the mounts, and when we execute the `sync` command

partitions = sorted(psutil.disk_partitions(all=True), key=lambda x: len(x.mountpoint), reverse=True)

# list of mountpoints (directory paths) to sync
dirs_to_sync = []

def preprocess():
    indices_to_remove = []
    for index, part in enumerate(partitions):
        check_1 = part.mountpoint in dirs_to_exclude
        check_2 = any(map(lambda x: os.path.commonpath((x, part.mountpoint)) != "/", dirs_to_exclude))
        check_3 = any(map(lambda x: x == part.fstype, types_to_exclude))
        logger.debug("Check values: %s %s %s", check_1, check_2, check_3)
        if check_1 or check_2 or check_3:
            logger.debug("need to remove index %s", index)
            indices_to_remove.append(index)

    indices_to_remove.sort(reverse=True, key=lambda x: x)
    logger.debug("indices to remove: %s", indices_to_remove)
    for index in indices_to_remove:
        logger.debug("removing index %s with value %s", index, partitions[index])
        partitions.pop(index)

def find_mount_point(path):
    path = os.path.realpath(path)
    dir_to_append = "/"
    for partition in partitions:
        if os.path.commonpath((partition.mountpoint, path)) != "/":
            dir_to_append = partition.mountpoint
            break
    if dir_to_append not in dirs_to_sync:
        dirs_to_sync.append(dir_to_append)

def parse_args():
    argument_parser = argparse.ArgumentParser(description="Script for syncing mountpoints after system upgrades,"\
        " to be used as script for an alpm-hook")
    argument_parser.add_argument("-d", "--debug", help="Enable debug mode", action="store_true")

    args = argument_parser.parse_args()

    if args.debug:
        logger.info("enabling debug mode")
        logger.setLevel(logging.DEBUG)

def run():
    """
    Entrypoint for main function
    """
    parse_args()

    preprocess()

    for path in sys.stdin:
        path = path.strip()
        logger.debug("checking %s", path)
        find_mount_point(path)

    logger.info("Syncing these mountpoints now: %s", dirs_to_sync)
    subprocess.run(["sync", "--"] + dirs_to_sync, check=False)
    logger.info("Mountpoints now synced")

if __name__ == '__main__':
    run()

