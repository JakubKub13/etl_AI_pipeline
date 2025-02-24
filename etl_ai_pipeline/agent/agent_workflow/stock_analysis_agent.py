from typing import Dict, List, Literal
import logging
from datetime import datetime
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_anthropic import ChatAnthropic
from ...db.analysis_queries import StockAnalyzer
from ...db.Stock_data_manager import StockDataManager
from ...agent.models.models import StockAnalysisState, EmailConfig
from ...settings import settings
from ...services.email_service import EmailService

logger = logging.getLogger(__name__)

class StockAnalysisAgent:

    def __init__(self):
        """Initialize the stock analysis agent."""
        self.stock_analyzer = StockAnalyzer(StockDataManager())
        self.llm = ChatAnthropic(
            model="claude-3-5-sonnet-20240620",
            temperature=0.5,
        )
        self.workflow = self._create_workflow()
        self.email_service = EmailService()

    async def fetch_trends_data(self, state: StockAnalysisState) -> Dict:
        """Fetch trends data for the specified ticker."""
        try:
            trends = await self.stock_analyzer.identify_short_term_trends(state["ticker"])
            logger.info(f"Trends data fetched for {state['ticker']}")
            return {"trends_data": trends}
        except Exception as e:
            logger.error(f"Error fetching trends data: {e}")
            raise

    async def fetch_volatility_data(self, state: StockAnalysisState) -> Dict:
        """Fetch volatility data for the specified ticker."""
        try:
            volatility = await self.stock_analyzer.calculate_short_term_volatility(state["ticker"])
            logger.info(f"Volatility data fetched for {state['ticker']}")
            return {"volatility_data": volatility}
        except Exception as e:
            logger.error(f"Error fetching volatility data: {e}")
            raise

    async def generate_analysis_report(self, state: StockAnalysisState) -> Dict:
        """Generate analysis report using LLM."""
        try:
            system_prompt = """You are a professional stock market analyst. 
            Analyze the provided market data and create a detailed, professional report.
            Format your response in clean HTML with proper styling."""
            
            analysis_prompt = f"""
            Analyze the following stock data for {state['ticker']}:
            
            Trends Data:
            {state['trends_data']}
            
            Volatility Data:
            {state['volatility_data']}
            
            Create a professional analysis report using this HTML template:
            
            <div style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px;">
                <h1 style="color: #333; border-bottom: 2px solid #eee; padding-bottom: 10px;">
                    Stock Analysis Report: {state['ticker']}
                </h1>
                
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h2 style="color: #444; margin-top: 0;">1. Market Overview</h2>
                    [Insert your market overview here]
                </div>
                
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h2 style="color: #444; margin-top: 0;">2. Technical Analysis</h2>
                    [Insert your technical analysis here]
                </div>
                
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h2 style="color: #444; margin-top: 0;">3. Risk Assessment</h2>
                    [Insert your risk assessment here]
                </div>
                
                <div style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h2 style="color: #444; margin-top: 0;">4. Trading Recommendations</h2>
                    [Insert your trading recommendations here]
                </div>
                
                <div style="font-size: 12px; color: #666; margin-top: 30px; padding-top: 10px; border-top: 1px solid #eee;">
                    Report generated on {state['date']}
                </div>
            </div>
            """

            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=analysis_prompt)
            ]

            response = await self.llm.ainvoke(messages)
            return {"analysis_report": response.content}
        except Exception as e:
            logger.error(f"Error generating analysis report: {e}")
            raise

    async def send_email_report(self, state: StockAnalysisState) -> Dict:
        """Send analysis report via email."""
        try:
            email_service = EmailService()
            subject = f"Stock Analysis Report - {state['ticker']} - {state['date']}"
            
            await email_service.send_analysis_report(
                recipient_email=state['email_config'].recipient_email,
                subject=subject,
                report_content=state['analysis_report'],
                cc=state['email_config'].cc
            )
            
            logger.info(f"Analysis report sent for {state['ticker']}")
            return {"email_sent": True}
        except Exception as e:
            logger.error(f"Error sending email report: {e}")
            raise

    def _create_workflow(self) -> StateGraph:
        """Create the workflow graph with parallel data fetching."""
        workflow = StateGraph(StockAnalysisState)
        
        # Add nodes
        workflow.add_node("fetch_trends", self.fetch_trends_data)
        workflow.add_node("fetch_volatility", self.fetch_volatility_data)
        workflow.add_node("generate_report", self.generate_analysis_report)
        workflow.add_node("send_email", self.send_email_report)
        
        # Create parallel execution
        workflow.add_edge(START, "fetch_trends")
        workflow.add_edge(START, "fetch_volatility")
        workflow.add_edge("fetch_trends", "generate_report")
        workflow.add_edge("fetch_volatility", "generate_report")
        workflow.add_edge("generate_report", "send_email")
        workflow.add_edge("send_email", END)
        
        return workflow.compile()
    
    async def run_analysis(self, ticker: str, date: str, email_config: EmailConfig) -> Dict:
        """
        Run the complete analysis workflow.
        
        Args:
            ticker (str): Stock ticker symbol
            date (str): Analysis date
            email_config (EmailConfig): Email configuration
            
        Returns:
            Dict: Analysis results and status
        """
        try:
            initial_state = StockAnalysisState(
                ticker=ticker,
                date=date,
                trends_data=None,
                volatility_data=None,
                analysis_report=None,
                email_sent=False,
                email_config=email_config
            )
            
            result = await self.workflow.ainvoke(initial_state)
            return result
        except Exception as e:
            logger.error(f"Error running analysis workflow: {e}")
            raise

if __name__ == "__main__":
    import asyncio
    
    async def run_analysis():
        agent = StockAnalysisAgent()
        email_config = EmailConfig(
            recipient_email="jakubkubala3@gmail.com",
            subject="Stock Analysis Report"
        )
        state = StockAnalysisState(
            ticker="AAPL",
            date=datetime.now().strftime("%Y-%m-%d"),
            trends_data=None,
            volatility_data=None,
            analysis_report=None,
            email_sent=False,
            email_config=email_config
        )
        result = await agent.workflow.ainvoke(state)
        print(result)
    
    asyncio.run(run_analysis())