from collections import namedtuple
from decimal import Decimal, localcontext
import hashlib, requests
try:
    from urllib.parse import unquote_plus
except:
    from urllib import unquote_plus


class Paynow(namedtuple('Paynow', ['pid', 'pkey' ,'returnurl', 
                                   'resulturl' ,'email' ,'phone'])):
    """Create a paynow object with the required fields stated in docs"""

    weburl = "https://www.paynow.co.zw/interface/initiatetransaction"
    mobileurl = "https://www.paynow.co.zw/interface/remotetransaction"
    products = from_paynw = {}
    reference = ''

    def set_response_from_paynow(self, response):
    	self.from_paynw = self.cipher(response, method='decrypt') if response else None
    	return self.from_paynw

    def total(self):
        """ Returns totals of all items in the cart as float to 2dp"""
        with localcontext() as ctx: ctx.prec = 2
        amt =  [self.products[key] for key in self.products.keys()]
        amt = sum(amt)
        if amt <= 1: raise ValueError('Payments less than 1$ are disallowed!')
        return float(Decimal(amt).quantize(Decimal('.00')))

    def send_payment(self, reference, products):
        data = self.build_request(reference, products)
        try:
            if data['authemail'] and data['phone']:
                if all([data['authemail'], data['phone']]):
                    # TODO put try except
                    return self.set_response_from_paynow(
                        requests.post(mobileurl, data=data))
            # URL that handles web payments
            return self.set_response_from_paynow(requests.post(
                                       weburl, data=data))
        except Exception as e:
            raise e

    def status_update(self):
        pollurl = self.from_paynw.get('pollurl', '')
        data = requests.post(pollurl) if pollurl else ''
        try:return self.cipher(data, method="decrypt")
        except Exception:pass
        return data

    def cipher(self, data, method=''):
        if method == "encrypt":
            msg = ''
            for key, value in data.items():
                    msg += str(value)
            msg += self.paynow_key.lower()
            return hashlib.sha512(msg.encode('utf-8')).hexdigest().upper()
        else:
            msg = {}
            # TODO find a proper method to strip tabs and newlines ie method
            try:
                data = unquote_plus(data.text).replace('\n','').replace('\t','').split('&')
                raw_list = [data[i].split('=')for i in range(len(data))]

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

    def build_request(self, reference, products):
        self.reference = reference
        # TODO ensure products is a dict and items follow the rule ie float
        products = products.items()
        for desc, amount in products:
            self.products[desc] = float(amount)
        body = {'id':self.paynow_id,'reference':self.reference,
        	    'amount':self._total(),'additionalinfo':'',
        	    'return_url':self.return_url,'result_url':self.result_url,
                'authemail':self.authemail,'phone':self._phone,
        	    'Status':'Message'
                }
        body['Hash'] = self.cipher(body,method="encrypt")
        return body