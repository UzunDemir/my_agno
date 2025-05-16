import streamlit as st
from agno.agent import Agent
from agno.models.deepseek import DeepSeek
from agno.tools.reasoning import ReasoningTools
from agno.tools.yfinance import YFinanceTools

# Настройки Streamlit
st.set_page_config(page_title="Финансовый Анализ", layout="wide")
st.title("📈 Инвестиционные рекомендации")
st.markdown("Анализ перспективных компаний с помощью DeepSeek и YFinance.")

# Создание агента
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

# Ввод вопроса от пользователя
query = st.text_area(
    "Введите ваш вопрос:",
    value="Выведи перспективные компании, объясни, почему. Какие прогнозы. Что покупать, продавать?",
    height=150
)

if st.button("🔍 Получить ответ"):
    placeholder = st.empty()
    with st.spinner("Анализируем данные..."):
        output = ""
        try:
            for chunk in agent.stream_response(
                query,
                show_full_reasoning=True,
                stream_intermediate_steps=True
            ):
                # Обработка потока: chunk может быть строкой или словарем
                if isinstance(chunk, dict):
                    content = chunk.get("content", "")
                else:
                    content = str(chunk)

                output += content
                placeholder.markdown(output, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Произошла ошибка: {e}")
