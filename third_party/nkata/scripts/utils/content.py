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

"""Utility for bundling and getting sections.
"""
import logging
from os import listdir
from os.path import join

import click
from scripts.transformations import HtmlTransformation
from scripts.utils.fileutil import copy_files


def bundle_content_section(src_path, dst_path, section, config, online_link):
  """Bundles content.

  Calls copy_files method after setting necessary
  parameters in HtmlTransformation

  Args:
    src_path: Path to the content to be bundled
    dst_path: Path where the bundled content will be written
    section: Section to be bundled
    config: Dictionary containing configuration parameters
    online_link: URL to content online
  """
  # Initialising a list of transformations
  logging.info("Start bundling files from " + section + ".")
  transformations = []
  if online_link and not "http://" in online_link:
    online_link = "http://" + online_link

  link_color = config["link_color"]
  tracking_code = config["tracking_code"]
  html_transform = HtmlTransformation(color=link_color, code=tracking_code,
                                      link=online_link)
  transformations.append(html_transform)
  paths = (src_path, dst_path)
  copy_files(paths, section, transformations)
  click.echo("\n")
  logging.info("Finish bundling files from " + section + ".")


def bundle_video_section(paths, vid, metadata, transformations, videos_src):
  """Bundles videos.

  Calls copy_files method after setting necessary
  parameters in HtmlTransformation for videos only.

  Args:
    paths: Tuple of source and destination directories
    vid: Video Section
    metadata: Video metadata
    transformations: Transformation object
    videos_src: Path to video source directory
  """

  logging.info("Start bundling videos from " + vid + ".")
  copy_files(paths, vid, transformations, metadata, videos_src)
  click.echo("\n")
  logging.info("Finish bundling videos from " + vid + ".")


def get_divisions(division, ignored_sections):
  """Gets division in a list after removing the ignored_paths.

  Args:
    division: Division object
    ignored_sections: Sections to ignore

  Returns:
    List of sections for bundling

  """

  def is_content_division(item):
    """Removes ignored_section.

    Args:
      item: section to be checked

    Returns:
      False if item is to be ignored else returns true

    """

    if item in ignored_sections:
      return False

    item_list = item.split("/")
    if item_list[0] in ignored_sections:
      return False

    return True

  return ([item for item in division if is_content_division(item)],
          [item.replace(ignored_sections[0] + "/", "")
           for item in division if not is_content_division(item)])


def get_sections(src_dir, ignored_paths):
  """Gets section in a list after removing the ignored_paths.

  Args:
    src_dir: Source directory for content
    ignored_paths: Paths to content to be ignored

  Returns:
    List of sections to be processed

  """
  def is_content_section(item):
    """Removes ignored_paths and section starting with ".".

    Args:
      item: Section to be checked

    Returns:
      False if item is to be ignored, returns True otherwise
    """
    if item.startswith("."):
      return False

    path = join(src_dir, item)

    if path in ignored_paths:
      return False

    return True

  return [item for item in listdir(src_dir) if is_content_section(item)]
