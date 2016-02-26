#!/usr/bin/env python
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

"""Main bundling script for all content.
"""
from datetime import datetime
import logging
from os import getcwd
from os import makedirs
from os.path import basename
from os.path import exists
from os.path import isdir
from os.path import isfile
from os.path import join
from os.path import normpath
import shutil
import sys

import click
import jinja2
from scripts.transformations import HtmlTransformation
from scripts.transformations import VideoTransformation
from scripts.utils import bundle_content_section
from scripts.utils import bundle_video_section
from scripts.utils import get_divisions
from scripts.utils import get_sections
from .verifyconfig import readconfig
from .verifyconfig import verify_section_config
import yaml

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(getcwd()),
    extensions=["jinja2.ext.autoescape"],
    autoescape=True)

#pylint: disable=invalid-name
main_page_index = list()
division_process = list()
division_main_list = list()
page_index = []


def compile_sections():
  """Bundles each section except the videos directory.

  Returns:
    False if one of the paths in the config file does not exist
  """
  try:
    click.echo(
        click.style("\nReading and verifying configuration file...",
                    fg="green"))
    logging.info(
        "............................ Reading and verifying configuration file."
        )
    important_keys = ["division", "project_title", "project_subtitle",
                      "source.main_path", "source.video_source",
                      "destination.main_path",
                      "absolute_link_color", "tracking_code"]
    conf_data = readconfig(important_keys)
  except:
    click.echo("Error in main config file. That's in config.yaml,"
               "in the root directory of nkata. Fix, then try again."
               " Pull from the sample source directory if necessary.")
    return

  title = conf_data["project_title"]
  sub_title = conf_data["project_subtitle"]
  src_dir = conf_data["source"]["main_path"]
  video_src = conf_data["source"]["video_source"]
  dst = conf_data["destination"]["main_path"]
  link_color = conf_data["absolute_link_color"]
  tracking_code = conf_data["tracking_code"]
  folder_name = conf_data["output_folder_name"]
  if not folder_name:
    folder_name = "goc"
  config = {
      "title": title,
      "sub_title": sub_title,
      "tracking_code": tracking_code,
      "link_color": link_color
  }

  if conf_data["division"]:
    division_process.append(True)
    division_values = list(conf_data["division"].values())
    division_list = [item for sublist in division_values for item in sublist]
    division_main_list.extend(list(conf_data["division"].keys()))
    verify_section_config(src_dir, list(set(division_list)), video_src)

    for div in conf_data["division"]:

      dst_dir = join(dst, folder_name, div)
      if not isdir(dst_dir):
        makedirs(dst_dir)

      # get list of sections plus ignoring videos source
      if not exists(src_dir):
        message = ("\nError: Source Directory( " + src_dir +
                   " ) specified doesn't exist\n")
        click.echo(click.style(message, fg="red"))
        logging.error("Source Directory( " + src_dir +
                      " ) specified doesn't exist")
        return False

      sections = get_divisions(conf_data["division"][div], [video_src])
      kwargs = (page_index, div, None, sections[1])
      process_sections(src_dir, dst_dir, config, sections[0], kwargs)
      page_index[:] = list()
  else:
    division_process.append(False)
    dst_dir = join(dst, folder_name)
    if not isdir(dst_dir):
      makedirs(dst_dir)
    # get list of sections plus ignoring videos source
    if not exists(src_dir):
      message = ("\nError: Source Directory( " + src_dir +
                 " ) specified doesn't exist\n")
      click.echo(click.style(message, fg="red"))
      logging.debug("Source Directory( " +
                    src_dir + " ) specified doesn't exist")
      return False
    sections = get_sections(src_dir, [join(src_dir, video_src)])
    path_to = folder_name
    verify_section_config(src_dir, sections, video_src)
    kwargs = (main_page_index, path_to, "single", None)
    process_sections(src_dir, dst_dir, config, sections, kwargs)

  click.echo(click.style(".......... Finished!", fg="green"))
  logging.info(".............. Finished")


def process_sections(src_dir, dst_dir, config, sections, kwargs):
  """Process each section and calls generate_template.

  Args:
    src_dir: Source Directory
    dst_dir: Destination Directory
    config: Configuration data from yaml file
    sections: List of sections
    kwargs: List of arguments containing:
      Page index
      Path
      Type
      Division

  """
  page_index, path_to, typ, division = kwargs
  for section in sections:
    src_path = join(src_dir, section)
    dst_path = join(dst_dir, section)

    config_file_path = join(src_path, "section_config.yaml")
    if not isfile(src_path):
      try:
        with open(config_file_path) as data_file:
          config_data = yaml.load(data_file)
          title = config_data["title"]
          online_link = config_data["online_link"] or ""
          metadata = config_data["metadata"]
          page_index.append((section, path_to, title, metadata))
      except:
        message = ("Error in " + section +
                   " config file. Check sample and try again")
        click.echo(click.style(message, fg="red"))
        logging.debug("Oops!  There is no configuration file for " + section)
        sys.exit()

    else:
      online_link = None
    bundle_content_section(src_path, dst_path, section, config, online_link)

  if division:
    compile_videos(division, dst_dir, path_to)

  elif division is None:
    compile_videos()

  if not typ:
    generate_template(dst_dir, config["title"], config["sub_title"],
                      config["tracking_code"], page_index, None, True)


