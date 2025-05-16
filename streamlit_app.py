import streamlit as st
from agno.agent import Agent
from agno.models.deepseek import DeepSeek
from agno.tools.reasoning import ReasoningTools
from agno.tools.yfinance import YFinanceTools

# Initialize the agent outside the main function to avoid re-initialization on every rerun
@st.cache_resource
def create_agent():
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
    return agent

agent = create_agent()

st.title("Финансовый Аналитик")

user_query = st.text_input("Введите ваш запрос:", "Выведи перспективные компании, объясни, почему. Какие прогнозы. Что покупать, продавать?")

if st.button("Анализировать"):
    if user_query:
        with st.spinner("Анализирую..."):
            response_placeholder = st.empty()
            full_response = ""

            for chunk in agent.stream(user_query, show_full_reasoning=False, stream_intermediate_steps=False):
                full_response += chunk
                response_placeholder.markdown(full_response)
    else:
        st.warning("Пожалуйста, введите ваш запрос.")
