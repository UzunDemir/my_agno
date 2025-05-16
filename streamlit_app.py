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
st.title("🧠 Финансовый AI-Аналитик — Пошаговый вывод")

query = st.text_input("Введите вопрос:", "самый высокий рос в ближайшие 3 месяца")

if st.button("🚀 Запустить анализ"):
    with st.spinner("⏳ Анализируем..."):
        # Этот вызов возвращает словарь: {"final_response": ..., "intermediate_steps": [...]}
        result = agent.run(query, stream=False, return_steps=True)

        st.subheader("🧩 Пошаговое рассуждение:")
        for i, step in enumerate(result.get("intermediate_steps", [])):
            st.markdown(f"### Шаг {i+1}:")
            st.markdown(f"**Инструмент:** `{step['tool_name']}`")
            st.markdown(f"**Ввод:** {step['tool_input']}")
            st.markdown("**Вывод:**")
            st.markdown(step["tool_output"], unsafe_allow_html=True)
            st.markdown("---")

        st.subheader("📊 Финальный отчет:")
        st.markdown(result["final_response"], unsafe_allow_html=True)
