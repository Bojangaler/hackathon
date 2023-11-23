from streamlit_authenticator import Authenticate
import streamlit as st
from pinecone_vector_store import get_retriever
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
import time


GPT_MODEL = "gpt-3.5-turbo-1106"


def render_main_content(authenticator: Authenticate, name: str) -> None:
    with st.sidebar:
        st.write(f"Welcome *{name}*")
        openai_api_key = st.text_input(
            "OpenAI API Key", key="chatbot_api_key", type="password"
        )
        authenticator.logout("Logout", "sidebar")

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    retriever = get_retriever()

    if prompt := st.chat_input():
        if not openai_api_key:
            st.info("Please add your OpenAI API key to continue.")
            st.stop()

        openai_model = ChatOpenAI(api_key=openai_api_key, model=GPT_MODEL)

        if not st.session_state["chat_memory"]:
            st.session_state["chat_memory"] = ConversationBufferMemory(
                memory_key="chat_history", return_messages=True
            )
        memory = st.session_state["chat_memory"]
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=openai_model,
            memory=memory,
            retriever=retriever,
            get_chat_history=lambda h: h,
            verbose=True,
        )

        if prompt := st.chat_input("How can I help you?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.spinner("Generating an answer..."):
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    full_response = ""
                    response = qa_chain({"question": prompt})  # QA chain
                    for response in response["answer"]:
                        full_response += response
                        time.sleep(0.02)
                        message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
                st.session_state.messages.append(
                    {"role": "assistant", "content": full_response}
                )
        # st.session_state.messages.append({"role": "user", "content": prompt})
        # st.chat_message("user").write(prompt)
        # response = client.chat.completions.create(
        #     model=GPT_MODEL, messages=st.session_state.messages
        # )
        # msg = response.choices[0].message.content
        # st.session_state.messages.append({"role": "assistant", "content": msg})
        # st.chat_message("assistant").write(msg)
