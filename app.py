import paynowzw
from flask import Flask

app = Flask(__name__)

paynow = paynowzw.Paynow(pid='10293',
                pkey='0eadc675-aedb-42ab-9aad-3185061fd842',
                returnurl='/return',
                resulturl='/result',
                email='wasp00007@gmail.com')

@app.route('/')
def index():
    products = { 'honey':2.00, 'sugar':3.00 }
    paynow.send_payment('items bought', products)
    import pdb;pdb.set_trace()
    return 'Make payment here'


if __name__ == '__main__':
    app.run(debug=True)
