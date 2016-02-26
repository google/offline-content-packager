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

import unittest
from scripts.transformations import HtmlTransformation


class TestHtmlTransformHelpers(unittest.TestCase):

  def test__create_tracking_tag_empty(self):
    self.t = HtmlTransformation(color="green", code="",
                                link="www.google.com")
    result = self.t._create_tracking_tag("")
    self.assertEqual(result, None)

  def test__create_tracking_tag_valid(self):
    self.t = HtmlTransformation(color="green", code="<img src=''>",
                                link="www.google.com")
    result = self.t._create_tracking_tag("<img src=''>")
    self.assertIsNotNone(result)
    self.assertIn("<img", result)


class TestHtmlTransformPublic(unittest.TestCase):

  def setUp(self):
    self.t = HtmlTransformation(color="green", code="<img src=''>",
                                link="www.google.com")
    self.filename = "test_file.html"

  def test_transform_empty(self):
    result = self.t.transform("", self.filename)
    self.assertEquals(result, "")

  def test_transform_case1(self):
    """If there is no <body> and <a>.
    """

    html_in = "<html><div></div></html>"
    html_out = "<html><div></div></html>"
    result = self.t.transform(html_in, self.filename)
    self.assertEquals(result, html_out)

  def test_transform_case2(self):
    """If there is no <body> but there is <a>.
    """

    html_in = "<html><a href='http://'></a></html>"
    html_out = ("<html><a href='http://' target='_blank' "
                " style='color: green' ></a></html>")
    result = self.t.transform(html_in, self.filename)
    self.assertEquals(result, html_out)

  def test_transform_case3(self):
    """If there is no <body> and we have non-relative <a>.
    """

    html_in = "<html><a href='/homepage'></a></html>"
    html_out = "<html><a href='/homepage'></a></html>"
    result = self.t.transform(html_in, self.filename)
    self.assertEquals(result, html_out)

  def test_transform_case4(self):
    """If there is no <body> and we have non-relative <a> and a relative <a>.
    """

    html_in = "<html><a href='http://'></a><a href='/homepage'></a></html>"
    html_out = ("<html><a href='http://' target='_blank' "
                " style='color: green' ></a><a href='/homepage'></a></html>")
    result = self.t.transform(html_in, self.filename)
    self.assertEquals(result, html_out)

  def test_transform_case5(self):
    """If there is <body> and no <a> .
    """

    html_in = "<html><body></body></html>"
    result = self.t.transform(html_in, self.filename)
    self.assertIn("<img", result)

  def test_transform_case6(self):
    """If there is <body> and there is <a> .
    """

    html_in = "<html><body><a href='http://'></a></body></html>"
    result = self.t.transform(html_in, self.filename)
    self.assertIn("<img", result)
    self.assertIn("<a href='http://' target='_blank'  style='color: green' >",
                  result)

  def test_transform_tracking_insertion(self):
    result = self.t.transform("<html><body></body></html>", self.filename)
    self.assertNotEqual(self.t.tracking_code, result)


if __name__ == "__main__":
  unittest.main()
