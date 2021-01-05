# RBJAS Rule Based Json Api Server

## SARFS Api Server

[SAFRS: Python OpenAPI & JSON:API Framework](https://github.com/thomaxxl/safrs)

SAFRS is an acronym for SqlAlchemy Flask-Restful Swagger. The purpose of this framework is to help python developers create a self-documenting JSON API for sqlalchemy database objects and relationships. These objects can be serialized to JSON and can be created, retrieved, updated and deleted through the JSON API. Optionally, custom resource object methods can be exposed and invoked using JSON. Class and method descriptions and examples can be provided in yaml syntax in the code comments. The description is parsed and shown in the swagger web interface. The result is an easy-to-use swagger/OpenAPI and JSON:API compliant API implementation

## LogicBank

[Transaction Rules for SQLAlchemy Object Models](https://github.com/valhuber/logicbank)

Use Logic Bank to govern SQLAlchemy update transaction logic - multi-table derivations, constraints, and actions such as sending mail or messages. Logic consists of _both:_

*   **Rules - 40X** more concise using a spreadsheet-like paradigm, and

*   **Python - control and extensibility,** using standard tools and techniques

Logic Bank is based on SQLAlchemy - it handles `before_flush` events to enforce your logic.

## Ceckit Out

[Open API (Swagger)](/api)

[Quick Admin](/admin)

## installation / execution
copy EXAMPLE.env to .env and adjust
pip install -r requirements.txt
run run_this_app.py

for SAFRS you may need the current HEAD