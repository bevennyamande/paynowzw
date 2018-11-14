from decimal import Decimal, localcontext
import requests
import hashlib
from urllib.parse import unquote_plus

# TODO create a config file
URL_INIT_WEB = "https://www.paynow.co.zw/interface/initiatetransaction"
URL_INIT_MOBILE = "https://www.paynow.co.zw/interface/remotetransaction"

class Paynow(object):

    def __init__(self, paynow_id, paynow_key, return_url,
                       result_url,authemail=None, phone=None):
        self.paynow_id = paynow_id
        self.paynow_key = paynow_key
        self.return_url = return_url
        self.result_url = result_url
        self.authemail = authemail
        self._phone = phone
        self.products = {}
        self._from_paynw = {}
        self._reference = None

    def _set_response_from_paynow(self, response):
    	self._from_paynw = self._decrypt(response) if response else None
    	return self._from_paynw

    def _total(self):
        """ Returns totals of all items in the cart as float to 2dp"""
        with localcontext() as ctx: ctx.prec = 2
        amt =  [self.products[key] for key in self.products.keys()]
        amt = sum(amt)
        if amt <= 1: raise ValueError('Payments less than 1$ are disallowed!')
        return float(Decimal(amt).quantize(Decimal('.00')))

    def send_payment(self, reference, products):
        data = self._build_request(reference, products)
        try:
            if data['authemail'] and data['phone']:
                if all([data['authemail'], data['phone']]):
                    # TODO put try except
                    return self._set_response_from_paynow(
                        requests.post(URL_INIT_MOBILE, data=data))
            # URL that handles web payments
            return self._set_response_from_paynow(requests.post(
                                       URL_INIT_WEB, data=data))
        except Exception as e:
            raise e

    def status_update(self):
        pollurl = self._from_paynw.get('pollurl', '')
        data = requests.post(pollurl) if pollurl else ''
        try:return self._decrypt(data)
        except Exception:pass
        return data

    def _encrypt(self, data):
    	msg = ''
    	for key, value in data.items():
    		msg += str(value)
    	msg += self.paynow_key.lower()
    	return hashlib.sha512(msg.encode('utf-8')).hexdigest().upper()

    def _decrypt(self, resp):
        msg = {}
        # TODO find a proper method to strip tabs and newlines ie method
        try:
            resp = unquote_plus(resp.text).replace('\n','').replace('\t','').split('&')
            raw_list = [resp[i].split('=')for i in range(len(resp))]

            for i in range(len(raw_list)):
                if not len(raw_list[i]) > 2:
                    msg.update({raw_list[i][0]:raw_list[i][1]})
                else:
                    # TODO hpt to unpack 3 items to 2 vars
                    pollurl, url, url2 = raw_list[i]
                    msg.update({pollurl:url+url2})
            # TODO check the reponse object of an error msg
            # handle the error
            if not 'Hash' in msg.keys():
                raise ValueError('Paynow messages must have a hash!')
        except AttributeError:
            pass
        return msg

    def _build_request(self, reference, products):
        self._reference = reference
        # TODO ensure products is a dict and items follow the rule ie float
        products = products.items()
        for desc, amount in products:
            self.products[desc] = float(amount)
        body = {'id':self.paynow_id,'reference':self._reference,
        	    'amount':self._total(),'additionalinfo':'',
        	    'return_url':self.return_url,'result_url':self.result_url,
                'authemail':self.authemail,'phone':self._phone,
        	    'Status':'Message'
                }
        body['Hash'] = self._encrypt(body)
        return body
