![Paynowzw Logo](./logo.png)

Simple python API wrapper for Paynow Zimbabwe Online Payment Gateway system.
Check official website for Paynow  [Paynow](http://www.paynow.co.zw)

## Installation

Installing paynowzw is as simple as following the steps belows


```python
pipenv install paynowzw
```


### Dependencies

* request library py [Kenneth Reitz](https://)
* urllib.parse library


## Tutorial

```python

from paynowzw import Paynow

paynow = Paynow()

# send payment to Paynow with reference as str
paynow.send_payment('reference', {'honey':23.345})

or

# create a dictionary of products
products = {'honey':2.34,'sugar':2.33}
response = paynow.send_payment('reference', products)

#check payment status
if response['Status'] == 'Ok':
....# do stuff
else:
    # do something else. status returned an 'Error' if the payment fails

#Use this method to poll status updates about a payment
poll_status = paynow.status_update()

```

## To Do

* Documentation ,Documentation just felt lazy :)
* Create example with a web framework mainly flask
* Create a Flask extension
* Create a test suite 
* Refactoring

### Pull requests are encouraged!


## License

MIT License

Copyright (c) 2018 bevenfx. However this is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any means.
