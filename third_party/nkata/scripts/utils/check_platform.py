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

"""Check compatibility for windows system.
"""
from sys import platform
from sys import version_info

import click


def check_platform():
  """Check the platform that script is running on.
  """
  if platform.startswith("win32") or platform.startswith("cygwin"):
    if version_info[0] < 3 and version_info[1] > 1:
      click.echo("Python version not supported, "
                 "Install python 3.x.x and try again")
