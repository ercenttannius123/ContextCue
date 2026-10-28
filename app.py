import streamlit as st
from llm_client import generate_response
from context_extractor import extract_context
from context_tracker import (
    create_empty_context,
    update_context
)

st.set_page_config(
    page_title="ContextCue",
    page_icon="🎬"
)
st.title("🎬 ContextCue")
st.caption("Context-Aware Movie Dialogue System")


if "messages" not in st.session_state:
    st.session_state.messages = []

if "context" not in st.session_state:
    st.session_state.context = create_empty_context()

if st.button("New Conversation"):
    st.session_state.messages = []
    st.session_state.context = create_empty_context()
    st.rerun()


for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

user_input = st.chat_input(
    "Ask me anything about movies..."
)

if user_input:
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    # Prepare user message
    user_message = {
        "role": "user",
        "content": user_input
    }
    # Prepare conversation history
    pending_messages = (
        st.session_state.messages + [user_message]
    )

    updated_context = st.session_state.context.copy()
    with st.spinner("Analyzing conversation context..."):
        try:
            extracted_context = extract_context(
                user_input
            )
            updated_context = update_context(
                st.session_state.context,
                extracted_context
            )
        except Exception as error:
            st.warning(
                "Context extraction temporarily failed. "
                "Continuing with conversation history."
            )
            print(
                f"Context extraction error: {error}",
                flush=True
            )
    with st.chat_message("assistant"):
        with st.spinner("ContextCue is thinking..."):
            try:
                answer = generate_response(
                    pending_messages,
                    updated_context
                )
            except Exception as error:
                answer = None
                error_message = str(error)
                if (
                    "429" in error_message
                    or "RESOURCE_EXHAUSTED" in error_message
                ):
                    st.error(
                        "Gemini API rate limit reached. "
                        "Please wait a moment and try again."
                    )
                elif (
                    "503" in error_message
                    or "UNAVAILABLE" in error_message
                ):
                    st.error(
                        "Gemini is temporarily unavailable. "
                        "Please try again later."
                    )
                else:
                    st.error(
                        "Unable to generate a response. "
                        "Please try again."
                    )
                print(
                    f"Response generation error: {error}",
                    flush=True
                )

        if answer is not None:
            st.markdown(answer)
            # Save user message
            st.session_state.messages.append(
                user_message
            )
            # Save assistant response
            st.session_state.messages.append({
                "role": "assistant",
                "content": answer
            })
            # Save updated context
            st.session_state.context = updated_context

with st.expander("Current Conversation Context"):
    st.json(st.session_state.context)
