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

from os import makedirs
from os.path import dirname
from os.path import join
from os.path import realpath
import shutil
import tempfile
import unittest

from scripts.utils import bundle_content_section
from scripts.utils import get_sections


class GetSectionTest(unittest.TestCase):

  def setUp(self):
    self.dirpath = tempfile.mkdtemp()
    makedirs(join(self.dirpath, "docs"))
    makedirs(join(self.dirpath, "sdk"))
    makedirs(join(self.dirpath, "tutorial"))
    makedirs(join(self.dirpath, ".folder"))
    makedirs(join(self.dirpath, "videos"))

  def tearDown(self):
    shutil.rmtree(self.dirpath)

  def test_get_sections_without_ignore_path(self):
    """Test get_sections method without ignoring any path.


      get_sections should ignore the dirname that starts with '.'
      then return other dirname in the source directory
    """
    result = get_sections(self.dirpath, [])
    expected = ["docs", "sdk", "tutorial", "videos"]
    self.assertEqual(result, expected)

  def test_get_sections_with_ignore_path(self):
    """Test get_sections and ignore one path.

      get_sections should ignore the dirname that starts with '.'
      and plus the second argument path, then return others
    """
    videos_src = join(self.dirpath, "videos")
    result = get_sections(self.dirpath, videos_src)
    expect = ["docs", "sdk", "tutorial"]
    self.assertEqual(result, expect)

  def test_get_sections_with_ignore_two_paths(self):
    """Test get_sections and ignore two paths.

      get_sections should ignore the dirname that starts with '.'
      and plus the second argument path, then return others.
      Should ignore two dirpath
    """
    videos_src = join(self.dirpath, "videos")
    sdk_src = join(self.dirpath, "sdk")
    result = get_sections(self.dirpath, [videos_src, sdk_src])
    expect = ["docs", "tutorial"]
    self.assertEqual(result, expect)


if __name__ == "__main__":
  unittest.main()
