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

"""Metadata from YouTube generator.
"""
import logging
from os import getcwd
from os import makedirs
from os import walk
from os.path import exists
from os.path import isdir
from os.path import join

import click
import requests
import yaml


def generate_one_metadata(link):
  """Generates metadata for a single video, from YouTube.

  Args:
    link: Link to YouTube video

  Returns:
    True if successful, returns false if not successful
  """
  if link:
    template = metadata_content_generator(link)
    if template:
      dst = click.prompt("Where would you like to save the data generated? ",
                         default=getcwd())
      if dst:
        if not exists(dst):
          makedirs(dst)
        write_file = open(join(dst, "metadata.yaml"), "w")
        write_file.write(template)
        return True
    else:
      click.echo("Error: Can't get metadata for this video, make sure the url"
                 "is correct")
      logging.error("Error: Can't get metadata for this video, make sure the "
                    "url is correct")
  else:
    click.echo("Error: No URL specified. Try Again!")
    logging.error("No URL specified. Try Again!")
    return False


def generate_video_metadata():
  """Generates metadata for each section of videos.

  Generates metadata for each section of videos, given a videos_url
  config file with YouTube URLs.

  Returns:
    False if there is an error , e.g. If meta data file is missing
  """
  try:
    with open("./config.yaml") as data_file:
      conf_data = yaml.load(data_file)
  except:
    click.echo(click.style("Oops! No root config.yaml file.  "
                           "Check config.yaml.example for an example and try"
                           "again.", fg="red"))
    logging.debug("Oops!  There is no configuration file.")
    return False

  src_dir = conf_data["source"]["main_path"]
  video_src = conf_data["source"]["video_source"] or "videos"

  for section, _, _ in walk(join(src_dir, video_src)):
    src_path = join(section, "videos_url.yaml")

    try:
      with open(src_path) as data_file:
        conf_data = yaml.load(data_file)
        metadata_path = join(section, "metadata")

        for url_obj in conf_data["urls"]:
          video_name = url_obj["video_name"]
          click.echo("Generating metadata for " + video_name + " video file...")
          url = url_obj["url"]
          template = metadata_content_generator(url)
          if template:
            if not isdir(metadata_path):
              makedirs(metadata_path)
            write_file = open(join(metadata_path, video_name +
                                   "_metadata.yaml"), "w")
            write_file.write(template)

          else:
            click.echo("Error: Can't get metadata for " + video_name + ".")
            logging.error("Error: Can't get metadata for " + video_name + ".")
    except:
      continue
  click.echo("Done.")


def metadata_content_generator(url):
  """Metadata generator helper for videos.

  Args:
    url: YouTube URL from which metadata will be pulled

  Returns:
    String containing Title, Author name, description and Thumbnail URL
  """
  link = "http://www.youtube.com/oembed?url=" + url + "&format=json"
  res = requests.get(link)
  if res.status_code is not 200:
    return False
  metadata = res.json()
  title = metadata["title"]
  author_name = metadata["author_name"]
  author_url = metadata["author_url"]
  thumbnail_url = metadata["thumbnail_url"]
  sub_title = "( " + author_name + " )"
  description = ("Watch the Official on " + author_url + ". Author"
                 " Name: " + author_name)

  title_string = "---\n"+ "  title: '" + title + "'"
  sub_title_string = "\n  sub_title: '" + sub_title + "'"
  description_string = "\n  description: '" + description + "'"
  thumbnail_string = "\n  thumbnail_url: '" + thumbnail_url + "'"
  return title_string + sub_title_string + description_string + thumbnail_string
