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

"""Zip conversion script.
"""
import logging
from os import walk
from os.path import isdir
from os.path import join
from os.path import normcase
from os.path import sep
from os.path import split
import zipfile

import click


def to_zip(dir_path=None, zip_file_path=None, include_dir_in_path=True,
           filelist=None):
  """Verify path, the calls trim_path method.

  Args:
    dir_path: Path to directory containing content to be zipped
    zip_file_path: Path to which Zipped file is to be written
    include_dir_in_path: Flag to indicate if the parent directory name should
                         be included in the zip file name
    filelist: :List of files to be included in the zip file

  Raises:
    OSError: if dirPath is invalid or does not point to a directory
  """
  if not zip_file_path:
    zip_file_path = dir_path + ".zip"
  if not isdir(dir_path):
    logging.error("dirPath argument must point to a directory. " + dir_path +
                  " does not.")
    raise OSError("dirPath argument must point to a directory. "
                  "'%s' does not." % dir_path)

  parent_dir, dir_to_zip = split(dir_path)

  # Little nested function to prepare the proper archive path
  def trim_path(path):
    """coverts to Zip format.

    Args:
      path: path to be trimmed

    Returns:
      Path to the zip archive
    """
    archive_path = path.replace(parent_dir, "", 1)
    if parent_dir:
      archive_path = archive_path.replace(sep, "", 1)
    if not include_dir_in_path:
      archive_path = archive_path.replace(dir_to_zip + sep, "", 1)
    return normcase(archive_path)

  if not filelist:
    filelist = []
    for (archive_dir_path, dir_names, file_names) in walk(dir_path):
      for file_name in file_names:
        filelist.append(join(archive_dir_path, file_name))

      # getting empty directories as well
      if not file_names and not dir_names:
        filelist.append(archive_dir_path)
  out_fil = zipfile.ZipFile(zip_file_path, "w",
                            compression=zipfile.ZIP_DEFLATED, allowZip64=True)

  for file_path in filelist:
    if isdir(file_path):
      zip_info = zipfile.ZipInfo(trim_path(file_path) + "/")
      out_fil.writestr(zip_info, "")
    else:
      out_fil.write(file_path, trim_path(file_path))

  out_fil.close()
  click.echo("Finished!")
