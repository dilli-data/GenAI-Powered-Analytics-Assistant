import streamlit as st
import pandas as pd
from sql_generator import SQLGenerator
from athena_query import AthenaQueryExecutor
import logging
from config import validate_config

# Configure logging
logger = logging.getLogger(__name__)

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def format_dataframe(df: pd.DataFrame) -> str:
    """Format DataFrame as a readable string"""
    if df.empty:
        return "No results found."
    
    # Convert DataFrame to string with formatting
    return df.to_string(index=False)

def main():
    st.title("GenAI Analytics Assistant")
    st.write("Ask questions about your data in natural language!")
    
    # Initialize components
    sql_generator = SQLGenerator()
    athena_executor = AthenaQueryExecutor()
    
    # Chat input
    user_question = st.chat_input("Ask a question about your data...")
    
    if user_question:
        try:
            # Add user question to chat
            st.session_state.chat_history.append(("user", user_question))
            
            # Generate SQL
            with st.spinner("Generating SQL query..."):
                sql_query = sql_generator.generate_sql(user_question)
            
            # Execute query
            with st.spinner("Executing query..."):
                results_df = athena_executor.execute_query(sql_query)
            
            # Format response
            response = f"Here are the results:\n\n{format_dataframe(results_df)}"
            st.session_state.chat_history.append(("assistant", response))
            
        except Exception as e:
            error_message = f"Error: {str(e)}"
            st.session_state.chat_history.append(("assistant", error_message))
            logger.error(error_message)
    
    # Display chat history
    for role, message in st.session_state.chat_history:
        if role == "user":
            st.chat_message("user").write(message)
        else:
            st.chat_message("assistant").write(message)

if __name__ == "__main__":
    try:
        # Validate configuration
        validate_config()
        main()
    except Exception as e:
        st.error(f"Application error: {str(e)}")
        logger.error(f"Application error: {str(e)}") 