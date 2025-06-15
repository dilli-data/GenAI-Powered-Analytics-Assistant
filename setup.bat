@echo off
echo Starting GenAI Analytics Assistant Setup...

:: Check Python version
python -c "import sys; sys.exit(0 if sys.version_info >= (3,8) else 1)" 2>NUL
if errorlevel 1 (
    echo Error: Python 3.8 or higher is required
    exit /b 1
)

:: Create virtual environment
echo Creating virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

:: Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

:: Check if .env exists
if not exist .env (
    echo Creating .env file...
    copy .env.example .env
    echo Please edit .env file with your configuration
    echo Required values:
    echo AWS_REGION=us-east-1
    echo S3_BUCKET=your-bucket-name
    echo ATHENA_DATABASE=your_database_name
    echo ATHENA_WORKGROUP=primary
    echo ATHENA_OUTPUT_LOCATION=s3://your-bucket-name/athena-results/
    echo OPENAI_API_KEY=your-openai-api-key
)

:: Generate sample data
echo Generating sample data...
python data\generate_sample_data.py

:: Check AWS CLI
where aws >nul 2>nul
if errorlevel 1 (
    echo AWS CLI is not installed. Please install it first.
    echo Visit: https://aws.amazon.com/cli/
    exit /b 1
)

:: Check AWS credentials
aws sts get-caller-identity >nul 2>nul
if errorlevel 1 (
    echo AWS credentials not found. Please run 'aws configure'
    exit /b 1
)

echo Setup completed successfully!
echo To start the application, run:
echo streamlit run streamlit_ui.py 