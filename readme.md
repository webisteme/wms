# Warehouse Management System (Prototype)

## About

- Author: Eli Gothill
- Date: 17.02.2019
- Version: 0.1

## Description

* This is a prototype *Warehouse Management System* (WMS) implementation. It provides a public API with CRUD methods for orders, order lists, SKUs and storages; it also exposes a fulfillment endpoint for instructions on how to fulfill an order based on available storage. (See `assignment.md` for the full brief).

## Dependencies

- Python 3.7
- Django 2.1.7
- Django Rest Framework 3.9.1

## Setup

- Install dependencies

`pip install -r requirements.txt`

- Migrate database

`python wms/manage.py migrate`

- Run tests

`python wms/manage.py test api`

- Run server on port 8000:

`python wms/manage.py runserver`

## API Usage

### Models API

The application provides a public REST API for managing orders, order lines, SKUs and storage. No authorization is required. Four main API endpoints are provided for the models (see `wms/models.py` for model defintiions):

- /api/order/
- /api/orderline/
- /api/sku/
- /api/storage/

Each endpoint accepts the standard CRUD operations via HTTP (POST, GET, PUT, DELETE). Refer to `wms/tests.py` for example requests of every operation at each endpoint.

Note: trailing slashes are required.

### Fulfillment API

The application's core service is the fulfilment API, which is responsible for providing instuctions on how to fulfill an order based on the warehouse storage state. For a list of order lines, an ordered list of picks is returned, where each pick references a quantity and storage ID. The storages used are ordered based on stock, with the storages with the least stock used first. An order for an SKU may therefore span multiple storages.

The fulfilment API is available at

- /api/fulfillment/

It accepts only POST requests. The body of the request should structured as in the following example: `{lines: [{sku: 1, quantity: 2}, {sku: 2, quantity: 7}]}`.

Note: trailing slashes are required.

### Order Search API

It's also possible to search for orders by `customer_name` at the `/api/order/` endpoint. The following search syntax is supported: `/api/order/?q=query` where `query` is the search term to match against the order `customer_name`.

Search is case-insensitive and ASCII characters will match with their non-ASCII equivalents (e.g. you can search 'Muller' to find 'Müller') but not the other way round (e.g. searching for 'Jönes' will not return 'Jones').

## Ideas for improvement

- Implement soft delete by overriding DRF's delete methods
- Make CRUD API and fulfilment interfaces more consistent
- Return more granular error code and message when find_picks() fails