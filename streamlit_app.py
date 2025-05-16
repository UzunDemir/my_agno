import streamlit as st
from agno.agent import Agent
from agno.models.deepseek import DeepSeek
from agno.tools.reasoning import ReasoningTools
from agno.tools.yfinance import YFinanceTools

# --- Настройка агента ---
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

# --- Интерфейс Streamlit ---
st.set_page_config(page_title="Финансовый агент", layout="wide")
st.title("📈 Финансовый AI-агент на базе Agno")

user_input = st.text_area("Введите вопрос о компаниях, инвестициях, акциях и т.д.", height=150)

if st.button("Анализировать"):
    if user_input.strip() == "":
        st.warning("Пожалуйста, введите запрос.")
    else:
        with st.spinner("Агент анализирует данные..."):
            # Вывод ответа с промежуточными шагами
            response = agent.run(
                    user_input,
                    stream=False,
                    show_full_reasoning=True,
                    stream_intermediate_steps=True,
                )
            st.markdown(response)

