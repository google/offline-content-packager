# Copyright 2015 The Offline Content Packager Authors. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Script for converting content to Zip/ISO format.
"""

from os import makedirs
from os import stat
from os import walk
from os.path import isdir
from os.path import join
from shutil import copy2
from shutil import copytree
import sys

import click
from scripts.utils import to_iso
from scripts.utils import to_zip
from .verifyconfig import readconfig


def makeiso(size=None):
  """Converts content to ISO format.

  Args:
    size: Size of the content to be converted
  """
  try:
    click.echo("\nReading and verifying "
               "configuration file.....................")
    result = readconfig(["division", "destination.main_path",
                         "output_folder_name"], True)
    division = result[0]
    dst = result[1]
    folder_name = result[2]
  except:
    click.echo("Unable to read information from config.yaml. Fix it (or "
               "check it out from github) then try again.")
    return

  if not division:
    iso_maker(join(dst, folder_name), dst, folder_name, size)
  else:
    if not isdir(join(dst, "iso")):
      copytree(join(dst, folder_name, "img"),
               join(dst, "iso", "img"), symlinks=True)
    for div in division:
      dst_dir = join(dst, "goc", div)
      iso_maker(dst_dir, join(dst, "iso"), div, size)

    copy2(join(dst, folder_name, "index.html"), join(dst, "iso"))


def iso_maker(dst_dir, dst, div, size):
  """Gets size of content then converts content to ISO format.

  Args:
    dst_dir: Destination directory
    dst: Destination file name
    div: Division object
    size: size of content
  """
  if not isdir(dst_dir):
    click.echo(
        "Error: No output for div %s. Have you run the bundle command?" % div)
    return

  if size:
    max_size = int(size)
    parts = split(dst_dir, max_size)
    for i, part in enumerate(parts):
      click.echo(
          "Packaging content in a ISO format %d / %d" % (i+1, len(parts)))
      to_iso(dst_dir, join(dst, "%s%d.iso" % (div, i+1)), filelist=part)
  else:
    # convert to ISO file
    click.echo("Packaging content in a ISO format..................")
    to_iso(dst_dir, join(dst, "%s.iso" % div))


def zip_maker(dst_dir, dst, div, size):
  """Converts content to ZIP format.

  Args:
    dst_dir: Destination directory
    dst: Destination file name
    div: Division object
    size: size of content
  """
  if not isdir(dst_dir):
    click.echo(
        "Error: No output for div %s. Have you run the bundle command?" % div)
    return

  if size:
    max_size = int(size)
    parts = split(dst_dir, max_size)
    for i, part in enumerate(parts):
      click.echo(
          "Packaging content in a zip file %d / %d" % (i+1, len(parts)))
      to_zip(dst_dir, join(dst, "%s%d.zip" % (div, i+1)), False, filelist=part)
  else:
    # convert to zip file
    click.echo("Packaging content in a zip file..................")
    to_zip(dst_dir, join(dst, "%s.zip" % div), False)


def makezip(size=None):
  """Gets size of content then converts content to Zip format.

  Args:
    size: Size of the content to be converted
  """
  try:
    click.echo(
        "\nReading and verifying configuration file.....................")
    result = readconfig(["division", "destination.main_path",
                         "output_folder_name"], True)
    division = result[0]
    dst = result[1]
    folder_name = result[2]
  except:
    click.echo("Unable to read information from config.yaml."
               " Fix, then try again.")
    return

  if not division:
    # #convert to zip file and ISO
    zip_maker(join(dst, folder_name), dst, folder_name, size)
  else:
    if not isdir(join(dst, "zip")):
      copytree(join(dst, folder_name, "img"),
               join(dst, "zip", "img"), symlinks=True)
    for div in division:
      dst_dir = join(dst, "goc", div)
      zip_maker(dst_dir, join(dst, "zip"), div, size)

    copy2(join(dst, folder_name, "index.html"), join(dst, "zip"))


def split(dst_dir, max_size):
  """Checks the total size of content, then split content.

  Args:
    dst_dir: Destination directory
    max_size: Maximum size of a split

  Returns:
    List of splits
  """
  parts = []
  current_part = []
  current_free = max_size

  for srcpath, dirnames, filenames in walk(dst_dir):

    for name in filenames:
      src = join(srcpath, name)
      info = stat(src)
      size = 1.0 * info.st_size / 1024 / 1024

      if current_free < size:
        # create a new part
        parts.append(current_part)
        current_part = []
        current_free = max_size

      current_part.append(src)
      current_free -= size

    if not dirnames and not filenames:
      current_part.append(srcpath)

  parts.append(current_part)
  return parts
