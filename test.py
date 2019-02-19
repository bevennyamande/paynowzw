#! /usr/bin/env python

import unittest
import paynowzw

class PaynowTestCase(unittest.TestCase):
    def setUp(self):
        self.paynow = paynowzw.Paynow(pid='123', pkey='122', returnurl='www',
                         resulturl='weew', email='wew', phone='wew')

    def test_send_payment(self):
        pass

    def test_total(self):
        pass

    def test_set_response_from_paynow(self):
        pass

    def test_cipher(self):
        pass

    def test_status_update(self):
        pass

    def test_poll_update(self):
        pass
    
    def test_build_request(self):
        pass


if __name__ == "__main__":
    unittest.main()
