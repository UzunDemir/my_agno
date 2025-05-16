# 1. АБСОЛЮТНО ПЕРВАЯ КОМАНДА В ФАЙЛЕ - ДО ЛЮБЫХ ИМПОРТОВ!
import streamlit as st
st.set_page_config(page_title="Анализ акций", layout="wide")

# 2. Основные импорты (после set_page_config)
from agno.agent import Agent
from agno.models.deepseek import DeepSeek
from agno.tools.reasoning import ReasoningTools
from agno.tools.yfinance import YFinanceTools

# 3. Инициализация агента (с кэшированием)
@st.cache_resource
def init_agent():
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

# 4. Основной интерфейс
def main():
    st.title("📈 Анализ перспективных компаний")
    
    with st.form("query_form"):
        query = st.text_area(
            "Введите запрос:",
            value="Выведи перспективные компании, объясни почему. Какие прогнозы? Что покупать/продавать?",
            height=100
        )
        submitted = st.form_submit_button("Анализировать")
    
    if submitted:
        agent = init_agent()
        
        with st.spinner("Анализируем данные..."):
            with st.expander("Детали анализа", expanded=False):
                reasoning = st.empty()
            
            result = st.empty()
            
            full_response = ""
            for chunk in agent.stream_response(
                query,
                stream=True,
                show_full_reasoning=True,
                stream_intermediate_steps=True
            ):
                if 'reasoning' in chunk:
                    reasoning.markdown(chunk['reasoning'])
                if 'response' in chunk:
                    full_response += chunk['response']
                    result.markdown(full_response)

if __name__ == "__main__":
    main()
