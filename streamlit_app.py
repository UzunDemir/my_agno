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
st.set_page_config(page_title="Финансовый AI-Аналитик", layout="wide")
st.title("📊 Финансовый AI-Аналитик")
st.markdown("Введите вопрос на русском или английском. Примеры: \
**'самый высокий рос в ближайшие 3 месяца'** или **'top stock gainers in 3 months'**")

query = st.text_input("🔎 Ваш вопрос к агенту:", "самый высокий рос в ближайшие 3 месяца")

if st.button("Сформировать отчет"):
    with st.spinner("⏳ Анализ данных..."):
        response = agent.run(query)
        st.markdown(response, unsafe_allow_html=True)  # сохраняет таблицы и markdown
