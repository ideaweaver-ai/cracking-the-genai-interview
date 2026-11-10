import uuid
import requests
import streamlit as st

N8N_WEBHOOK_URL = "https://ideaweavercloud.app.n8n.cloud/webhook-test/99a8b300-69a8-4515-812b-31472e7d8095"  # use your n8n production webhook URL

# page header
st.title("🤖 My Smart Helper")
st.subheader("Here's what I can do for you")

st.markdown("""
1. Answer general questions using web search.
2. Schedule events and meetings on your calendar.
3. Read, summarize and reply to your emails.
4. Keep track of your to-do list.
5. Jot down quick notes.
6. Log your spending and help with budgeting.
""")

st.subheader("💬 Start a conversation")

# set up conversation history and a session id for the agent's memory
if "chat_log" not in st.session_state:
    st.session_state.chat_log = []
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# replay earlier messages
for entry in st.session_state.chat_log:
    with st.chat_message(entry["role"]):
        st.markdown(entry["content"])

# input box
prompt_text = st.chat_input("Type your message here...")

if prompt_text:
    # show and store the user's message
    with st.chat_message("user"):
        st.markdown(prompt_text)
    st.session_state.chat_log.append({"role": "user", "content": prompt_text})

    # forward the message to the n8n webhook
    try:
        api_reply = requests.post(
            N8N_WEBHOOK_URL,
            json={"message": prompt_text, "sessionId": st.session_state.session_id},
            timeout=120,
        )
        api_reply.raise_for_status()
        bot_answer = api_reply.text
    except requests.RequestException as err:
        bot_answer = f"Sorry, I couldn't reach the assistant: {err}"

    # show and store the assistant's answer
    with st.chat_message("assistant"):
        st.markdown(bot_answer)
    st.session_state.chat_log.append({"role": "assistant", "content": bot_answer})
