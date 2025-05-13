import streamlit as st
from agno.agent import Agent
from agno.embedder.huggingface import HuggingfaceCustomEmbedder
from agno.knowledge.url import UrlKnowledge
from agno.models.deepseek import DeepSeek
from agno.tools.reasoning import ReasoningTools
from agno.vectordb.pgvector import PgVector

@st.cache_resource
def load_agent():
    embedder = HuggingfaceCustomEmbedder()
    knowledge = UrlKnowledge(
        urls=["https://docs.agno.com/introduction/agents.md"],
        vector_db=PgVector(
            db_url=st.secrets["DB_URL"],
            table_name="huggingface_embeddings",
            embedder=embedder,
        )
    )
    agent = Agent(
        name="Agno Assist",
        model=DeepSeek(id="deepseek-chat"),
        instructions=[
            "Use tables to display data.",
            "Include sources in your response.",
            "Search your knowledge before answering the question.",
            "Only include the output in your response. No other text.",
        ],
        knowledge=knowledge,
        tools=[ReasoningTools(add_instructions=True)],
        add_datetime_to_instructions=True,
        markdown=True,
    )
    agent.knowledge.load(recreate=False)
    return agent

# UI
st.title("🤖 Agno Agent")
question = st.text_input("Введите ваш вопрос:")

if question:
    with st.spinner("Генерируем ответ..."):
        agent = load_agent()
        response = agent.chat(question)
        st.markdown(response)
