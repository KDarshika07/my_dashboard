import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# File paths
TASK_FILE = "tasks.json"
JOURNAL_FILE = "journal.json"
QUOTE_FILE = "quote.txt"

# Load/Save Functions
def load_json(file, default):
    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    return default

def save_json(data, file):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

# Task Functions
def load_tasks():
    return load_json(TASK_FILE, {
        "Mind Mastery": [],
        "Career Sculpting": [],
        "Identity & Self-Worth": [],
        "Soul Nourishment": []
    })

def save_tasks(tasks):
    save_json(tasks, TASK_FILE)

# Journal Functions
def load_journal():
    return load_json(JOURNAL_FILE, [])

def save_journal(journal):
    save_json(journal, JOURNAL_FILE)

# Quote
def load_quote():
    if os.path.exists(QUOTE_FILE):
        with open(QUOTE_FILE, "r") as f:
            return f.read()
    return "What you seek is seeking you. – Rumi"

# Set page layout
st.set_page_config(page_title="Darshika's Growth Dashboard", layout="wide")

# Load state
if "tasks" not in st.session_state:
    st.session_state.tasks = load_tasks()
if "journal" not in st.session_state:
    st.session_state.journal = load_journal()

# Sidebar Resources
st.sidebar.title("Tools & Resources")
st.sidebar.markdown("""
- [Matplotlib Guide](https://realpython.com/python-matplotlib-guide/)  
- [Seaborn Cheat Sheet](https://datacamp-community-prod.s3.amazonaws.com/69f4cfd2-52b8-4c10-8c61-6b0a6b4d8a2f)  
- [Pandas Visualization](https://pandas.pydata.org/docs/user_guide/visualization.html)  
- [Plotly Python](https://plotly.com/python/)
""")

pillar = st.sidebar.selectbox(
    "Choose Section",
    ["Home", "Tasks", "Journal"]
)

# HOME PAGE
if pillar == "Home":
    st.title("Darshika's Growth Dashboard")
    st.subheader("Vision • Clarity • Power")
    st.markdown("### Your 5-Year Vision")
    st.markdown("""
    I see myself in a corner office, with a MacBook in front of me, files on the left and coffee on the right.  
    I’m a Data Science Partner at Deloitte. Charts speak to me — I find patterns others miss.  
    I live independently in a cozy-modern apartment with a traditional touch.  
    My passions — cooking, dancing, reading, pottery — are on another level.  
    I’m living my best, most aligned life.
    """)

    st.markdown("### Daily Affirmations")
    st.markdown("""
    - I am already enough.  
    - I do not need to be perfect to be loved or worthy.  
    - My past does not define my future.  
    - I have the power to create the life I dream of.  
    - I belong — exactly as I am.  
    - I choose courage over comfort.  
    - My uniqueness is my power.
    """)

    st.markdown("### Quote of the Day")
    st.info(load_quote())

# TASK SECTION
elif pillar == "Tasks":
    pillar_select = st.selectbox("Choose Growth Pillar", list(st.session_state.tasks.keys()))
    with st.form(f"add_task_{pillar_select}"):
        st.markdown(f"#### Add New Task - {pillar_select}")
        task_name = st.text_input("Task")
        task_due = st.date_input("Due Date", datetime.today())
        task_priority = st.selectbox("Priority", ["Low", "Medium", "High"])
        submitted = st.form_submit_button("Add Task")

        if submitted and task_name:
            st.session_state.tasks[pillar_select].append({
                "Task": task_name,
                "Due Date": str(task_due),
                "Priority": task_priority,
                "Status": "Not Started"
            })
            save_tasks(st.session_state.tasks)
            st.success("Task added!")

    st.markdown(f"#### {pillar_select} Tasks")
    if st.session_state.tasks[pillar_select]:
        df = pd.DataFrame(st.session_state.tasks[pillar_select])
        edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
        st.session_state.tasks[pillar_select] = edited_df.to_dict("records")
        save_tasks(st.session_state.tasks)
    else:
        st.info("No tasks yet. Add some above!")

    # Progress Bar
    total = sum(len(v) for v in st.session_state.tasks.values())
    done = sum(1 for v in st.session_state.tasks.values() for task in v if task["Status"] == "Completed")
    pct = done / total if total else 0
    st.sidebar.markdown("### Progress")
    st.sidebar.progress(pct)

# JOURNAL SECTION
elif pillar == "Journal":
    st.title("Your Journal")
    st.markdown("Write freely. This is your space for reflection.")

    with st.form("journal_entry"):
        today = datetime.now().strftime("%Y-%m-%d")
        entry = st.text_area("What’s on your mind today?")
        save = st.form_submit_button("Save Entry")

        if save and entry.strip():
            new_entry = {"date": today, "entry": entry}
            st.session_state.journal.append(new_entry)
            save_journal(st.session_state.journal)
            st.success("Entry saved.")

    if st.session_state.journal:
        st.markdown("### Past Entries")
        for j in reversed(st.session_state.journal[-5:]):
            st.markdown(f"**{j['date']}**")
            st.markdown(f"{j['entry']}")
            st.markdown("---")
