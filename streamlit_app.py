import streamlit as st
from agno.agent import Agent
from agno.models.deepseek import DeepSeek
from agno.tools.reasoning import ReasoningTools
from agno.tools.yfinance import YFinanceTools

# Initialize the agent with DeepSeek and tools
agent = Agent(
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

# Streamlit App
def main():
    st.title("Stock Recommendation and Analysis")

    # Text input for user's question
    user_input = st.text_area("Ask about stock analysis and recommendations:")

    if user_input:
        with st.spinner("Processing your request..."):
            # Get response from the agent
            response = agent.print_response(
                user_input,
                stream=True,
                show_full_reasoning=True,
                stream_intermediate_steps=True,
            )
            # Display the response
            st.markdown(response)

if __name__ == "__main__":
    main()
