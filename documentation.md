# API Documentation (Made by Fred and Angel)

## Connecting to the API

Since we are running our API locally, access the endpoint at `http://127.0.0.1:5000` (or the address the appears on your console).

## Welcome

- **Method:** GET
- **Path:** `/`
- **Query parameters:** None

This endpoint sends a basic message verifying API operating capability.

### **Request (Example):**

```sh
curl -X GET http://127.0.0.1:5000/
```

### **Response (Example):**

```json
"Flask API is running. Go to /data to view the CSV in JSON format."
```

---

## Get Data

- **Method:** GET
- **Path:** `/data`
- **Query parameters (optional):**
  - `limit` (integer) - Number of records to return (default: 10)
  - `offset` (integer) - Number of records to skip (default: 0)
  - `format` (string) - Response format (`json` or `csv`, default: `json`)
  - Additional query parameters to filter data by column values

This API filters and paginates data from the CSV file housed on GitHub at will.

### **Request (Example):**

```sh
curl -X GET "http://127.0.0.1:5000/data?limit=5&format=json"
```

### **Response (Example):**

```json
[
  {
    "Region Code": "001",
    "Region": "World",
    "Year": 2022,
    "Value": 789456123
  },
  {
    "Region Code": "002",
    "Region": "Africa",
    "Year": 2022,
    "Value": 123456789
  }
]
```

### **Request (CSV format) (Example):**

```sh
curl -X GET "http://127.0.0.1:5000/data?limit=5&format=csv"
```

### **Response (CSV file content) (Example):**

```csv
Region Code,Region,Year,Value
001,World,2022,789456123
002,Africa,2022,123456789
```

---

## Filtering Data

- Data can be filtered by users supplying query parameters matching column names.
- Example: To filter by `Region Code` and get results for `001`:

### **Request (Example):**

```sh
curl -X GET "http://127.0.0.1:5000/data?Region Code=001"
```

### **Response (Example):**

```json
[
  {
    "Region Code": "001",
    "Region": "World",
    "Year": 2022,
    "Value": 789456123
  }
]
```