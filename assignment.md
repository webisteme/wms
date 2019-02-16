# byrd backend developer task
## Brief
* Implement the foundations of a *Warehouse Management System* (WMS)
* Your solution should provide the following:
  * Modelling
  * Public API
  * Validation
* Scope
  * Use any language and framework of your choice
    * The byrd stack currently uses Flask and Python 2.7
  * Don't spend days working on your solution
	  * **Focus on quality over quantity** - *production ready* code is preferred
	  * If you run out of time, let us know what your solution is missing
* Submission
  * Send an email to `tech.careers@getbyrd.com`
  * Provide us with a link to your solution - e.g. GitHub, Bitbucket etc.
  * Provide a short explanation of your solution - e.g. the tools you used and why

## Models
* SKU
  * ID
  * Product name
* Storage
  * ID
  * Stock
  * SKU
* Order
  * Customer name
  * ID
* Order Line
  * ID
  * SKU
  * Quantity

## API
* [_CRUD_](https://en.wikipedia.org/wiki/Create,_read,_update_and_delete) endpoints should be available for all models
* An additional endpoint should be provided to explain how to *fulfil an order* (details below)

### Fulfillments
* An endpoint should be provided to return instructions on how to fulfil an order
* Given an order, the system should return a list of the "picks" required, and from which storages
* The picks should take items from the storages with the fewest items *first*, and include picks from multiple storages if necessary
* The system should return a `400` error when the order cannot be fulfilled

#### Example
* Given an order
```js
{
  lines: [
    {
      sku: 'abc',
      quantity: 12
    },
    {
      sku: 'def',
      quantity: 2
    }
  ]
}
```

* And the storages
```js
[
  {
    id: 'zzz',
    sku: 'abc',
    quantity: 5
  },
  {
    id: 'yyy',
    sku: 'abc',
    quantity: 100
  },
  {
    id: 'xxx',
    sku: 'def',
    quantity: 100
  }
]
```

*  The system should return the picks
```js
[
  {
    id: 'zzz',
    quantity: 5
  },
  {
    id: 'yyy',
    quantity: 7
  },
  {
    id: 'xxx',
    quantity: 2
  }
]
```

### BONUS: Order Searching
* If you find yourself with the time, it should also be possible to search for orders based on the customer name, by providing a `?q` query parameter
* The search should ignore character variants such as `ü`
  * e.g. `?q=muller` should return an order by from a customer named "Thomas Müller"
* Alternatively, provide a few short sentences in your submission discussing how you might approach this problem