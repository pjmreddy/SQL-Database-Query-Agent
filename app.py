import streamlit as st
from pathlib import Path
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain.agents.agent_types import AgentType
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_groq import ChatGroq
import re
from db_utils import DatabaseManager
from table_formatter import format_query_results, format_as_markdown

st.set_page_config(
    page_title="SQL Agent", 
    layout="wide"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #4527A0;
        text-align: center;
        margin-bottom: 1rem;
    }
    .subheader {
        font-size: 1.2rem;
        color: #5E35B1;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton button {
        background-color: #673AB7;
        color: white;
        border-radius: 5px;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    }
    .sidebar .stButton button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🔍 SQL Database Query Agent</h1>', unsafe_allow_html=True)
st.markdown('<p class="subheader">Ask questions about your database</p>', unsafe_allow_html=True)

db_manager = DatabaseManager()

with st.sidebar:
    st.markdown("### Database Connection")
    st.markdown("---")
    database_options = ["Connect to SQLite Database (company.db)", "Connect to External MySQL Database"]
    selected_database = st.radio(label="Select Database Type", options=database_options, label_visibility="collapsed")
    
    if database_options.index(selected_database) == 1:
        connection_type = DatabaseManager.MYSQL
        with st.expander("MySQL Connection Details", expanded=True):
            mysql_host = st.text_input("Host Address")
            mysql_user = st.text_input("Username")
            mysql_password = st.text_input("Password", type="password")
            mysql_database = st.text_input("Database Name")
        
        if all([mysql_host, mysql_user, mysql_password, mysql_database]):
            try:
                database = db_manager.get_connection(
                    connection_type,
                    host=mysql_host,
                    user=mysql_user,
                    password=mysql_password,
                    db_name=mysql_database
                )
            except Exception as e:
                st.sidebar.error(f"Failed to connect to MySQL database: {str(e)}")
                st.stop()
        else:
            st.sidebar.info("Please provide all MySQL connection details")
            database = None
    else:
        connection_type = DatabaseManager.SQLITE
        try:
            database = db_manager.get_connection(connection_type)
            st.sidebar.success("Connected to SQLite database")
        except Exception as e:
            st.sidebar.error(f"Failed to connect to SQLite database: {str(e)}")
            st.stop()

st.sidebar.markdown("---")
st.sidebar.markdown("### API Configuration")
llm_api_key = st.sidebar.text_input(label="Groq API Key", type="password")

if not llm_api_key:
    st.sidebar.warning("⚠️ Please enter your Groq API key to continue")
    st.info("Enter your Groq API key in the sidebar to get started")
    st.stop()

language_model = ChatGroq(groq_api_key=llm_api_key, model_name="Llama3-8b-8192", streaming=True)

if database:
    sql_toolkit = SQLDatabaseToolkit(db=database, llm=language_model)
    
    sql_agent = create_sql_agent(
        llm=language_model,
        toolkit=sql_toolkit,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        handle_parsing_errors=True,
    )
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.markdown("### Chat Options")
    with col2:
        if st.button("🗑️ Clear History", key="clear_history"):
            st.session_state["chat_history"] = [{"role": "assistant", "content": "How can I help you with your database today?"}]
            st.rerun()
    
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = [{"role": "assistant", "content": "How can I help you with your database today?"}]
    
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.chat_history:
            role = message["role"]
            content = message["content"]
            with st.chat_message(role):
                st.markdown(f"<div class='{role}-message'>{content}</div>", unsafe_allow_html=True)
    
    user_message = st.chat_input(placeholder="Ask a question about your database...")
    
    if user_message:
        st.session_state.chat_history.append({"role": "user", "content": user_message})
        with st.chat_message("user"):
            st.markdown(f"<div class='user-message'>{user_message}</div>", unsafe_allow_html=True)
        
        with st.chat_message("assistant"):
            callback_handler = StreamlitCallbackHandler(st.container())
            agent_response = sql_agent.run(user_message, callbacks=[callback_handler])
            
            formatted_response = agent_response
            sql_result_pattern = r"\[\(.*?\)\]|\(\(.*?\)\)|\[(\d+, '[^']*'(?:, '[^']*')*(?:, \d+)*)\]"
            
            if "The result set is:" in agent_response and "[(" in agent_response and ")]" in agent_response:
                result_section = re.search(r"The result set is:\s*\n*(.+?)(?:\n\n|$)", agent_response, re.DOTALL)
                if result_section:
                    results_str = result_section.group(1).strip()
                    try:
                        results = eval(results_str)
                        if isinstance(results, list) and len(results) > 0:
                            df = format_query_results(results)
                            formatted_response = agent_response.replace(results_str, "[Results formatted as table below]")
                            st.markdown(f"<div class='assistant-message'>{formatted_response}</div>", unsafe_allow_html=True)
                            st.dataframe(df, use_container_width=True, hide_index=True)
                            with st.expander("📋 View as Markdown"):
                                st.markdown(format_as_markdown(results))
                            st.session_state.chat_history.append({"role": "assistant", "content": formatted_response})
                    except Exception as e:
                        st.session_state.chat_history.append({"role": "assistant", "content": agent_response})
                        st.markdown(f"<div class='assistant-message'>{agent_response}</div>", unsafe_allow_html=True)
            elif re.search(sql_result_pattern, agent_response):
                results_str = re.search(sql_result_pattern, agent_response).group(0)
                try:
                    results = eval(results_str)
                    if isinstance(results, list) and len(results) > 0:
                        df = format_query_results(results)
                        formatted_response = re.sub(sql_result_pattern, "[Results formatted as table below]", agent_response)
                        st.markdown(f"<div class='assistant-message'>{formatted_response}</div>", unsafe_allow_html=True)
                        st.dataframe(df, use_container_width=True, hide_index=True)
                        with st.expander("📋 View as Markdown"):
                            st.markdown(format_as_markdown(results))
                        st.session_state.chat_history.append({"role": "assistant", "content": formatted_response})
                except:
                    st.session_state.chat_history.append({"role": "assistant", "content": agent_response})
                    st.markdown(f"<div class='assistant-message'>{agent_response}</div>", unsafe_allow_html=True)
            else:
                st.session_state.chat_history.append({"role": "assistant", "content": agent_response})
                st.markdown(f"<div class='assistant-message'>{agent_response}</div>", unsafe_allow_html=True)
else:
    st.warning("Please configure your database connection in the sidebar to continue")
    st.info("Once connected, you can ask questions about your database in natural language")
    
    st.markdown("### Example Queries")
    example_queries = [
        "List all employees and their departments",
        "What is the average salary by department?",
        "Show me the projects with the highest budget",
        "Which clients are in the technology industry?"
    ]
    
    for query in example_queries:
        st.markdown(f"- {query}")