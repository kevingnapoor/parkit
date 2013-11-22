#!/usr/bin/env python
# -*- coding: utf-8 -*-
import contextlib
import gc
import threading


class GarbageCollector(object):
	"""We see a small improvement by offloading gc during request handling."""

	def __init__(self):
		self.gc_thread = threading.Thread(target=self.collect)
		self.timer = threading.Condition()
		self.threaded = threading.Event()

	def __del__(self): # pragma: no cover
		self.stop()

	def start(self):
		gc.disable()
		self.threaded.set()
		self.gc_thread.start()

	def stop(self):
		self.threaded.clear()

		with self.timer:
			self.timer.notify()

		gc.enable()

	def collect(self):
		while self.threaded.is_set(): # pragma: no branch
			with self.timer:
				self.timer.wait(11)
			gc.collect()

	@contextlib.contextmanager
	def gc_disabled(self):
		self.start()
		try:
			yield
		finally:
			self.stop()
