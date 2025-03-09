import streamlit as st
import ssl
import time
import random

from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px

# Temporary SSL workaround
ssl._create_default_https_context = ssl._create_unverified_context

# Title and question
st.title("Ballon d'Or Winners")

st.markdown("""
This app shows two different visualizations to answer a question and observe which is more efficient.
Please read the question below and then click the button to see a randomly selected chart.
""")

st.header("Question")
st.markdown("**Which football player has the most Ballon d'Ors?**")

# Connect to Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(spreadsheet="https://docs.google.com/spreadsheets/d/1GCrhuVbC3_8qiFsnLxaDEYSy_iDgFLvuQn74YxRaHvw/edit?gid=0#gid=0")

# Define two charts
def chart_a(dataframe):
    """Chart A: Horizontal Bar Chart"""
    st.subheader("Chart A: Horizontal Bar Chart")
    fig = px.bar(
        dataframe,
        x="Ballon D'Ors",            # x-axis is the numeric column
        y="Football Players",        # y-axis is the categorical column
        orientation='h',            # horizontal orientation
        title="Ballon d'Ors by Player (Horizontal Bar)"
    )
    st.plotly_chart(fig)

def chart_b(dataframe):
    """Chart B: Pie Chart"""
    st.subheader("Chart B: Pie Chart")
    fig = px.pie(
        dataframe,
        names="Football Players",
        values="Ballon D'Ors",
        title="Distribution of Ballon d'Ors"
    )
    st.plotly_chart(fig)

# Initialize session state
if "chart_chosen" not in st.session_state:
    st.session_state["chart_chosen"] = None
if "start_time" not in st.session_state:
    st.session_state["start_time"] = 0

# First button: show random chart
if st.button("Show me a chart!"):
    st.session_state["chart_chosen"] = random.choice(["A", "B"])
    st.session_state["start_time"] = time.time()

# If a chart is chosen, display it and the second button
if st.session_state["chart_chosen"] is not None:
    if st.session_state["chart_chosen"] == "A":
        chart_a(df)
    else:
        chart_b(df)

    if st.button("I answered your question"):
        end_time = time.time()
        duration = end_time - st.session_state["start_time"]
        st.write(f"It took you **{duration:.2f} seconds** to answer the question!")
