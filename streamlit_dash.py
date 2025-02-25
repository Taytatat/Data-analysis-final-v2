import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
#import matplotlib.pyplot as plt
#import seaborn as sns


st.set_page_config(
    page_title="",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")



st.markdown("""
<style>

[data-testid="block-container"] {
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 1rem;
    padding-bottom: 0rem;
    margin-bottom: -7rem;
}

[data-testid="stVerticalBlock"] {
    padding-left: 0rem;
    padding-right: 0rem;
}

[data-testid="stMetric"] {
    background-color: #393939;
    text-align: center;
    padding: 15px 0;
}

[data-testid="stMetricLabel"] {
  display: flex;
  justify-content: center;
  align-items: center;
}

[data-testid="stMetricDeltaIcon-Up"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

[data-testid="stMetricDeltaIcon-Down"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

</style>
""", unsafe_allow_html=True)



df_reshaped = pd.read_csv('BLSdata.csv')

#st.set_page_config(page_title="BLS Data Dashboard", page_icon=":bar_chart:", layout="wide")  
st.title("BLS Data Dashboard")


st.sidebar.title("Filters")
selected_year = st.sidebar.selectbox("Select Year", data['year'].unique())
selected_period = st.sidebar.selectbox("Select Period", data['period'].unique())
selected_seriesID = st.sidebar.selectbox("Select Series ID", data['seriesID'].unique())


filtered_data = data[(data['year'] == selected_year) & (data['period'] == selected_period) & (data['seriesID'] == selected_seriesID)]


col1, col2 = st.columns(2)  


with col1:
    st.subheader("Line Chart")
    fig = px.line(filtered_data, x='year', y='value', title="Value Over Time")
    st.plotly_chart(fig, use_container_width=True)  


with col2:
    st.subheader("Data Table")
    st.dataframe(filtered_data, use_container_width=True)


st.subheader("Interactive Chart")
fig2 = px.scatter(data, x='year', y='value', color='seriesID', hover_data=['period'])
st.plotly_chart(fig2, use_container_width=True)
