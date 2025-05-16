import streamlit as st
from agno.agent import Agent
from agno.models.deepseek import DeepSeek
from agno.tools.reasoning import ReasoningTools
from agno.tools.yfinance import YFinanceTools

# Set up the Streamlit app
st.title("Stock Market Prediction Agent")
st.write("This agent analyzes stock market trends and predicts what might grow in the next 3 months.")

@st.cache_resource
def get_agent():
    return Agent(
        model=DeepSeek(id="deepseek-chat"),
        tools=[
            ReasoningTools(add_instructions=True),
            YFinanceTools(
                stock_price=True,
                analyst_recommendations=True,
                company_info=True,
                company_news=True,
            ),
        ],
        instructions=[
            "Use tables to display data.",
            "Include sources in your response.",
            "Only include the report in your response. No other text.",
        ],
        markdown=True,
    )

agent = get_agent()

# User input
user_query = st.text_input(
    "Ask about stock predictions:",
    "What stocks are likely to grow in the next 3 months?"
)

if st.button("Get Prediction"):
    try:
        # Create a placeholder for the response
        response_placeholder = st.empty()
        
        # Get the response (using regular response instead of stream_response)
        response = agent.run(user_query)
        
        # Display the response
        response_placeholder.markdown(response)
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please try again or check the logs for more details.")
