#!/usr/bin/python2.4
#
# Copyright 2010 Google Inc. All Rights Reserved.

"""Discovery document tests

Functional tests that verify we can retrieve data from existing services.

These tests are read-only in order to ensure they're repeatable. They also
only work with publicly visible data in order to avoid dealing with OAuth.
"""

__author__ = 'ade@google.com (Ade Oshineye)'

from apiclient.discovery import build
import logging
import unittest

class BuzzFunctionalTest(unittest.TestCase):
  def test_can_get_buzz_activities_with_many_params(self):
    buzz = build('buzz', 'v1')
    max_results = 2
    actcol = buzz.activities()
    activities = actcol.list(userId='googlebuzz', scope='@self',
                             max_comments=max_results*2 ,max_liked=max_results*3,
                             max_results=max_results).execute()
    activity_count = len(activities['items'])
    self.assertEquals(max_results, activity_count)

    activities = actcol.list_next(activities).execute()
    activity_count = len(activities['items'])
    self.assertEquals(max_results, activity_count)

  def test_can_page_through_users_activities(self):
    buzz = build('buzz', 'v1')
    max_results = 2
    actcol = buzz.activities()
    
    activities = actcol.list(userId='adewale', scope='@self',
                             max_results=max_results).execute()
    for count in range(10):
      activities = actcol.list_next(activities).execute()
      activity_count = len(activities['items'])
      self.assertEquals(max_results, activity_count, 'Failed after %s pages' % str(count))

if __name__ == '__main__':
  unittest.main()
