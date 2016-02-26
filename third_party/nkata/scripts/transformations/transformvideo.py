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

"""VideoTransformation script.
"""
import logging
from os import makedirs
from os.path import basename
from os.path import dirname
from os.path import exists
from os.path import isfile
from os.path import join
from os.path import split
from os.path import splitext
import shutil

import click
from scripts.utils.downloader import download_image
import yaml


class VideoTransformation(object):
  """Copys video files and transform them.
  """

  def __init__(self, tracking_code, jinjaenv):
    """Instance varaibles.

    Args:
      tracking_code: Analtics tracking code
      jinjaenv: Jinja environment variable

    """
    self.tracking_code = tracking_code
    self.jinjaenv = jinjaenv
    self.list_of_videos = list()
    self.new_list = list()
  EXTENSIONS = [".webm", ".mkv", ".flv" ".vob" ".ogv", ".drc", ".mng", ".avi",
                ".mov", ".qt", ".wmv", ".yuv", ".rm", ".rmvb", ".mp4", ".m4v",
                ".asf", ".mpg", ".mpeg", ".m2v", ".svi", ".3gp", ".3g2", ".mxf",
                ".roq", ".nsv"]

  def applies(self, src):  # pylint: disable=no-self-use
    """Checks video extension.

    Args:
      src: File path to check

    Returns:
      True if file extension is in applicable video extensions, False if it is
      not
    """
    _, extension = splitext(src)
    return extension in self.EXTENSIONS

  def apply(self, itemsrc, itemdst, finaldst, metadata, videos_src):
    """Transform each video.

    Args:
      itemsrc: File path to read video from
      itemdst: File path to write video to
      finaldst: Final file path to write video to
      metadata: Video metadata
      videos_src: Path to Videos folder
    """
    finaldst_dir, finaldst_name = dirname(finaldst), basename(finaldst)
    video_name, extension = splitext(finaldst_name)
    video_type = "video/%s" % extension[1:]
    html_name = "%s_%s.html" % (video_name, extension)
    finaldst_base, _ = split(finaldst)
    _, finaldst_base_path = split(finaldst_base)
    itemsrc_base, _ = split(itemsrc)

    if len(self.splitpath(finaldst)) - len(self.splitpath(videos_src)) > 2:
      video_source_path = join(finaldst_base_path, "html_files", html_name)
      back = "../../index.html"
      data_file = join(itemsrc_base, "metadata", video_name + "_metadata.yaml")
      try:
        with open(data_file) as data_file:
          conf_data = yaml.load(data_file)
          title = conf_data["title"]
          sub_title = conf_data["sub_title"]
          description = conf_data["description"]
          thumbnail_url = conf_data["thumbnail_url"]
          if thumbnail_url:
            image = download_image(thumbnail_url, finaldst_base, video_name)
            if image:
              image_path = join(finaldst_base_path, "images", image)
            else:
              image_path = ""
          else:
            image_path = ""
      except:
        title, sub_title, description, image_path = video_name, "", "", ""

    else:
      video_source_path = join("html_files", html_name)
      back = "../index.html"
      if metadata and isfile(metadata[video_name]):
        title, sub_title, description, thumbnail_url = self.process_meta_data(
            video_name, metadata)
        if thumbnail_url:
          image = download_image(thumbnail_url, finaldst_base, video_name)
          if image:
            image_path = join(".", "images", image)
          else:
            image_path = ""
        else:
          image_path = ""
      else:
        title, sub_title, description, image_path = video_name, "", "", ""

    video_info = (title, sub_title, description, image_path)
    video_source = join("..", video_name) + extension

    if len(title) > 50:
      title = title[0:45] + "..."

    if finaldst_base_path in self.new_list:
      self.list_of_videos.append((video_name, video_source_path, title,
                                  sub_title, image_path, None))
    else:
      self.new_list.append(finaldst_base_path)
      self.list_of_videos.append(("", "", "", "", "", finaldst_base_path))
      kwargs = (video_name, video_source_path, title, sub_title, image_path,
                None)
      self.list_of_videos.append(kwargs)

    # generate html page for video
    video_detail = (video_name, video_source, video_type, video_info)
    self.generate_html(finaldst_dir, html_name, video_detail, back)

    # copy videos
    shutil.copy2(itemsrc, itemdst)

  def process_meta_data(self, video_name, metadata):  # pylint: disable=no-self-use
    """Process metadata to return values in metadata.

    Args:
      video_name: Name of video
      metadata: Dictionary containing video metadata

    Returns:
      False if metadata does not exist or tupple containing title,
      sub_title, description, thumbnail_url if it does
    """
    if metadata[video_name]:
      data_file = metadata[video_name]

      try:
        with open(data_file) as data_file:
          conf_data = yaml.load(data_file)
      except:
        click.echo("\nOops!  There is no metadata for " + video_name +
                   ".  Try again...")
        logging.debug("\nOops!  There is no metadata for " + video_name + ".")
        return False

      title = conf_data["title"]
      sub_title = conf_data["sub_title"]
      description = conf_data["description"]
      thumbnail_url = conf_data["thumbnail_url"]

      return title, sub_title, description, thumbnail_url

  def generate_html(self, dst_path, html_name, video_detail, back):

    """Generate HTML file in destination path.

    Takes a destination path and writes a HTML file
    named dst_path/html_files/html_name using video_* arguments, tracking_code
    from the transformation instance, video specific metadata yaml file
    (if it is listed in the main config file), rendering it using JINJA object
    from html_template property.

    Args:
      dst_path: Path to which file is written
      html_name: Name of HTML file to read from
      video_detail: Video metadata
      back: Indicates whether to show back navigation link
    """
    video_name, video_source, video_type, video_info = video_detail
    if not exists(join(dst_path, "html_files")):
      makedirs(join(dst_path, "html_files"))

    write_file = open(join(dst_path, "html_files", html_name), "w")
    template_values = {
        "video_name": video_name,
        "video_type": video_type,
        "video_source": video_source,
        "tracking_code": self.tracking_code,
        "title": video_info[0],
        "sub_title": video_info[1],
        "description": video_info[2],
        "back": back
    }

    template = self.jinjaenv.get_template("templates/video.html")
    write_file.write(template.render(template_values))

  def generate_video_list_html(self, dst_dir, video_subtitle,
                               video_summary, path_to, template_pth=None):
    """Generate homepage for video sections.

    Generates homepage for each video sections, and list all videos
    in html file.

    Args:
      dst_dir: Directory to write file to
      video_subtitle: Name of the video
      video_summary: Text describing the video
      path_to: Determines if to display "Back To Home" link
      template_pth: Path to template

    """
    # if no videos, skip this
    if not self.list_of_videos:
      return

    write_file = open(join(dst_dir, "index.html"), "w")
    template_values = {
        "video_summary": video_summary,
        "video_subtitle": video_subtitle,
        "tracking_code": self.tracking_code,
        "list": self.list_of_videos,
        "division_back": path_to
    }
    if template_pth:
      template = self.jinjaenv.get_template(template_pth)
      write_file.write(template.render(template_values))
    else:
      template = self.jinjaenv.get_template("templates/videos_list.html")
    write_file.write(template.render(template_values))
    self.list_of_videos[:] = []

  def splitpath(self, path, maxdepth=20):
    """Splits path.

    Splits path i.e  path >> User/documents/source, its return
    [User, documents, source]

    Args:
      path: Path to split
      maxdepth: Maximum depth of path to split

    Returns:
      Array of path elements
    """
    (head, tail) = split(path)
    return self.splitpath(head, maxdepth - 1) + [tail] \
      if maxdepth and head and head != path \
      else [head or tail]
