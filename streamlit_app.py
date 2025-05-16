import streamlit as st
from agno.agent import Agent
from agno.models.deepseek import DeepSeek
from agno.tools.reasoning import ReasoningTools
from agno.tools.yfinance import YFinanceTools

# Настройка страницы Streamlit
st.set_page_config(page_title="Анализ акций", layout="wide")
st.title("Анализ перспективных компаний")

# Инициализация агента
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

# Пользовательский ввод
user_query = st.text_area(
    "Введите ваш запрос о перспективных компаниях:",
    value="Выведи перспективные компании, объясни, почему. Какие прогнозы. Что покупать, продавать?",
    height=100
)

if st.button("Получить анализ"):
    # Создание контейнеров для вывода
    response_container = st.container()
    reasoning_container = st.expander("Подробный процесс анализа")
    
    # Обработка запроса
    with reasoning_container:
        st.write("Процесс анализа:")
        reasoning_placeholder = st.empty()
        
        def stream_callback(chunk):
            if 'intermediate_step' in chunk:
                reasoning_placeholder.markdown(f"**Шаг:** {chunk['intermediate_step']}")
            if 'reasoning' in chunk:
                reasoning_placeholder.markdown(chunk['reasoning'])
    
    with response_container:
        st.write("Результат анализа:")
        response_placeholder = st.empty()
        
        full_response = ""
        for chunk in agent.stream_response(
            user_query,
            stream=True,
            show_full_reasoning=True,
            stream_intermediate_steps=True,
            callback=stream_callback
        ):
            if 'response' in chunk:
                full_response += chunk['response']
                response_placeholder.markdown(full_response)
