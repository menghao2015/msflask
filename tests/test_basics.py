import unittest
from flask import current_app
from myapp import create_app, db

class BasicsTestCase(unittest.TestCase):
	PRESERVE_CONTEXT_ON_EXCEPTION = False
	def setUp(self):
		self.apl = create_app('testing')
		self.apl_context = self.apl.app_context()
		self.apl_context.push()
		db.create_all()

	def teraDown(self):
		db.session.remove()
		db.drop_all()
		self.apl_context.pop()
	
	def test_app_exists(self):
		self.assertFalse(current_app is None)

	def test_app_is_testing(self):
		self.assertTrue(current_app.config['TESTING'])

