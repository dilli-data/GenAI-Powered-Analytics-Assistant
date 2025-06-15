#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting GenAI Analytics Assistant Setup...${NC}"

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
if (( $(echo "$python_version < 3.8" | bc -l) )); then
    echo -e "${RED}Error: Python 3.8 or higher is required${NC}"
    exit 1
fi

# Create virtual environment
echo -e "${GREEN}Creating virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo -e "${GREEN}Installing dependencies...${NC}"
pip install -r requirements.txt

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${GREEN}Creating .env file...${NC}"
    cp .env.example .env
    echo -e "${RED}Please edit .env file with your configuration${NC}"
    echo -e "Required values:"
    echo "AWS_REGION=us-east-1"
    echo "S3_BUCKET=your-bucket-name"
    echo "ATHENA_DATABASE=your_database_name"
    echo "ATHENA_WORKGROUP=primary"
    echo "ATHENA_OUTPUT_LOCATION=s3://your-bucket-name/athena-results/"
    echo "OPENAI_API_KEY=your-openai-api-key"
fi

# Generate sample data
echo -e "${GREEN}Generating sample data...${NC}"
python data/generate_sample_data.py

# Check AWS CLI
if ! command -v aws &> /dev/null; then
    echo -e "${RED}AWS CLI is not installed. Please install it first.${NC}"
    echo "Visit: https://aws.amazon.com/cli/"
    exit 1
fi

# Check AWS credentials
if ! aws sts get-caller-identity &> /dev/null; then
    echo -e "${RED}AWS credentials not found. Please run 'aws configure'${NC}"
    exit 1
fi

echo -e "${GREEN}Setup completed successfully!${NC}"
echo -e "To start the application, run:"
echo -e "${GREEN}streamlit run streamlit_ui.py${NC}" 