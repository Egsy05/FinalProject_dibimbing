import streamlit as st
import pandas as pd

data = pd.read_csv("games_.csv")

st.header("This is the clusters for All games in Steam from 2008 to 2023", divider='blue')
cluster_value = data['clusters'].unique()
select_clusters = st.multiselect("Select Cluster",cluster_value)
if select_clusters:
    filter_table = data[data['clusters'].isin(select_clusters)]
    st.write(filter_table)
else:
    filter_table = data
    st.write(filter_table)

st.scatter_chart(filter_table, x='Positive_Negative_dif', y='Peak CCU', color='Name',size='days_since_release')