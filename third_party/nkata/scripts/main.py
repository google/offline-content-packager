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

"""Offline content.
"""
import logging

from .analyze import analyze_content
from .bundle import compile_sections
from .bundle import compile_videos
import click
from .convert import makeiso
from .convert import makezip
from scripts.utils import check_platform
from scripts.utils import generate_one_metadata
from scripts.utils import generate_video_metadata


FORMAT = "[%(asctime)s] %(levelname)s: %(message)s"
DATEFMT = "%m/%d/%Y %I:%M:%S %p"
logging.basicConfig(format=FORMAT, datefmt=DATEFMT, filename="nkata.log",
                    level=logging.DEBUG)


@click.group()
def cli():
  """Offline Content Packaging tool.
  """
  pass


@click.command(help="Process files to an archive")
@click.option("--size", "-s", help="Maximum size in (MB)")
@click.option("--formt", "-f", help="Converts to (zip/iso/zipiso) format")
@click.option("-v", "--verbose", is_flag=True, help="Enables verbose mode")
def bundle(verbose, size=None, formt=None):
  """Bundle content.

  Bundle content from source directory specified
  in the config, process and save in destination
  directory specified.
  """
  if verbose:
    console = logging.StreamHandler()
    formatter = logging.Formatter("%(name)-4s: %(levelname)-8s %(message)s")
    console.setFormatter(formatter)
    logging.getLogger("").addHandler(console)

  check_platform()
  compile_sections()

  if formt and formt.lower() == "iso":
    makeiso(size)
  elif formt and formt.lower() == "zip":
    makezip(size)
  elif formt and formt.lower() == "zipiso":
    makezip(size)
    makeiso(size)


@click.command(help="Bundle only video file(s)")
@click.option("--size", "-s", help="Maximum size in (MB)")
@click.option("--formt", "-f", help="Converts to (iso) format")
@click.option("-v", "--verbose", is_flag=True, help="Enables verbose mode")
def bundle_videos(verbose, size=None, formt=None):
  """Bundle only video content.

  Bundle only video content from source directory specified
  in the config, process and saved in destination
  directory specified.

  Args:
    verbose: Run in verbose mode
    size: size of ISO files to generate
    formt: ZIP or ISO format
  """
  if verbose:
    console = logging.StreamHandler()
    formatter = logging.Formatter("%(name)-4s: %(levelname)-8s %(message)s")
    console.setFormatter(formatter)
    logging.getLogger("").addHandler(console)

  check_platform()
  compile_videos()

  if formt and formt.lower() == "iso":
    makeiso(size)


@click.command(help="Generate title, author, and thumbnail for YouTube videos")
@click.option("--typ", "-t", help="Specify type: 'single' for a single file,"
              " 'auto' to get URLs from videos_url.yaml")
def generate(typ):
  """Generate video metadata from YouTube API.

  Args:
    typ: Indicates if it is processing a directory or generating for
         a single file. Can be "single" or "auto"

  Returns:
         False if wrong type is specified
  """
  if typ == "single":
    url = click.prompt("Enter the Youtube video link")
    w(url)

  elif typ == "auto":
    generate_video_metadata()

  else:
    click.echo("Error: wrong type specified.")
    logging.error("Wrong type specified for generate command.")
    return False


@click.command(help="Shows the application logs")
def log():
  """Log history on the terminal.
  """
  for line in open("nkata.log").readlines():
    click.echo(line.rstrip())


@click.command(help="Package output files into a zip or ISO file. ")
@click.option("--size", "-s", help="Maximum size of storage medium in (MB)")
@click.option("--formt", "-f", help=
              "Valid options are 'zip', 'iso', or 'zipiso'.", default="zipiso")
def convert(formt, size=None):
  """Convert bundled content to either Zip or ISO.

  Args:
    formt: the format of the resulting file can be "zip" or "iso"
    size: Maximum size of resulting file in MB
  """
  if formt.lower() == "iso":
    makeiso(size)
  elif formt.lower() == "zip":
    makezip(size)
  else:
    makezip(size)
    makeiso(size)


@click.command(help="Calculate the number of discs needed to copy"
               " content / memory needed")
@click.option("--size", "-s", help="Maximum size in (MB)")
def analyze(size=None):
  """Analyze content.

  Analyze content. Gets information on the
  total size of the content, and suitable storage medium.

  Args:
    size: Size of intended storage medium
  """
  analyze_content(size)


cli.add_command(bundle)
cli.add_command(bundle_videos)
cli.add_command(generate)
cli.add_command(convert)
cli.add_command(log)
cli.add_command(analyze)
