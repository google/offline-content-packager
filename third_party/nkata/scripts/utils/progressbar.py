#!/usr/bin/python
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

# -*- coding: utf-8 -*-
"""ProgressBar Indicator script.
"""
import sys


class ProgressBar(object):
  """ProgressBar class.
  """

  def __init__(self, message, width=30, progress_symbol=u'# ',
               empty_symbol=u'. '):
    """Initial variables.

    Args:
      message: Message to display
      width: number of indicators to display
      progress_symbol: character to use for Indicator progress
      empty_symbol: character to use for empty part of progress indicator
    """
    self.width = width

    if self.width < 0:
      self.width = 0
    self.message = message
    self.progress_symbol = progress_symbol
    self.empty_symbol = empty_symbol

  def update(self, progress):
    """Updates ProgressBar.

    Args:
      progress: percentage progress (between 0 and 100)
    """
    total_blocks = self.width
    filled_blocks = int(round(progress / (100 / float(total_blocks))))
    empty_blocks = total_blocks - filled_blocks

    progress_bar = (self.progress_symbol * filled_blocks + self.empty_symbol *
                    empty_blocks)

    if not self.message:
      self.message = u''

    progress_message = u'\r{0} {1}  {2}%'.format(self.message, progress_bar,
                                                 progress)

    sys.stdout.write(progress_message)
    sys.stdout.flush()

  def calculate_update(self, done, total):
    """Calculates new ProgressBar.

    Args:
      done: amount done
      total: total amount
    """
    progress = int(round((done / float(total)) * 100))
    self.update(progress)
