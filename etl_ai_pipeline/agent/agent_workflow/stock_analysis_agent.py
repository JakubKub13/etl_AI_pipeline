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
            Focus on key trends, volatility patterns, and actionable insights."""
            
            analysis_prompt = f"""
            Analyze the following stock data for {state['ticker']}:
            
            Trends Data:
            {state['trends_data']}
            
            Volatility Data:
            {state['volatility_data']}
            
            Create a professional analysis report including:
            1. Market Overview
            2. Technical Analysis
            3. Risk Assessment
            4. Trading Recommendations
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

    def _create_workflow(self) -> StateGraph:
        """Create the workflow graph."""
        workflow = StateGraph(StockAnalysisState)
        
        # Add nodes
        workflow.add_node("fetch_trends", self.fetch_trends_data)
        workflow.add_node("fetch_volatility", self.fetch_volatility_data)
        workflow.add_node("generate_report", self.generate_analysis_report)
        
        # Add edges
        workflow.add_edge(START, "fetch_trends")
        workflow.add_edge("fetch_trends", "fetch_volatility")
        workflow.add_edge("fetch_volatility", "generate_report")
        workflow.add_edge("generate_report", END)

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
                email_sent=False
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
        state = {
            "ticker": "TSLA",
            "date": datetime.now().strftime("%Y-%m-%d"),
        }
        result = await agent.workflow.ainvoke(state)
        print(result)
    
    # Spustenie asynchrónnej funkcie
    asyncio.run(run_analysis())