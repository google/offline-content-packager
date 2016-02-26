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

"""ISO converter script.
"""
import logging
from os import link
from os import makedirs
from os import system
from os import unlink
from os.path import dirname
from os.path import isdir
from os.path import isfile
from os.path import join
from sys import platform
from tempfile import mkdtemp

import click


def to_iso(source, destination, filelist=None):
  """ISO converter utility.

  Convert contents to ISO format checking the systems platform where the tool
  is being run.

  Args:
    source: path to directory with content to be converted
    destination: path to destination where the ISO file is written
    filelist: TBD
  """
  # overwrite existing ISO file
  if isfile(destination):
    unlink(destination)

  if filelist:
    # create tmp dir
    tmpdir = mkdtemp()
    for item in filelist:
      rel = item[len(source)+1:]
      dst = join(tmpdir, rel)

      if not isdir(dirname(dst)):
        makedirs(dirname(dst))

      if not isdir(item):
        link(item, dst)

    source = tmpdir

  if platform.startswith("darwin"):
    system("hdiutil makehybrid -iso -joliet -o %s %s"%(destination, source))
    click.echo("Finished!")
  elif platform.startswith("linux"):
    system("mkisofs -r -J -o %s %s"%(destination, source))
    click.echo("Finished!")
  else:
    click.echo(platform + (" not supported for converting to ISO files."
                           "Try to download ISO maker tool from "
                           "'http://www.magiciso.com/tutorials/"
                           "miso-iso-creator.htm'"))
    logging.debug(platform + (" not supported for converting to ISO files."
                              "Try to download ISO maker tool from "
                              "'http://www.magiciso.com/tutorials/"
                              "miso-iso-creator.htm'"))
