import io
import sys
import streamlit as st
from agno.agent import Agent
from agno.models.deepseek import DeepSeek
from agno.tools.reasoning import ReasoningTools
from agno.tools.yfinance import YFinanceTools

st.set_page_config(page_title="Финансовый Анализ", layout="wide")
st.title("📈 Инвестиционные рекомендации")

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

query = st.text_area(
    "Введите ваш вопрос:",
    value="Выведи перспективные компании, объясни, почему. Какие прогнозы. Что покупать, продавать?",
    height=150,
)

if st.button("🔍 Получить ответ"):
    placeholder = st.empty()
    with st.spinner("Анализируем данные..."):

        # Перехватываем stdout
        buffer = io.StringIO()
        sys_stdout = sys.stdout
        sys.stdout = buffer

        try:
            # Вызываем print_response с stream=True — вывод попадет в buffer
            agent.print_response(
                query,
                stream=True,
                show_full_reasoning=True,
                stream_intermediate_steps=True,
            )
        finally:
            sys.stdout = sys_stdout

        # Получаем весь вывод
        full_output = buffer.getvalue()

        # Выводим в Streamlit
        placeholder.markdown(full_output, unsafe_allow_html=True)
