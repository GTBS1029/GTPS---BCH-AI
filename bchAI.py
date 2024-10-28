from openai import OpenAI
import streamlit as st
import time

st.title("부천고 챗봇")

if "api_key" not in st.session_state:
    st.session_state["api_key"] = st.text_input("OpenAI API 키를 입력하세요:", type="password")
    if st.session_state["api_key"]:
        st.success("API 키가 설정되었습니다.")
else:
    client = OpenAI(api_key=st.session_state["api_key"])

with st.sidebar:
    "[부천고등학교 홈페이지](https://bch-h.goebc.kr/bch-h/main.do)"

    thread_id = st.text_input("쓰레드 ID")

    thread_btn = st.button("쓰레드 만들기")

    if thread_btn:
        thread = client.beta.threads.create()
        thread_id = thread.id

        st.subheader(f"{thread_id}", divider="rainbow")
        st.info("쓰레드가 생성되었습니다.")

assistant_id = "asst_QcmomMBaccpaVZaiAfRMOsSg"

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "ft:gpt-4o-mini-2024-07-18:personal:bucheon-6:A716KZkt"

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "부천고에 대해 궁금 한 것이 있으신가요?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not thread_id:
        st.info("쓰레드 아이디를 추가해 주세요")
        st.stop()
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    thread_message = client.beta.threads.messages.create(
        thread_id,
        role="user",
        content=prompt,
    )

    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id
    )

    run_id = run.id
    while True:
        run = client.beta.threads.runs.retrieve(
        thread_id=thread_id,
        run_id=run_id
        )
        if run.status == "completed":
            break
        else:
            time.sleep(0.1)

    thread_message = client.beta.threads.messages.list(thread_id)

    msg= thread_message.data[0].content[0].text.value

    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)
