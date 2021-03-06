from decimal import Decimal, localcontext
import requests, hashlib
from six.moves.urllib_parse import quote_plus, parse_qs


class Paynow(object):
    """Instantiates the Paynow Object"""

    WEB_URL: str = "https://www.paynow.co.zw/interface/initiatetransaction"
    MOBILE_URL: str = "https://www.paynow.co.zw/interface/remotetransaction"

    def __init__(
        self,
        pid: str = "",
        pkey: str = "",
        returnurl: str = "",
        resulturl: str = "",
        authemail: str = "",
        phone: str = None,
    ):

        self.pid = pid
        self.pkey = pkey
        self.returnurl = returnurl
        self.resulturl = resulturl
        self.authemail = authemail
        self.phone = phone
        self.reference = ""
        self.products: dict = {}
        self.frompaynow: dict = {}
        self.method: str = "ecocash"

    def set_response_from_paynow(self, resp) -> dict:
        """ Setter for response from Paynow """

        self.frompaynow = self.decrypt(resp)
        return self.frompaynow

    def total(self) -> float:
        """ calculate the total of products in cart to two decimal point """

        with localcontext() as ctx:
            ctx.prec = 2
        amount = sum(value for value in self.products.values())
        if amount <= 1:
            raise ValueError("Payments less than $1 are disallowed!")
        return float(Decimal(amount).quantize(Decimal(".00")))

    def send_payment(self, reference, products) -> dict:
        """ Sends the transaction to Paynow"""

        data = self.build_request(reference, products)
        try:
            if data["method"]:  # for mobile payments
                return self.set_response_from_paynow(
                    requests.post(self.MOBILE_URL, data=data)
                )

            # URL that handles web payments
            return self.set_response_from_paynow(requests.post(self.WEB_URL, data=data))
        except Exception as e:
            raise e

    def status_update(self):
        pollurl = self.frompaynow.get("pollurl", "")
        data = requests.post(pollurl) if pollurl else ""
        try:
            return self.decrypt(data)
        except Exception:
            pass
        return data

    def encrypt(self, data) -> str:
        message = ""
        for key, value in data.items():
            if str(key).lower() == "hash":
                continue

            message += str(value)
        message += self.pkey
        return hashlib.sha512(message.encode("utf-8")).hexdigest().upper()

    def decrypt(self, data) -> dict:
        # TODO check functionality here
        try:
            data = parse_qs(data.text)
        except Exception as e:
            print(e)

    def build_request(self, reference, products):
        """ Build the required post object for Paynow API"""

        self.reference = reference
        for key, amount in products.items():
            self.products[key] = float(amount)

        body = {
            "id": self.pid,
            "reference": self.reference,
            "amount": self.total(),
            "additionalinfo": "xyz",
            "returnurl": self.returnurl,
            "resulturl": self.resulturl,
            "authemail": self.authemail,
            "phone": self.phone,
            "method": self.method,
            "Status": "Message",
        }

        for key, value in body.items():
            if key == "authemail":
                continue

            body[key] = quote_plus(str(value))

        body["Hash"] = self.encrypt(body)
        return body
