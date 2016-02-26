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
from os.path import join
import shutil
import tempfile
import unittest

from scripts.utils import get_sections
from scripts.verifyconfig import verify_section_config


class VerifySectionConfigTest(unittest.TestCase):

  def setUp(self):
    self.dirpath = tempfile.mkdtemp()
    makedirs(join(self.dirpath, "docs"))
    makedirs(join(self.dirpath, "sdk"))
    makedirs(join(self.dirpath, "tutorial"))
    makedirs(join(self.dirpath, "videos"))
    self.video_src = join(self.dirpath, "videos")
    self.sections = get_sections(self.dirpath, [self.video_src])

  def tearDown(self):
    shutil.rmtree(self.dirpath)

  def test_verify_section_config_case1(self):

    """All the sections don't have configuration file.
    """
    with self.assertRaises(SystemExit) as cm:
      verify_section_config(self.dirpath, self.sections, self.video_src)
    self.assertEqual(cm.exception.code, 1)

  def test_verify_section_config_case2(self):

    """Some sections have configuration file, some don't have.
    """
    open(join(self.dirpath, "docs", "section_config.yaml"), "w")
    open(join(self.dirpath, "sdk", "section_config.yaml"), "w")

    with self.assertRaises(SystemExit) as cm:
      verify_section_config(self.dirpath, self.sections, self.video_src)
    self.assertEqual(cm.exception.code, 1)

  def test_verify_section_config_case3(self):
    """All the sections have configuration file.
    """
    open(join(self.dirpath, "docs", "section_config.yaml"), "w")
    open(join(self.dirpath, "sdk", "section_config.yaml"), "w")
    open(join(self.dirpath, "tutorial", "section_config.yaml"), "w")

    try:
      verify_section_config(self.dirpath, self.sections, self.video_src)
    except:
      self.assertTrue(False)

if __name__ == "__main__":
  unittest.main()
