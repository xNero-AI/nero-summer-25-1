import streamlit as st
from utils import response

st.title("Gabi Chat ̶a̶")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    #######
    
    # Exibe a mensagem do usuário imediatamente
    with st.chat_message("user"):
        st.markdown(prompt)
        
        
    # chat_response = response(prompt)
    # st.session_state.messages.append({"role": "assistant", "content": chat_response})
    
    # Display user message in chat message container
    with st.chat_message("assistant"):
        chat_response = st.write_stream(response(prompt)) 
        # st.markdown(chat_response)
    st.session_state.messages.append({"role": "assistant", "content": chat_response})