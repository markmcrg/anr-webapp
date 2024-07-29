data_dict = {
    "type": "sql_endpoint",
    "data": {
        "columns": [
            {
                "col": "username",
                "data_type": "VARCHAR",
                "nullable": True
            }
        ],
        "rows": ['asd'],
        "result": {
            "code": 200,
            "message": "Query OK!",
            "start_ms": 1722286346789,
            "end_ms": 1722286346798,
            "latency": "9.118209ms",
            "row_count": 0,
            "row_affect": 0,
            "limit": 1000
        }
    }
}

# Check if there are any rows
if data_dict["data"]["rows"]:
    print("There are rows in the data.")
else:
    print("There are no rows in the data.")