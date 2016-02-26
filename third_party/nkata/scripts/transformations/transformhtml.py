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

"""HtmlTransformation script.
"""


import re
import uuid

try:
  from urllib import urlencode
except ImportError:
  from urllib.parse import urlencode

from bs4 import BeautifulSoup


class HtmlTransformation(object):
  """Copy HTML files and insert information header and a tracking code.
  """

  def __init__(self, **kwargs):
    """Instance varaibles.

    Args:
      **kwargs: Keyword arguments (color:external link color ,
              link:online link, code:tracking code)
    """
    self.link_color = kwargs["color"]
    self.online_link = kwargs["link"]
    self.tracking_code = kwargs["code"]

    self.header_html = str(self._create_header())

    flags = re.DOTALL | re.IGNORECASE
    self.link_re = re.compile(r'<a([^>]+href=[\'"]https?://.*?)>.*?</a\s*>',
                              flags=flags)
    self.link_target_re = re.compile(r"target\s*=['\"].+?['\"]", flags=flags)
    self.link_style_re = re.compile(r"style\s*=['\"](.+?)['\"]", flags=flags)

  def _create_tracking_tag(self, dst):
    """Creates tracking tag('<img src="tracking_img_src">').

    Args:
      dst: Path to page being viewed/tracked

    Returns:
      HTML img tag with tracking code
    """
    if not self.tracking_code:
      return None

    img_url_attr = {"v": "1", "t": "pageview", "ec": "page",
                    "ea": "open", "cm": "site"}
    img_url_attr["cs"] = "offlinedevsite"
    img_url_attr["cn"] = "OfflineDevContent"
    img_url_attr["tid"] = self.tracking_code
    img_url_attr["dp"] = dst
    img_url_attr["cid"] = str(int(uuid.uuid1().int>>96)) + "." + str(
        int(uuid.uuid1().int>>96))
    img_src = ("http://www.google-analytics.com/collect?" +
               urlencode(img_url_attr))

    tracking_img_tag = '<img src="' + img_src + '">'
    return tracking_img_tag

  def _create_header(self):
    """Creates header tag for html.

    Returns:
      BeautifulSoup object of HTML header
    """
    info_header = open("templates/html_header.html", "r").read()
    soup = BeautifulSoup(info_header)

    # add online link for each html page if specified
    if self.online_link:
      template_link = soup.find("a", {"class": "abcde"})
      template_link["href"] = self.online_link

    return soup

  def applies(self, src):
    """Check out for only html document.

    Args:
      src: path to file
    Returns:
      True if file name ends with ".html"

    """
    return src.endswith(".html")

  def apply(self, src, dst, finaldst, metadata, video):
    """Apply transformation.

    Args:
      src: path to input file
      dst: destination path
      finaldst: Final destination path
      metadata: File meta data
      video: Path to video file
    """
    video_data = finaldst, metadata, video
    html = open(src, "r").read()
    html = self.transform(html, dst) or html
    with open(dst, "w") as out_file:
      out_file.write(html)

  def transform(self, html, dst):
    """Transform method.

    Args:
      html: BeautifulSoup html object
      dst: Path to output destination
    """
    # change link color and target
    l_color = self.link_color or "green"

    def transform_link(value):
      """Transforms link.

      Args:
        value: value

      Returns:
        Transformed link
      """
      attr_append = ""
      link, attr = value.group(0), value.group(1)

      attr_new = attr

      # rewrite target attribute or add a new attribute
      attr_new, count = re.subn(
          self.link_target_re, "target='_blank'", attr_new)
      if count == 0:
        attr_append += " target='_blank' "

      # append to style attribute or add a new attribute
      attr_new, count = re.subn(
          self.link_style_re, r"style='\1; color: %s'" % l_color, attr_new)
      if count == 0:
        attr_append += " style='color: %s' " % l_color

      return link.replace(attr, attr_new + attr_append)

    # find all external links, process them with transform_link
    html = re.sub(self.link_re, transform_link, html)

    # add tracking script and header to page top
    flags = re.DOTALL | re.IGNORECASE
    html = re.sub(r"(<body[^>]*>)",
                  r"\1%s" % self.header_html, html, flags=flags)
    tracking_tag = str(self._create_tracking_tag(dst))
    html = re.sub(r"(</body[^>]*>)", r"%s\1" % tracking_tag, html, flags=flags)

    return html
