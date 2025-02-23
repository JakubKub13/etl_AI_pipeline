🚀 ETL AI Pipeline for Stock Analysis

📊 Overview
A sophisticated ETL pipeline that processes stock market data using AI/LLM for enhanced analysis and automated reporting. The application uses LangGraph for workflow management and Claude 3.5 Sonnet for market analysis.

✨ Features
- Stock data processing with Polygon API
- AI-powered market analysis using Claude 3.5 Sonnet 
- Automated HTML report generation
- Email notifications with analysis reports
- Supabase database integration
- FastAPI REST endpoints

🛠 Prerequisites
- Python 3.9+
- Poetry for dependency management
- Supabase account
- Anthropic API key
- SMTP server access
- Polygon.io API key

Clone repository
git clone https://github.com/yourusername/etl-ai-pipeline.git
cd etl-ai-pipeline

# DB setup
The application uses Supabase. Create the following tables:
-- stock_data table
CREATE TABLE stock_data (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  ticker VARCHAR(10) NOT NULL,
  date DATE NOT NULL,
  open_price DECIMAL NOT NULL,
  high_price DECIMAL NOT NULL,
  low_price DECIMAL NOT NULL,
  close_price DECIMAL NOT NULL,
  volume INTEGER NOT NULL,
  after_hours_price DECIMAL,
  pre_market_price DECIMAL,
  status VARCHAR(20) NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- stock_analysis table
CREATE TABLE stock_analysis (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  stock_data_id UUID REFERENCES stock_data(id),
  llm_analysis TEXT NOT NULL,
  market_sentiment VARCHAR(20) NOT NULL,
  model_version VARCHAR(50) NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

# Install Poetry
curl -sSL https://install.python-poetry.org | python3 

# Install dependencies
poetry install

# Spawn shell
poetry shell

# Start the application
poetry run start

# Access the API documentation
OpenAPI UI: http://localhost:8000/docs






