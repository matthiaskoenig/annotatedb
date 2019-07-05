
see also https://django-elasticsearch-dsl-drf.readthedocs.io/en/0.1.8/basic_usage_examples.html

## Usage examples
The generic enpoint to access mappings is
```
http://localhost:9000/search/mapping/?format=json
```
This returns all mappings ass paginated results. To access a given subset of mappings
use the `search` and `filter` options on the endpoint described below.


### Search
Multiple search terms are joined with `OR`.

Let’s assume we have a number of `Mapping` items with fields `source.term`, `qualifier` and `source.collection.namespace`.

#### Search in all fields
Search in all fields (name, address, city, state_province and country) for word “reilly”.
```
/search/publisher/?search=reilly
/search/mapping/?search=CHEBI:123
```

#### Search a single term on specific field
In order to search in specific field (name) for term “reilly”, 
add the field name separated with | to the search term.
```
http://127.0.0.1:8080/search/publisher/?search=name|reilly
```

#### Search for multiple terms

In order to search for multiple terms “reilly”, “bloomsbury” add multiple search query params.
```
http://127.0.0.1:8080/search/publisher/?search=reilly&search=bloomsbury
```

#### Search for multiple terms in specific fields

In order to search for multiple terms “reilly”, “bloomsbury” in specific fields add multiple search query params and field names separated with | to each of the search terms.
```
http://127.0.0.1:8080/search/publisher/?search=name|reilly&search=city|london
```

### Filtering
Let’s assume we have a number of Publisher documents with in cities (Yerevan, Groningen, Amsterdam, London).

Multiple filter terms are joined with `AND`.

#### Filter documents by single field
Filter documents by field (city) “yerevan”.
```
http://127.0.0.1:8080/search/publisher/?city=yerevan
```

#### Filter documents by multiple fields

Filter documents by city “Yerevan” and “Groningen”.
```
http://127.0.0.1:8080/search/publisher/?city__in=yerevan|groningen
```
You can achieve the same effect by specifying multiple filters (city) “Yerevan” and “Amsterdam”. 
Note, that in this case multiple filter terms are joined with OR.
```
http://127.0.0.1:8080/search/publisher/?city=yerevan&city=amsterdam
```
If you want the same as above, but joined with AND, add __term to each lookup.
```
http://127.0.0.1:8080/search/publisher/?city__term=education&city__term=economy
```

#### Filter documents by a word part of a single field
Filter documents by a part word part in single field (city) “ondon”.

```
http://127.0.0.1:8080/search/publisher/?city__wildcard=*ondon
```

### Ordering

The `-` prefix means ordering should be descending.

#### Order documents by field (ascending)
Filter documents by field city (ascending).
```
http://127.0.0.1:8080/search/publisher/?search=country|armenia&ordering=city
```

#### Order documents by field (descending)
Filter documents by field country (descending).
```
http://127.0.0.1:8080/search/publisher/?ordering=-country
```
#### Order documents by multiple fields

If you want to order by multiple fields, use multiple ordering query params. In the example below, documents would be ordered first by field country (descending), then by field city (ascending).
```
http://127.0.0.1:8080/search/publisher/?ordering=-country&ordering=city
```

