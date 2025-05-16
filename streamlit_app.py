import streamlit as st
from agno.agent import Agent
from agno.models.deepseek import DeepSeek
from agno.tools.reasoning import ReasoningTools
from agno.tools.yfinance import YFinanceTools

# Настройка агента
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

# Интерфейс Streamlit
st.title("📈 Финансовый AI-Аналитик")

query = st.text_input("Введите вопрос:", "самый высокий рос в ближайшие 3 месяца")

if st.button("🔍 Получить отчет"):
    with st.spinner("Генерация отчета..."):
        response = agent.run(query)
        st.markdown(response)  # сохраняет таблицы и форматирование
