
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

from os.path import dirname
from os.path import join
from os.path import realpath
import shutil
import tempfile
import unittest

from scripts.transformations import HtmlTransformation
from scripts.utils import copy_files


class CopyFileTest(unittest.TestCase):

  def setUp(self):
    self.src_dir = tempfile.mkdtemp()
    self.dst_dir = join(dirname(realpath(__file__)), "output")
    self.filename = "test_file.txt"
    outfile = open(join(self.src_dir, self.filename), "w")
    outfile.write("Mary had a little lamb.\n")
    outfile.close()

  def tearDown(self):
    shutil.rmtree(self.src_dir)
    shutil.rmtree(self.dst_dir)

  def test_copy_files(self):
    link_color = "blue"
    tracking_code = "##########"
    online_link = "www.xxx.com"
    section = "Books"
    html_transformation = HtmlTransformation(
        color=link_color, code=tracking_code, link=online_link)
    paths = self.src_dir, self.dst_dir
    copy_files(paths, section, [html_transformation])

    expected = "Mary had a little lamb.\n"
    result = open(join(self.dst_dir, self.filename)).read()
    self.assertEqual(result, expected)


if __name__ == "__main__":
  unittest.main()
