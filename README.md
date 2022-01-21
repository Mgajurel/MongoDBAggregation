# MongoDBAggregation

This is a test project for demonstrating MongoDB Aggregation capabilities using pipeline.

# Sample Database

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
