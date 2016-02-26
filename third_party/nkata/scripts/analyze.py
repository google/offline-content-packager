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

"""Size summary for content.

Script gives basic information about the total size of
content in MegaBytes and the suitable storage medium to copy
content.
"""

import math
from os import walk
from os.path import getsize
from os.path import join
import click
import yaml


def analyze_content(size):
  """Analyze content for basic size information.

  Gives basic information about the total size of
  content in MegaBytes and the suitable storage medium to copy
  content.

  Args:
    size: Size of intended storage medium in MB
  """
  with open("./config.yaml") as data_file:
    conf_data = yaml.load(data_file)

  src_dir = conf_data["source"]["main_path"]
  total_size = get_size(src_dir) / 1000000.00

  if not size:
    single_layered_disc = int(math.ceil(total_size / 4700))
    dual_layered_disc = int(math.ceil(total_size / 8500))
    flash = int(math.ceil(total_size / 16000))
    click.echo("The total size of content is {0}MB".format(total_size))
    click.echo("You need {0} single-layered DVD disc(s) or {1} dual-layered"
               " DVD disc(s) to copy content".format(single_layered_disc,
                                                     dual_layered_disc))
    click.echo(
        " OR You need {0} (16GB) flash drive(s) to copy content".format(flash))
  else:
    device_number = int(math.ceil(total_size / int(size)))
    click.echo("The total size of content is {0}MB".format(total_size))
    click.echo(
        "You need {0} storage device of this size to copy content".format(device_number))


def get_size(start_path="."):
  """Gets total size of content.

  Args:
    start_path: Directory path to content

  Returns:
    Total size of content located at start_path
  """
  total_size = 0
  for dirpath, _, filenames in walk(start_path):
    for filename in filenames:
      filename_path = join(dirpath, filename)
      total_size += getsize(filename_path)
  return total_size
