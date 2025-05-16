import streamlit as st
from agno.agent import Agent
from agno.models.deepseek import DeepSeek
from agno.tools.reasoning import ReasoningTools
from agno.tools.yfinance import YFinanceTools

# Set up the Streamlit app
st.title("Stock Market Prediction Agent")
st.write("This agent analyzes stock market trends and predicts what might grow in the next 3 months.")

# Initialize the agent (we'll cache this to avoid reinitialization)
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
    "Ask about stock predictions (e.g., 'What will grow in the next 3 months?'):",
    "Что будет расти через 3 месяца"
)

if st.button("Get Prediction"):
    # Create a placeholder for the streaming response
    response_placeholder = st.empty()
    full_response = ""

    # Stream the response
    for chunk in agent.stream_response(
        user_query,
        stream=True,
        show_full_reasoning=True,
        stream_intermediate_steps=True
    ):
        full_response += chunk
        response_placeholder.markdown(full_response)

    # Display the final response
    response_placeholder.markdown(full_response)
