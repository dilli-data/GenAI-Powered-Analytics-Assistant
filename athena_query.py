import boto3
import time
import pandas as pd
import logging
from config import (
    AWS_REGION,
    ATHENA_DATABASE,
    ATHENA_WORKGROUP,
    ATHENA_OUTPUT_LOCATION
)

logger = logging.getLogger(__name__)

class AthenaQueryExecutor:
    def __init__(self):
        self.client = boto3.client('athena', region_name=AWS_REGION)
        self.database = ATHENA_DATABASE
        self.workgroup = ATHENA_WORKGROUP
        self.output_location = ATHENA_OUTPUT_LOCATION
    
    def execute_query(self, query: str) -> pd.DataFrame:
        """
        Execute SQL query on Athena and return results as DataFrame
        
        Args:
            query (str): SQL query to execute
            
        Returns:
            pd.DataFrame: Query results
        """
        try:
            # Start query execution
            logger.info(f"Executing query: {query}")
            response = self.client.start_query_execution(
                QueryString=query,
                QueryExecutionContext={'Database': self.database},
                WorkGroup=self.workgroup,
                ResultConfiguration={'OutputLocation': self.output_location}
            )
            
            query_execution_id = response['QueryExecutionId']
            
            # Wait for query to complete
            while True:
                query_status = self.client.get_query_execution(
                    QueryExecutionId=query_execution_id
                )['QueryExecution']['Status']['State']
                
                if query_status in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
                    break
                    
                time.sleep(1)
            
            if query_status == 'FAILED':
                error_message = self.client.get_query_execution(
                    QueryExecutionId=query_execution_id
                )['QueryExecution']['Status']['StateChangeReason']
                raise Exception(f"Query failed: {error_message}")
            
            # Get results
            results = []
            paginator = self.client.get_paginator('get_query_results')
            
            for page in paginator.paginate(QueryExecutionId=query_execution_id):
                for row in page['ResultSet']['Rows'][1:]:  # Skip header row
                    results.append([field.get('VarCharValue', '') for field in row['Data']])
            
            # Convert to DataFrame
            if not results:
                return pd.DataFrame()
                
            columns = [field['Label'] for field in 
                      self.client.get_query_results(
                          QueryExecutionId=query_execution_id
                      )['ResultSet']['Rows'][0]['Data']]
            
            df = pd.DataFrame(results, columns=columns)
            logger.info(f"Query completed successfully. Retrieved {len(df)} rows.")
            return df
            
        except Exception as e:
            logger.error(f"Error executing query: {str(e)}")
            raise 