import streamlit as st
from utils.validator import check_emergency
from utils.logic import (
    generate_summary, get_next_question, get_dynamic_question, get_symptom_info
)

st.set_page_config(page_title="HealthAssist", page_icon="🩺")

# Theme (your colors)
st.markdown(
    """
    <style>
    .stApp {
        background-color: #F0F2F6;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session state
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.patient_data = {}
    st.session_state.messages = [
        {"role": "assistant", "content": get_next_question(0)}
    ]
    st.session_state.show_report = False

st.title("🩺 HealthAssist AI")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Type here..."):
    is_emergency, warning = check_emergency(prompt)

    st.session_state.messages.append({"role": "user", "content": prompt})

    if is_emergency:
        response = warning
    else:
        steps = ["name", "reason", "severity", "duration", "notes"]
        current_key = steps[st.session_state.step]
        st.session_state.patient_data[current_key] = prompt

        # If symptom entered, give extra helpful info
        if st.session_state.step == 1:  # After reason
            info, reco = get_symptom_info(prompt)
            if info:
                response = f"ℹ️ **About this symptom:** {info}\n\n"
                response += get_dynamic_question(prompt)
            else:
                response = get_dynamic_question(prompt)
        else:
            st.session_state.step += 1
            if st.session_state.step < len(steps):
                response = get_next_question(st.session_state.step)
            else:
                response = "All set! Click **Generate Report** below."

    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

# Generate Report Button
if st.session_state.step >= 5:
    if st.button("📄 Generate Report"):
        st.session_state.show_report = True

if st.session_state.show_report:
    st.markdown("## 🏥 Your Report")
    st.write(generate_summary(st.session_state.patient_data))
