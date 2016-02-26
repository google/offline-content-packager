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

"""Download Image Script.
"""
from os import makedirs
from os.path import isdir
from os.path import join
from os.path import splitext
import sys

import click

try:
  from urllib.request import urlretrieve
except ImportError:
  from urllib import urlretrieve


def download_image(url, out_folder, video_name):
  """Downloads from specified url.

  Args:
    url: URL to image
    out_folder: folder to write image file to
    video_name: Name with which image will be saved

  Returns:
    File name of saved image or False if image could not be downloaded
  """
  click.echo("\nDownloading image for " + video_name)
  if not isdir(join(out_folder, "images")):
    makedirs(join(out_folder, "images"))
  try:
    url_part = url.split("/")[-1]
    _, url_last_extension = splitext(url_part)
    out_file = join(out_folder, "images", video_name + url_last_extension)

    urlretrieve(url, out_file)
    click.echo("Successfully downloaded " + video_name + " thumbnail")
    return video_name + url_last_extension
  except:
    click.echo("\nUnable to download thumbnail for " + video_name)
    return False
