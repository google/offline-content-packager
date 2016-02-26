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

"""Verification of necessary configuration files and key is done here.
"""
import logging
from os.path import exists
from os.path import isfile
from os.path import join
import sys

import click
import yaml


def readconfig(important_keys, retprop=False):
  """Reads the main configuration file and checks keys.

  Reads the main configuration file and calls
  the verify_and_extract_main_config to check keys.

  Args:
    important_keys: Keys in the config file that must be present
    retprop: Flag to indicate if the properties should be returned or not

  Returns:
    The properties or the configuration data
  """
  if not isfile("./config.yaml"):
    click.echo("There is no configuration file.")
    logging.debug("There is no configuration file.")
    sys.exit(1)

  with open("./config.yaml") as data_file:
    conf_data = yaml.load(data_file)

  # Error Handling inside the configuration file
  return verify_and_extract_main_config(conf_data, important_keys, retprop)


def verify_and_extract_main_config(conf_data, important_keys, retprop):
  """Check and verify that each key is in the configuration file.

  Args:
    conf_data: Dictionary representing data read from YAML file
    important_keys: Keys in the config file that must be present
    retprop: Flag to indicate if the properties should be returned or not

  Returns:
    The properties or the configuration data
  """
  if retprop:
    properties = []

  for key in important_keys:
    key_path = key.split(".")
    key_dict = conf_data
    for path in key_path:
      try:
        key_dict = key_dict[path]
      except:
        click.echo("The field '" + key +
                   "' is required. Please make sure it exists in the main"
                   " config.yaml file.")
        sys.exit(1)
    if retprop:
      properties.append(key_dict)

  if retprop:
    if len(properties) == 1:
      return properties[0]
    else:
      return properties
  else:
    return conf_data


def verify_section_config(src_dir, sections, video_src):
  """Performs sanity check.

  Performs sanity check on all the sections to be processed, and
  gives necessary feedback.

  Args:
    src_dir: Source Directory
    sections: List of sections
    video_src: Directory holding videos
  """
  error_list = []
  for section in sections:
    if not section.startswith(video_src):
      if not isfile(join(src_dir, section, "section_config.yaml")):
        error_list.append(section)

  if error_list:
    click.echo(click.style(
        "These section(s) don't have a config.yaml, create one:", fg="red"))
    click.echo(click.style(", ".join(error_list), fg="yellow", bold=True))
    logging.debug("These section(s) don't have a config.yaml, create one:" +
                  ", ".join(error_list))
    sys.exit(1)

  if not exists(join(src_dir, video_src)):
    click.echo(click.style("\nError:" + video_src +
                           " ) specified doesn't exist\n", fg="red"))
    logging.error("Video Source Directory( " +
                  video_src + " ) specified doesn't exist")
    sys.exit(1)
  click.echo(click.style("Finished sanity check. Continue.", fg="green"))
