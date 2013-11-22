#!/usr/bin/env python
# -*- coding: utf-8 -*-
import gc

import mock
import time

from garbage import GarbageCollector


class TestGarbageCollector(object):

	def test_garbage_collector_thread(self):
		assert gc.isenabled()

		collector = GarbageCollector()

		# don't sleep,
		with mock.patch.object(collector, 'timer'):
			with mock.patch('gc.collect') as collect:
				with collector.gc_disabled():
					assert not gc.isenabled()
					# FIXME: this is a little flakey
					time.sleep(0.05)
					assert collect.called

		assert gc.isenabled()

