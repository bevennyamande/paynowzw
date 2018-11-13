import unittest
from urllib.parse import unquote_plus
from paynowzw.core import Paynow


success = {
'Status': 'Ok', 'BrowserUrl': 'http://www.paynow.co.zw:7106/Payment/ConfirmPayment/1169',
'PollUrl': 'http://www.paynow.co.zw:7106/Interface/CheckPayment/?guid3cb27f4b-b3ef-4d1f-9178-5e5e62a43995',
'Hash': '8614C21DD93749339906DB35C51B06006B33DC8C192F40DFE2DB6549942C837C4452E1D1333DE9DB7814B278C8B9E3C34D1A76D2F937DEE57502336E0A071412'}
error = {'Status': 'Error', 'Error': 'Invalid amount field'}


class TestCase(unittest.TestCase):
	def setUp(self):
		self.products = {'honey':2.34} # dummy products
		self.paynow = Paynow('id12344','key1234', 'www.return.com','www.result.com')
		self.paynow_mobile = Paynow('id12344','key1234',
		                     'www.return.com',
		                     'www.result.com',
		                     authemail='bev@gmail.com',
		                     phone='077723742')
		self.paynow.send_payment('i dont have one', self.products)
		self.paynow_mobile.send_payment('i dont have one', self.products)

	def tearDown(self):
		pass

	def test_total(self):
		# having a problem here put 2.3444
		self.assertEqual(self.paynow._total(), 2.34)
		self.assertEqual(self.paynow_mobile._total(), 2.34)

	def test_send_payment(self):
		# check for web
		self.assertTrue(self.paynow.send_payment('sfsfsfs', self.products), error)
		# check for mobile
		self.assertTrue(self.paynow_mobile.send_payment('sfsfsfs', self.products), success)

	def test_status_update(self):
		pass

	def test_decrypt(self):
		pass


if __name__ == '__main__':
	unittest.main()
