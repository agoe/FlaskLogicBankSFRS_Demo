#!/usr/bin/env python3
"""
  This demo application demonstrates the functionality of the safrs documented REST API
  When safrs is installed, you can run this app:
  $ python3 demo_relationship.py [Listener-IP]

  This will run the example on http://Listener-Ip:5000

  - An sqlite database is created and populated
  - A jsonapi rest API is created
  - Swagger documentation is generated
  - two simple rules created with LogicBank

"""
import sys

from flask import render_template
from safrs import ValidationError

import app as app

# address where the api will be hosted, change this if you're not running the app on localhost!
host = sys.argv[1] if sys.argv[
                      1:] else "localhost"  # 127.0.0.1 check in swagger or your lient what is used you wight need cors support
app = app.create_app()


@app.route('/')
def welcome():
    return render_template('index.html')


@app.errorhandler(ValidationError)
def handle_exception(e: ValidationError):

    res = {'code': e.status_code,
           'errorType': 'Validation Error',
           'errorMessage': e.message}
#    if debug:
#        res['errorMessage'] = e.message if hasattr(e, 'message') else f'{e}'

    return res, 400

@app.after_request
def after_request(response):
    """
    Enable CORS. Disable it if you don't need CORS or instal Cors Libaray
    https://parzibyte.me/blog
    """
    response.headers[
        "Access-Control-Allow-Origin"] = "*"  # <- You can change "*" for a domain for example "http://localhost"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE, PATCH"
    response.headers["Access-Control-Allow-Headers"] = \
        "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization"
    return response


if __name__ == "__main__":
    app.run(host=host, threaded=False)
