# API Documentation (Made by Fred and Angel)

## Connecting to the API

Since we are running our API locally, access the endpoint at `http://127.0.0.1:5000` (or the address the appears on your console).

## Welcome

- **Method:** GET
- **Path:** `/`
- **Query parameters:** None

This endpoint sends a basic message verifying API operating capability.

### **Methodological Note on NaN Values**  

In this dataset, missing values in the `Footnotes` field are represented as `"NaN"` (with quotes) instead of `NaN`, since `NaN` is not a valid JSON type. Using quotes ensures compatibility with JSON parsers that do not recognize `NaN` and prevents errors when processing the data. Alternatively, `null` could be used to indicate missing values, but `"NaN"` maintains consistency with other textual representations in the dataset. This approach ensures that the data remains structured and readable across different platforms.

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
    "Footnotes": "NaN",
    "Country": "Total, all countries or areas",
    "Region Code": 1,
    "Series": "Population mid-year estimates (millions)",
    "Source": "United Nations Population Division, New York, World Population Prospects: The 2022 Revision, last accessed July 2022.",
    "Value": "6,985.60",
    "Year": 2010
  },
  {
    "Footnotes": "NaN",
    "Country": "Total, all countries or areas",
    "Region Code": 1,
    "Series": "Population mid-year estimates for males (millions)",
    "Source": "United Nations Population Division, New York, World Population Prospects: The 2022 Revision, last accessed July 2022.",
    "Value": "3,514.41",
    "Year": 2010
  },
  {
    "Footnotes": "NaN",
    "Country": "Total, all countries or areas",
    "Region Code": 1,
    "Series": "Population mid-year estimates for females (millions)",
    "Source": "United Nations Population Division, New York, World Population Prospects: The 2022 Revision, last accessed July 2022.",
    "Value": "3,471.20",
    "Year": 2010
  },
  {
    "Footnotes": "NaN",
    "Country": "Total, all countries or areas",
    "Region Code": 1,
    "Series": "Sex ratio (males per 100 females)",
    "Source": "United Nations Population Division, New York, World Population Prospects: The 2022 Revision; supplemented by data from the United Nations Statistics Division, New York, Demographic Yearbook 2021 and Secretariat for the Pacific Community (SPC) for small countries or areas, last accessed July 2022.",
    "Value": "101.2",
    "Year": 2010
  },
  {
    "Footnotes": "NaN",
    "Country": "Total, all countries or areas",
    "Region Code": 1,
    "Series": "Population aged 0 to 14 years old (percentage)",
    "Source": "United Nations Population Division, New York, World Population Prospects: The 2022 Revision; supplemented by data from the United Nations Statistics Division, New York, Demographic Yearbook 2021 and Secretariat for the Pacific Community (SPC) for small countries or areas, last accessed July 2022.",
    "Value": "27.1",
    "Year": 2010
  }
]
```

### **Request (CSV format) (Example):**

```sh
curl -X GET "http://127.0.0.1:5000/data?limit=5&format=csv"
```

### **Response (CSV file content) (Example):**

> **Note:** In this example, the `Footnotes` column is left empty (`, ,` in CSV format), but in other cases, it may contain values.

```csv
Region Code,Country,Year,Series,Value,Footnotes,Source
1,Total, all countries or areas,2010,789456123,6985.60, ,United Nations Population Division, New York, World Population Prospects: The 2022 Revision, last accessed July 2022.
1,Total, all countries or areas,2010,123456789,3514.41, ,United Nations Population Division, New York, World Population Prospects: The 2022 Revision, last accessed July 2022.
1,Total, all countries or areas,2010,123456789,3471.20, ,United Nations Population Division, New York, World Population Prospects: The 2022 Revision, last accessed July 2022.
1,Total, all countries or areas,2010,123456789,101.2, ,United Nations Population Division, New York, World Population Prospects: The 2022 Revision; supplemented by data from the United Nations Statistics Division, New York, Demographic Yearbook 2021 and Secretariat for the Pacific Community (SPC) for small countries or areas, last accessed July 2022.
1,Total, all countries or areas,2010,123456789,27.1, ,United Nations Population Division, New York, World Population Prospects: The 2022 Revision; supplemented by data from the United Nations Statistics Division, New York, Demographic Yearbook 2021 and Secretariat for the Pacific Community (SPC) for small countries or areas, last accessed July 2022.
```

---

## Filtering Data

- Data can be filtered by users supplying query parameters matching column names.
- Example: To filter by `Region Code` and get results for `1`:

### **Request (Example):**

```sh
curl -X GET "http://127.0.0.1:5000/data?Region%20Code=1"
```

### **Response (Example):**

```json
[
  {
    "Footnotes": "NaN",
    "Country": "Total, all countries or areas",
    "Region Code": 1,
    "Series": "Population mid-year estimates (millions)",
    "Source": "United Nations Population Division, New York, World Population Prospects: The 2022 Revision, last accessed July 2022.",
    "Value": "6,985.60",
    "Year": 2010
  },
  {
    "Footnotes": "NaN",
    "Country": "Total, all countries or areas",
    "Region Code": 1,
    "Series": "Population mid-year estimates for males (millions)",
    "Source": "United Nations Population Division, New York, World Population Prospects: The 2022 Revision, last accessed July 2022.",
    "Value": "3,514.41",
    "Year": 2010
  },
  {
    "Footnotes": "NaN",
    "Country": "Total, all countries or areas",
    "Region Code": 1,
    "Series": "Population mid-year estimates for females (millions)",
    "Source": "United Nations Population Division, New York, World Population Prospects: The 2022 Revision, last accessed July 2022.",
    "Value": "3,471.20",
    "Year": 2010
  },
  {
    "Footnotes": "NaN",
    "Country": "Total, all countries or areas",
    "Region Code": 1,
    "Series": "Sex ratio (males per 100 females)",
    "Source": "United Nations Population Division, New York, World Population Prospects: The 2022 Revision; supplemented by data from the United Nations Statistics Division, New York, Demographic Yearbook 2021 and Secretariat for the Pacific Community (SPC) for small countries or areas, last accessed July 2022.",
    "Value": "101.2",
    "Year": 2010
  },
  {
    "Footnotes": "NaN",
    "Country": "Total, all countries or areas",
    "Region Code": 1,
    "Series": "Population aged 0 to 14 years old (percentage)",
    "Source": "United Nations Population Division, New York, World Population Prospects: The 2022 Revision; supplemented by data from the United Nations Statistics Division, New York, Demographic Yearbook 2021 and Secretariat for the Pacific Community (SPC) for small countries or areas, last accessed July 2022.",
    "Value": "27.1",
    "Year": 2010
  },
  {
    "Footnotes": "NaN",
    "Country": "Total, all countries or areas",
    "Region Code": 1,
    "Series": "Population aged 60+ years old (percentage)",
    "Source": "United Nations Population Division, New York, World Population Prospects: The 2022 Revision; supplemented by data from the United Nations Statistics Division, New York, Demographic Yearbook 2021 and Secretariat for the Pacific Community (SPC) for small countries or areas, last accessed July 2022.",
    "Value": "11.1",
    "Year": 2010
  },
  {
    "Footnotes": "NaN",
    "Country": "Total, all countries or areas",
    "Region Code": 1,
    "Series": "Population density",
    "Source": "United Nations Population Division, New York, World Population Prospects: The 2022 Revision, last accessed July 2022.",
    "Value": "53.6",
    "Year": 2010
  },
  {
    "Footnotes": "NaN",
    "Country": "Total, all countries or areas",
    "Region Code": 1,
    "Series": "Population mid-year estimates (millions)",
    "Source": "United Nations Population Division, New York, World Population Prospects: The 2022 Revision, last accessed July 2022.",
    "Value": "7,426.60",
    "Year": 2015
  },
  {
    "Footnotes": "NaN",
    "Country": "Total, all countries or areas",
    "Region Code": 1,
    "Series": "Population mid-year estimates for males (millions)",
    "Source": "United Nations Population Division, New York, World Population Prospects: The 2022 Revision, last accessed July 2022.",
    "Value": "3,737.40",
    "Year": 2015
  },
  {
    "Footnotes": "NaN",
    "Country": "Total, all countries or areas",
    "Region Code": 1,
    "Series": "Population mid-year estimates for females (millions)",
    "Source": "United Nations Population Division, New York, World Population Prospects: The 2022 Revision, last accessed July 2022.",
    "Value": "3,689.19",
    "Year": 2015
  }
]
```