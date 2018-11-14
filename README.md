Get started
---------------

✨
`paynowzw` API for Humans
This framework provides the interface to the <a href="http://www.paynow.co.zw">Paynow Zimbabwe</a>Payment Gateway system



Installation
---------------

-  `$ pip install paynowzw`

Or through the recent pipenv

-  `$ pipenv  install paynowzw`

`paynowzw` requires the following dependencies

- requests library by Kenneth Reitz
- urllib.parse library


Usage
---------------

`from paynowzw import Paynow`
```
PAYNOW_ID = 'xyz'
PAYNOW_KEY = '24234jsdhfs'
RETURN_URL = 'http://www.test.co.zw/return_url'
RESULT_URL = 'http://www.test.co.zw/result_url'

# create new paynow object
paynow = paynowzw.Paynow(PAYNOW_ID, PAYNOW_KEY, RETURN_URL, RESULT_URL)

The above method is for web based payments. It does not require
the 'authemail' and 'phone' values. This however differs with
mobile based payments. For mobile just declare as shown below

paynow = Paynow('id12344','key1234',
                'www.example.com/return_url',
                'www.example.com/result_url',
                 authemail='example@example.com',
                 phone='0777XXXX')

2nd Step
# send payment to Paynow with reference as str
paynow.send_payment('reference', {'honey':23.345})

or

# create a dictionary of products
products = {'honey':2.34,'sugar':2.33}
response = paynow.send_payment('reference', products)

#check payment status
if response['Status'] == 'Ok':
....# do stuff

Status maybe 'Error' if the payment fails

#Use this method to poll status updates about a payment
poll_status = paynow.status_update()
```


To Do
-----
- Documentation ,Documentation just felt lazy :)
- Create example with a web framework mainly flask
- Create a Flask extension
- Tests for all defined methods
- Refactoring


-   Tests via `$ python3 tests.py`

Pull requests are encouraged!


License
-------
MIT License

Copyright (c) 2018 bevenfx. However this is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any means.

Just acknowledge my work

✨🍰✨


