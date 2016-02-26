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
from os.path import isdir
from os.path import join
import shutil
import tempfile
import unittest

import jinja2
from scripts.transformations import VideoTransformation
import yaml


class VideoTestCase(unittest.TestCase):

  def setUp(self):
    self.src_dir = tempfile.mkdtemp()
    self.dst_dir = tempfile.mkdtemp()

    self.tracking_code = "123456"
    self.video_subtitle = "test subtitle"
    self.video_summary = "test summary"
    self.video_name = "test_video"
    self.setUpMetadata()

    self.JINJA_ENVIRONMENT = jinja2.Environment(
        loader=jinja2.FileSystemLoader(self.src_dir),
        extensions=["jinja2.ext.autoescape"],
        autoescape=False)

  def setUpTemplate(self, template, content):
    template = join(self.src_dir, template)
    template_dir = dirname(template)
    if not isdir(template_dir):
      makedirs(template_dir)

    with open(template, "w") as f:
      f.write(content)

  def setUpMetadata(self):
    self.meta_data_content = {
        "title": "test video",
        "description": "test description",
        "sub_title": "test subtitle",
        "tags": "",
        "image_src": ""
    }
    self.metadata_file = join(self.src_dir, "video.yaml")
    f = open(self.metadata_file, "w")
    yaml.dump(self.meta_data_content, f)
    self.meta_data = {self.video_name: self.metadata_file}

  def createInstance(self):
    return VideoTransformation(self.tracking_code, self.JINJA_ENVIRONMENT)

  def tearDown(self):
    shutil.rmtree(self.src_dir)
    shutil.rmtree(self.dst_dir)

  def test_generate_html(self):
    html_name = "test_output.html"
    video_source = "/test/file/path/video_source.avi"
    video_type = "video/test"
    video_info = ("video_title", "video_subtitle", "video_description")

    template_content = ("{{ video_name }} / {{ video_type}} /"
                        " {{ video_source }} / {{ tracking_code }}")
    expected_output = "%s / %s / %s / %s" % (self.video_name, video_type,
                                             video_source, self.tracking_code)
    self.setUpTemplate("templates/video.html", template_content)

    transformation = self.createInstance()
    video_detail = (self.video_name, video_source, video_type, video_info)
    transformation.generate_html(self.dst_dir, html_name, video_detail, None)

    # assert the output
    with open(join(self.dst_dir, "html_files", html_name), "r") as f:
      output = f.read()

    self.assertEquals(output, expected_output)


if __name__ == "__main__":
  unittest.main()
