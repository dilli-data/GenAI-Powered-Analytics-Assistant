# Sample Data

This directory contains sample data files and instructions for setting up your data in Amazon S3.

## Data Structure

The application expects Parquet files with the following schema:

```sql
CREATE EXTERNAL TABLE IF NOT EXISTS sales_data (
    customer_id STRING,
    order_date DATE,
    amount DECIMAL(10,2),
    region STRING
)
STORED AS PARQUET
```

## Sample Data Generation

You can generate sample data using the following Python script:

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Generate sample data
np.random.seed(42)
n_records = 1000

data = {
    'customer_id': [f'CUST{i:04d}' for i in range(n_records)],
    'order_date': [
        datetime.now() - timedelta(days=np.random.randint(0, 365))
        for _ in range(n_records)
    ],
    'amount': np.random.uniform(10, 1000, n_records).round(2),
    'region': np.random.choice(['North', 'South', 'East', 'West'], n_records)
}

df = pd.DataFrame(data)

# Save as Parquet
df.to_parquet('sample_sales_data.parquet')
```

## Uploading to S3

1. Create an S3 bucket:
```bash
aws s3 mb s3://your-bucket-name
```

2. Upload the Parquet file:
```bash
aws s3 cp sample_sales_data.parquet s3://your-bucket-name/sales_data/
```

## Data Location

The data should be uploaded to:
```
s3://your-bucket-name/sales_data/
```

Make sure to update the `S3_BUCKET` environment variable in your `.env` file to match your bucket name. 