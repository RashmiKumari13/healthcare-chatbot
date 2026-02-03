import streamlit as st
from utils.validator import check_emergency
from utils.logic import generate_summary, get_next_question

st.set_page_config(page_title="HealthAssist", page_icon="🩺")

# Initialize data storage
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.patient_data = {}
    st.session_state.messages = [{"role": "assistant", "content": get_next_question(0)}]

st.title("🩺 HealthAssist Collector")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Type here..."):
    # 1. Check for emergency first!
    is_emergency, warning = check_emergency(prompt)
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if is_emergency:
        response = warning
    else:
        # 2. Save data based on the current step
        steps = ["name", "reason", "severity", "duration", "notes"]
        current_key = steps[st.session_state.step]
        st.session_state.patient_data[current_key] = prompt
        
        # 3. Move to next step
        st.session_state.step += 1
        
        if st.session_state.step < len(steps):
            response = get_next_question(st.session_state.step)
        else:
            response = generate_summary(st.session_state.patient_data)

    # 4. Show assistant response
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})