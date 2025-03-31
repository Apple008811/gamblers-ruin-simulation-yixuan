import streamlit as st
from api import get_chat_response

st.title("Gambler's Ruin Chat Interface")

# 添加介绍文本
st.write("""
Welcome to the Gambler's Ruin Chat Interface! You can ask questions about:
- Betting strategies
- Probability calculations
- Basic definitions and concepts
""")

# 创建聊天输入框
user_input = st.text_input("Ask a question about Gambler's Ruin:")

# 当用户输入问题时处理响应
if user_input:
    response = get_chat_response(user_input)
    st.write("Response:", response) 