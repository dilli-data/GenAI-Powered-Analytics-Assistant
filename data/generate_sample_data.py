import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def generate_sample_data(n_records: int = 1000, output_file: str = 'sample_sales_data.parquet'):
    """
    Generate sample sales data and save it as a Parquet file.
    
    Args:
        n_records (int): Number of records to generate
        output_file (str): Output file path
    """
    try:
        logger.info(f"Generating {n_records} sample records...")
        
        # Set random seed for reproducibility
        np.random.seed(42)
        
        # Generate data
        data = {
            'customer_id': [f'CUST{i:04d}' for i in range(n_records)],
            'order_date': [
                datetime.now() - timedelta(days=np.random.randint(0, 365))
                for _ in range(n_records)
            ],
            'amount': np.random.uniform(10, 1000, n_records).round(2),
            'region': np.random.choice(['North', 'South', 'East', 'West'], n_records)
        }
        
        # Create DataFrame
        df = pd.DataFrame(data)
        
        # Save as Parquet
        df.to_parquet(output_file)
        logger.info(f"Sample data saved to {output_file}")
        
        # Print sample statistics
        logger.info("\nSample Statistics:")
        logger.info(f"Total Records: {len(df)}")
        logger.info(f"Date Range: {df['order_date'].min()} to {df['order_date'].max()}")
        logger.info(f"Amount Range: ${df['amount'].min():.2f} to ${df['amount'].max():.2f}")
        logger.info("\nRecords by Region:")
        logger.info(df['region'].value_counts())
        
    except Exception as e:
        logger.error(f"Error generating sample data: {str(e)}")
        raise

if __name__ == "__main__":
    generate_sample_data() 