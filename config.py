import os
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# AWS Configuration
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
S3_BUCKET = os.getenv('S3_BUCKET')
ATHENA_DATABASE = os.getenv('ATHENA_DATABASE')
ATHENA_WORKGROUP = os.getenv('ATHENA_WORKGROUP', 'primary')
ATHENA_OUTPUT_LOCATION = os.getenv('ATHENA_OUTPUT_LOCATION')

# OpenAI Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Validate required environment variables
def validate_config():
    required_vars = [
        ('S3_BUCKET', S3_BUCKET),
        ('ATHENA_DATABASE', ATHENA_DATABASE),
        ('OPENAI_API_KEY', OPENAI_API_KEY),
        ('ATHENA_OUTPUT_LOCATION', ATHENA_OUTPUT_LOCATION)
    ]
    
    missing_vars = [var_name for var_name, var_value in required_vars if not var_value]
    
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")

# Sample schema for reference
SAMPLE_SCHEMA = """
CREATE EXTERNAL TABLE IF NOT EXISTS sales_data (
    customer_id STRING,
    order_date DATE,
    amount DECIMAL(10,2),
    region STRING
)
STORED AS PARQUET
LOCATION 's3://{bucket}/sales_data/'
""".format(bucket=S3_BUCKET) 