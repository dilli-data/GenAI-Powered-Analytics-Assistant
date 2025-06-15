from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import StrOutputParser
from langchain.chains import LLMChain
import logging
import re
from config import OPENAI_API_KEY, SAMPLE_SCHEMA

logger = logging.getLogger(__name__)

class SQLGenerator:
    def __init__(self):
        self.llm = ChatOpenAI(
            model_name="gpt-3.5-turbo",
            temperature=0,
            api_key=OPENAI_API_KEY
        )
        
        # Define allowed operations and patterns
        self.allowed_operations = {
            'SELECT', 'FROM', 'WHERE', 'GROUP BY', 'ORDER BY', 'HAVING',
            'JOIN', 'LEFT JOIN', 'RIGHT JOIN', 'INNER JOIN', 'LIMIT'
        }
        
        self.allowed_functions = {
            'COUNT', 'SUM', 'AVG', 'MIN', 'MAX', 'DATE_TRUNC', 'DATE_ADD',
            'DATE_DIFF', 'CURRENT_DATE', 'CURRENT_TIMESTAMP'
        }
        
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are a SQL expert that converts natural language questions into Athena SQL queries.
            The database schema is as follows:
            {schema}
            
            Important rules:
            1. Always use Athena-compatible SQL syntax
            2. Use proper date functions for date operations
            3. Format numbers using DECIMAL type
            4. Include error handling for NULL values
            5. Use appropriate aggregation functions
            6. Return only the SQL query without any explanations
            7. DO NOT include any sensitive information in the query
            8. DO NOT use any table or column names not in the provided schema
            9. DO NOT include any data values in the query
            """),
            ("user", "{question}")
        ])
        
        self.chain = LLMChain(
            llm=self.llm,
            prompt=self.prompt_template,
            output_parser=StrOutputParser()
        )
    
    def sanitize_sql(self, sql_query: str) -> str:
        """
        Sanitize and validate the generated SQL query
        
        Args:
            sql_query (str): The SQL query to sanitize
            
        Returns:
            str: Sanitized SQL query
            
        Raises:
            ValueError: If query contains unauthorized operations or patterns
        """
        # Convert to uppercase for consistent checking
        query_upper = sql_query.upper()
        
        # Check for unauthorized operations
        for operation in self.allowed_operations:
            if operation in query_upper:
                break
        else:
            raise ValueError("Query must contain at least one allowed operation")
        
        # Check for unauthorized functions
        for func in self.allowed_functions:
            if func in query_upper:
                break
        else:
            raise ValueError("Query must contain at least one allowed function")
        
        # Check for potentially dangerous patterns
        dangerous_patterns = [
            r'DROP\s+TABLE',
            r'DELETE\s+FROM',
            r'TRUNCATE\s+TABLE',
            r'UPDATE\s+.*\s+SET',
            r'INSERT\s+INTO',
            r'CREATE\s+TABLE',
            r'ALTER\s+TABLE',
            r';\s*--',  # SQL injection attempts
            r'UNION\s+ALL',
            r'UNION\s+SELECT'
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, query_upper, re.IGNORECASE):
                raise ValueError(f"Query contains unauthorized pattern: {pattern}")
        
        return sql_query
    
    def generate_sql(self, question: str) -> str:
        """
        Generate SQL query from natural language question
        
        Args:
            question (str): Natural language question
            
        Returns:
            str: Generated SQL query
        """
        try:
            logger.info(f"Generating SQL for question: {question}")
            
            # Sanitize input question
            sanitized_question = re.sub(r'[^\w\s\?\.]', '', question)
            
            # Generate SQL
            sql_query = self.chain.invoke({
                "question": sanitized_question,
                "schema": SAMPLE_SCHEMA
            })
            
            # Sanitize and validate the generated SQL
            sanitized_sql = self.sanitize_sql(sql_query.strip())
            
            logger.info("SQL query generated and sanitized successfully")
            return sanitized_sql
            
        except Exception as e:
            logger.error(f"Error generating SQL: {str(e)}")
            raise 