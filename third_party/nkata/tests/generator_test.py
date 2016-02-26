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

from scripts.utils import generate_one_metadata


class GeneratorTestCase(unittest.TestCase):

  def test_without_youtube_link(self):
    """Should return False if url is not specified.
    """
    value = generate_one_metadata("")
    self.assertEqual(value, False)

  def test_invalid_youtube_url(self):
    """Should return False if url specified is invalid.
    """
    url = ("https://www.youtube.com"
           "/watch\?v\=Ipl-rLRxOrs\&index\=56\&list\=PLsko1y3G")
    value = generate_one_metadata(url)
    self.assertEqual(value, None)


if __name__ == "__main__":
  unittest.main()
