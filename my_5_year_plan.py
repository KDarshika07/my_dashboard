import streamlit as st
import pandas as pd
from datetime import datetime

# Set page layout
st.set_page_config(page_title="Darshika's Growth Dashboard", layout="wide")

# Header
st.title("Darshika's Growth Dashboard")
st.subheader("Vision • Clarity • Power")

# Vision Section
st.markdown("## Your 5-Year Vision")
st.markdown("""
I see myself in a corner office, with a MacBook in front of me, files on the left and coffee on the right.  
I want to have my mind at work, which I’m so good at — it’s unbelievable!  
I’m a Data Science Partner at Deloitte. I know my craft so well, people don’t have to question me twice.  
The charts speak to me — I see insights in patterns no one else can.

I live independently in a cozy-modern apartment with a touch of tradition.  
My passions — cooking, dancing, reading, pottery — are on another level.  
I’m living my best, most aligned life.
""")

# Daily Affirmations
st.markdown("## Daily Affirmations")
st.markdown("""
- I am already enough.  
- I do not need to be perfect to be loved or worthy.  
- My past does not define my future.  
- I have the power to create the life I dream of.  
- I belong — exactly as I am.  
- I choose courage over comfort.  
- My uniqueness is my power.  
""")

# Sidebar - Resource Links (no Notion or ChatGPT)
st.sidebar.markdown("### Helpful Tools")
st.sidebar.markdown("""
- [Streamlit Documentation](https://docs.streamlit.io/)  
- [Matplotlib Visualization Guide](https://realpython.com/python-matplotlib-guide/)  
- [Seaborn Cheat Sheet](https://datacamp-community-prod.s3.amazonaws.com/69f4cfd2-52b8-4c10-8c61-6b0a6b4d8a2f)  
- [Pandas Visualization](https://pandas.pydata.org/docs/user_guide/visualization.html)  
- [Plotly for Interactive Charts](https://plotly.com/python/)  
""")

# Growth Pillar Selection
pillar = st.sidebar.selectbox(
    "Choose Growth Pillar",
    ["Mind Mastery", "Career Sculpting", "Identity & Self-Worth", "Soul Nourishment"]
)

# Initialize task tracker
if "tasks" not in st.session_state:
    st.session_state.tasks = {
        "Mind Mastery": [],
        "Career Sculpting": [],
        "Identity & Self-Worth": [],
        "Soul Nourishment": []
    }

# Add Task Section
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

# Display Tasks
st.markdown(f"### {pillar} Tasks")
if st.session_state.tasks[pillar]:
    df = pd.DataFrame(st.session_state.tasks[pillar])
    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
    st.session_state.tasks[pillar] = edited_df.to_dict('records')
else:
    st.info("No tasks yet. Add some above!")

# Progress Bar
total_tasks = sum(len(v) for v in st.session_state.tasks.values())
completed_tasks = sum(
    1 for v in st.session_state.tasks.values()
    for task in v if task["Status"] == "Completed"
)
progress = completed_tasks / total_tasks if total_tasks else 0
st.sidebar.markdown("### Progress Tracker")
st.sidebar.progress(progress)