def process_video_sections(sections, folder_name, transformations,
                           video_transformation, kwargs):
  """Process video sections.

  Args:
    sections: List of sections to be processed
    folder_name: Name of the folder
    transformations: Transformations
    video_transformation: Video Transformation object
    kwargs: list of config data
  """
  (src_dir, dst_dir, video_src, title, sub_title,
   tracking_code, dst, path_to) = kwargs
  meta = list()
  division_meta = list()
  for section in sections:
    src_path = join(src_dir, video_src, section)
    dst_path = join(dst_dir, section)
    if not isfile(join(src_dir, video_src, section)):
      # read videos conf file
      try:
        with open(join(src_dir, video_src, section,
                       "section_config.yaml")) as video_file:
          config_data = yaml.load(video_file)
          video_subtitle = config_data["video_subtitle"]
          video_summary = config_data["video_summary"]
          metadata = config_data["metadata"]
          template_path = config_data["template_path"]
      except:
        click.echo(section + " video configuration file doesn't exist "
                   "or has an error. Using default values.")
        logging.debug(section + " video configuration file doesn't exist "
                      "or has an error. Using default values.")
        video_summary = section
        video_subtitle = ""
        template_path = None
        metadata = None

      # check if the template specified exists
      if template_path and not isfile(template_path):
        click.echo("Template specified for " + section +
                   " video(s) doesn't exist. "
                   "Using default template.")
        logging.debug("Template specified for " + section +
                      " video(s) doesn't exist. "
                      "Using default template.")
        template_path = None

      con = {
          "filename": section + "/index.html",
          "title": section
      }
      meta.append(con)
      division_meta.append(con)
      page_index.append((path_to, "", section + " videos", division_meta))
      division_meta = []
      paths = (src_path, dst_path)
      videos_path = join(src_dir, folder_name, video_src)
      bundle_video_section(paths, section, metadata,
                           transformations, videos_path)

      # generate individual pages for each video
      video_transformation.generate_video_list_html(dst_path, video_subtitle,
                                                    video_summary, path_to,
                                                    template_path)

  # generate video homepage with links to individual videos
  if division_process and division_process[0]:
    dst_folder = join(dst, folder_name)
    generate_template(dst_folder, title, "",
                      tracking_code, division_main_list, True)
  else:
    main_page_index.append((video_src, folder_name, video_src, meta))
    generate_template(join(dst, folder_name), title, sub_title,
                      tracking_code, main_page_index)


def compile_videos(division=None, div_dir=None, path_to=None):
  """Bundles only video content.

  Args:
    division: Division object
    div_dir: Division directory
    path_to: Path to division directory

  Returns:
    False if there is an exception
  """
  click.echo("Processing videos .....................................")

  try:
    with open("./config.yaml") as data_file:
      conf_data = yaml.load(data_file)
  except:
    message = ("Oops!  There is no configuration file."
               "  Check sample and try again...")
    click.echo(click.style(message, fg="red"))
    logging.debug("Oops!  There is no configuration file.")
    return False

  src_dir = conf_data["source"]["main_path"]
  video_src = conf_data["source"]["video_source"] or "videos"
  dst = conf_data["destination"]["main_path"]
  link_color = conf_data["absolute_link_color"]
  tracking_code = conf_data["tracking_code"]
  title = conf_data["project_title"]
  sub_title = conf_data["project_subtitle"]
  folder_name = conf_data["output_folder_name"]
  if not folder_name:
    folder_name = "goc"

  base_path = basename(normpath(video_src))
  dst_dir = join(dst, folder_name, base_path)
  if not exists(join(src_dir, video_src)):
    message = ("\nError: Video Source Directory( " + video_src +
               " ) specified doesn't exist\n")
    click.echo(click.style(message, fg="red"))
    logging.error("Video Source Directory( " + video_src +
                  " ) specified doesn't exist")
    return False

  # Initialising a list of transformations
  video_transformation = VideoTransformation(tracking_code, JINJA_ENVIRONMENT)
  transformations = list()
  transformations.append(HtmlTransformation(color=link_color,
                                            code=tracking_code, link=False))
  transformations.append(video_transformation)

  # copy videos
  sections = get_sections(join(src_dir, video_src),
                          join(src_dir, video_src, "metadata"))

  if not division:
    kwargs = (src_dir, dst_dir, video_src,
              title, sub_title, tracking_code, dst, path_to)
    process_video_sections(sections, folder_name,
                           transformations, video_transformation, kwargs)
  else:
    kwargs = (src_dir, div_dir, video_src,
              title, sub_title, tracking_code, dst, path_to)
    process_video_sections(division, folder_name,
                           transformations, video_transformation, kwargs)

  # copy video image(jpeg)
  if not isdir(join(dst, folder_name, "img")):
    makedirs(join(dst, folder_name, "img"))
  shutil.copy2("img/video_image.svg", join(dst, folder_name, "img"))

  # copy video image(jpeg)
  if not isdir(join(dst, folder_name, "img")):
    makedirs(join(dst, folder_name, "img"))
  shutil.copy2("img/back-arrow.svg", join(dst, folder_name, "img"))


def generate_template(dst_dir, title, sub_title, tracking_code,
                      page_index, division=None, back=None):
  """Generate homepage templates.

  Args:
    dst_dir: destination directory
    title: Page title
    sub_title: Short description of the page content
    tracking_code: Analytics tracking code
    page_index: Page index
    division: Division that this page belongs to
    back: Used to determine if navigation back link should be included
  """
  write_file = open(join(dst_dir, "index.html"), "w")
  created_at = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
  template_values = {
      "project_title": title,
      "project_subtitle": sub_title,
      "created_at": created_at,
      "tracking_code": tracking_code,
      "sections": page_index,
      "back": back
  }

  if not division:
    template = JINJA_ENVIRONMENT.get_template("templates/homepage.html")
  else:
    template = JINJA_ENVIRONMENT.get_template(
        "templates/division_homepage.html")

  write_file.write(template.render(template_values))
