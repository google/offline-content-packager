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

"""File utility copy files from source directory to destination directory.
"""
from os import makedirs
from os import walk
from os.path import exists
from os.path import isdir
from os.path import isfile
from os.path import join
import shutil
import tempfile

from .progressbar import ProgressBar


def copy_with_transformations(itemsrc, itemdst, transformations,
                              metadata, video_src):

  """Copy file while running transformations.

  Copy file from itemsrc to itemdst running one or multiple transformations
  Transformations are working on paths, not on content so we can transform
  large files.

  Args:
    itemsrc: Source path for file to be copied
    itemdst: Destination path for file to be copied
    transformations: Transformations to be carried out on file
    metadata: Metadata for transformations to be applied
    video_src: Source path for video content
  """

  # filter only transformations that should apply to itemsrc file path
  valid_transformations = [t for t in transformations if t.applies(itemsrc)]

  if valid_transformations:
    inpath = itemsrc

    # run all but the last of the valid transformations
    for transformation in valid_transformations[:-1]:
      temp = tempfile.NamedTemporaryFile()
      transformation.apply(inpath, temp.name, itemdst, video_src)
      inpath = temp.name

    # run the last transformation, with the final destination
    final_transformation = valid_transformations[-1]
    final_transformation.apply(inpath, itemdst, itemdst, metadata, video_src)

  else:
    shutil.copy2(itemsrc, itemdst)


def copy_files(paths, section, transformations, metadata=None, video_src=None):
  """Walks through source directory and calls copy_with_transformations.

  Args:
    paths: tuple containing src_dir and dst_dir
    section: Object representing section being processed
    transformations: List of Transformations to be applied to section
    metadata: Metadata to be used for transformations
    video_src: Source path for video content
  """
  src_dir, dst_dir = paths
  num_files = count_files(src_dir)
  print
  progress = ProgressBar("Copying files from " + section + "...")

  num_copied = 0
  if isfile(src_dir) and not src_dir.endswith(".yaml"):
    copy_with_transformations(src_dir, dst_dir, transformations, metadata,
                              video_src)
  else:
    for srcpath, _, filenames in walk(src_dir):

      if srcpath.endswith("metadata"):
        continue
      relpath = srcpath[len(src_dir)+1:]
      dstpath = join(dst_dir, relpath)

      if not exists(dstpath):
        makedirs(dstpath)
      for name in filenames:
        if name.endswith(".yaml") or name.startswith("."):
          continue
        itemsrc = join(srcpath, name)
        itemdst = join(dstpath, name)
        copy_with_transformations(itemsrc, itemdst, transformations, metadata,
                                  video_src)
        num_copied += 1
        progress.calculate_update(num_copied, num_files)


def count_files(directory):
  """Counts total number of files in a particular directory.

  Args:
    directory: Directory containing files to be counted

  Returns:
    Number of files in directory
  """
  files = []
  if isdir(directory):
    for path, _, filenames in walk(directory):
      if path.endswith("metadata"):
        continue
      for name in filenames:
        if name.endswith(".yaml") or name.startswith("."):
          continue
        files.append(name)

  return len(files)
