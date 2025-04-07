import streamlit as st
import pandas as pd
from datetime import datetime

# Set up layout
st.set_page_config(page_title="Darshika's Growth Dashboard", layout="wide")
st.title("Darshika's Personal Growth Dashboard")
st.subheader("5-Year Vision: Data Science Partner at Deloitte")

# Sidebar to select growth area
pillar = st.sidebar.selectbox(
    "Choose Growth Pillar",
    ["Mind Mastery", "Career Sculpting", "Identity & Self-Worth", "Soul Nourishment"]
)

# Initialize task store
if "tasks" not in st.session_state:
    st.session_state.tasks = {
        "Mind Mastery": [],
        "Career Sculpting": [],
        "Identity & Self-Worth": [],
        "Soul Nourishment": []
    }

# Add task form
with st.form(f"add_task_{pillar}"):
    st.markdown(f"### Add New Task - {pillar}")
    task_name = st.text_input("Task")
    task_due = st.date_input("Due Date", datetime.today())
    task_priority = st.selectbox("Priority", ["Low", "Medium", "High"])
    submitted = st.form_submit_button("Add Task")

    if submitted and task_name:
        st.session_state.tasks[pillar].append({
            "Task": task_name,
            "Due Date": task_due,
            "Priority": task_priority,
            "Status": "Not Started"
        })
        st.success("Task added!")

# Show tasks in editable table
st.markdown(f"### {pillar} Tasks")
if st.session_state.tasks[pillar]:
    df = pd.DataFrame(st.session_state.tasks[pillar])
    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
    st.session_state.tasks[pillar] = edited_df.to_dict('records')
else:
    st.info("No tasks added yet.")

# Progress bar
total = sum(len(v) for v in st.session_state.tasks.values())
done = sum(
    1 for tasks in st.session_state.tasks.values()
    for t in tasks if t["Status"] == "Completed"
)
progress = done / total if total else 0
st.sidebar.markdown("### Overall Progress")
st.sidebar.progress(progress)
