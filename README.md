# MongoDBAggregation

This is a test project for demonstrating MongoDB Aggregation capabilities using pipeline.

## Sample Database

The database contains data from a mock office supply company. The company tracks customer information and sales data, and has several store locations throughout the world.

## Collection

This database contains a single collection named sales. Each document in the collection represents a single sale from a store run by the supply company. Each document contains the item(s) purchased, information on the customer who made the purchase, and several other details regarding the sale. A sample document has been presented below.

```json
{
  "_id": {
    "$oid": "5bd761dcae323e45a93ccfe8"
  },
  "saleDate": {
    "$date": {
      "$numberLong": "1427144809506"
    }
  },
  "items": [
    {
      "name": "notepad",
      "tags": ["office", "writing", "school"],
      "price": {
        "$numberDecimal": "35.29"
      },
      "quantity": {
        "$numberInt": "2"
      }
    },
    {
      "name": "pens",
      "tags": ["writing", "office", "school", "stationary"],
      "price": {
        "$numberDecimal": "56.12"
      },
      "quantity": {
        "$numberInt": "5"
      }
    },
    {
      "name": "envelopes",
      "tags": ["stationary", "office", "general"],
      "price": {
        "$numberDecimal": "19.95"
      },
      "quantity": {
        "$numberInt": "8"
      }
    },
    {
      "name": "binder",
      "tags": ["school", "general", "organization"],
      "price": {
        "$numberDecimal": "14.16"
      },
      "quantity": {
        "$numberInt": "3"
      }
    }
  ],
  "storeLocation": "Denver",
  "customer": {
    "gender": "M",
    "age": {
      "$numberInt": "42"
    },
    "email": "cauho@witwuta.sv",
    "satisfaction": {
      "$numberInt": "4"
    }
  },
  "couponUsed": true,
  "purchaseMethod": "Online"
}
```

## Aggregation in MongoDB

In MongoDB, aggregation operations process the data records/documents and return computed results. Among the three ways to perform aggregation in MongoDB provided below, we are concerned with **Aggregation pipeline**

- Aggregation pipeline
- Map-reduce function
- Single-purpose aggregation

###### Aggregation pipeline

The aggregation pipeline is a multi-stage pipeline, so in each state, the documents taken as input and produce the resultant set of documents now in the next stage(id available) the resultant documents taken as input and produce output, this process is going on till the last stage.

Lets Discuss the aggregation pipeline used here in lib/aggregation.py

###### Scenario

Making use of a number of stages, the goal is to separate our young tech savvy customers' information to three different servers (Server1, Server2, Server3) based on the total amount they have spent. Each of the stages involved has been represented and described below.

![Aggregation Pipeline Diagram](https://github.com/Mgajurel/MongoDBAggregation/blob/main/resources/daigram.png)

1. **Pipeline1 stage:**
   The first stage is a _$match_ stage. We have applied a filtering to select only those data whose items bought either
   contains a _backpack_ or _laptop_, has paid _Online_ and is below _30_ years of age (Hence, Young Tech savvy customers)

   ```python
   pipeline1 = {'$match': {'items.name': {'$in': ['bagpack', 'laptop']},
                            'purchaseMethod': 'Online', 'customer.age': {'$lt': 30}}}
   ```

2. **Pipeline2 stage:**
   The second stage is a _$unwind_ stage. This stage is used to unwind the document in _items_ array, so we can evaluate the
   totalPurchase amount.

   ```python
   pipeline2 = {'$unwind': '$items'}
   ```

3. **Pipeline3 stage:**
   The third stage is a _$group_ stage. Groups input documents by the specified _\_id_ expression, in our case it is the customer information in _customer_ and also finds the _totalPurchase_ made by the customer by multiplying _items.price_ and _items.quantity_ and adding them for each _items_ .

   ```python
   pipeline3 = {'$group': {
        '_id': '$customer',
        'totalPurchase': {'$sum': {'$multiply': ['$items.price', '$items.quantity']}}}}
   ```

4. **Pipeline4 stage:**
   The fourth stage is a _$project_ stage. This stage is used to add or remove fields from the output of previous stage.
   Here, we have retained _totalPurchase_, assigned _\_id_ (which contains customer info) to _customer_, removed _\_id_(for aesthetics) and finally added a new field _environment_ to each aggregated result whose values can be _Server1_, _Server2_ or _Server3_ based on the _totalPurchase_ the customer has made which is demonstrated below.

   ```python
   pipeline4 = {'$project': {'totalPurchase': 1, 'customer': '$_id', '_id': 0, 'environment':
                              {'$switch': {'branches': [
                                  {'case': {
                                      '$gt': ['$totalPurchase', 5000]}, 'then': 'Server1'},
                                  {'case': {
                                      '$lt': ['$totalPurchase', 2000]}, 'then': 'Server3'},
                              ],
                                  'default': 'Server2'
                              }}}}
   ```

5. **Pipeline5 stage:**
   The final stage is again a _$group_ stage. This stage is used to group the aggregated result based on _environment_ which is, after this, used to write them to respective servers.

   ```python
   pipeline5 = {'$group': {
        '_id': '$environment', 'data': {'$push': '$$ROOT'}}}
   ```
