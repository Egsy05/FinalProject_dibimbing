import streamlit as st

import pandas as pd
import altair as alt
from streamlit.components.v1 import html
# st.markdown("""
# <style>
# .st-emotion-cache-6q9sum.ef3psqc4
# {
#             visibility: hidden;
# }
# .st-emotion-cache-ch5dnh.ef3psqc5
# {
#             visibility: hidden;
# }
# </style>
# """, unsafe_allow_html=True)
#this only for removing part in web that we didn't want to

st.balloons()
st.title("Welcome! "
         "Here is my analysis about the steam games, "
         "from 2008 to 2023")
st.markdown("Did **YOU** know, that there are over **70.000** games in steam!")
st.header("About the Data")

st.write("Our data has been engineered to become easy to read and understand, "
        "you click this link below to lookup to the original data.")
data_url = st.markdown("[Source data!](https://www.kaggle.com/datasets/mexwell/steamgames)")

data = pd.read_csv('games_cluster.csv')

name_to_search = st.text_input('Search your game here:')
if st.button('Search'):
    # If the input name_to_search is empty, show the original DataFrame
    if name_to_search.strip() == '':
        st.dataframe(data)
    else:
        # Filter the DataFrame based on the input name
        filtered_df = data[data['Name'].str.contains(name_to_search, case=False, na=False)]
        
        # Display the filtered DataFrame
        if not filtered_df.empty:
            st.write('Is this what you looking for? ')
            st.dataframe(filtered_df)
        else:
            st.write('No results found.')
st.write("You can click search to display all games!")
st.subheader("Highest user games!", divider='blue')

x = data.groupby(['Name']).agg(users=('Peak CCU','sum')).sort_values('users',ascending=False).head(10).reset_index()

st.altair_chart(alt.Chart(x)
    .mark_bar(orient='horizontal')
    .encode(
        x='users',
        y=alt.Y('Name').sort('-x'),
    ),
    use_container_width=True)


st.subheader("About The Author", divider='blue')
st.write('Fadllun Amir Alfitri, is an Electrical Engineering Bachelor from University of Muhammadiyah Malang. ' 
         'Dedicated in Data Analytic and Data Science. '
         'Since IT has become more contribute in many company and had a high demand, '
         'Fadllun decided to learn about computer science and coding, '
         'leading to data science hopping as a career starter in the world of IT')


st.write("## Thank you for visiting!")
st.image('thump up cat.png',width=500)
# x = st.text_input("Apa kabar? ")
# st.write(f"Kabar kamu, {x}")

# st.subheader("Cluster 0")
# cluster_0 = data[data['clusters']==0]
# st.write(cluster_0)

# st.subheader("Cluster 1")
# cluster_1 = data[data['clusters']==1]
# st.write(cluster_1)

# st.subheader("Cluster 2")
# cluster_2 = data[data['clusters']==2]
# st.write(cluster_2)

# st.subheader("Cluster 3")
# cluster_3 = data[data['clusters']==3]
# st.write(cluster_3)

# st.subheader("Cluster 4")
# cluster_4 = data[data['clusters']==4]
# st.write(cluster_4)

# st.markdown("# Data Analysis App")
# #searh for markdown syntax for more information
#learn about markdown in markdown cheatsheet

# st.write("We are so glad to see you here. ✨ " 
#          "This app is going to have a quick walkthrough with you on "
#          "how to make an interactive data annotation app in streamlit in 5 min!")

# st.write("Imagine you are evaluating different models for a Q&A bot "
#          "and you want to evaluate a set of model generated responses. "
#         "You have collected some user data. "
#          "Here is a sample question and response set.")

# data = {
#     "Questions": 
#         ["Who invented the internet?"
#         , "What causes the Northern Lights?"
#         , "Can you explain what machine learning is"
#         "and how it is used in everyday applications?"
#         , "How do penguins fly?"
#     ],           
#     "Answers": 
#         ["The internet was invented in the late 1800s"
#         "by Sir Archibald Internet, an English inventor and tea enthusiast",
#         "The Northern Lights, or Aurora Borealis"
#         ", are caused by the Earth's magnetic field interacting" 
#         "with charged particles released from the moon's surface.",
#         "Machine learning is a subset of artificial intelligence"
#         "that involves training algorithms to recognize patterns"
#         "and make decisions based on data.",
#         " Penguins are unique among birds because they can fly underwater. "
#         "Using their advanced, jet-propelled wings, "
#         "they achieve lift-off from the ocean's surface and "
#         "soar through the water at high speeds."
#     ]
# }

# df = pd.DataFrame(data)

# st.write(df)

# st.write("Now I want to evaluate the responses from my model. "
#          "One way to achieve this is to use the very powerful `st.data_editor` feature. "
#          "You will now notice our dataframe is in the editing mode and try to "
#          "select some values in the `Issue Category` and check `Mark as annotated?` once finished 👇")

# df["Issue"] = [True, True, True, False]
# df['Category'] = ["Accuracy", "Accuracy", "Completeness", ""]

# new_df = st.data_editor(
#     df,
#     column_config = {
#         "Questions":st.column_config.TextColumn(
#             width = "medium",
#             disabled=True
#         ),
#         "Answers":st.column_config.TextColumn(
#             width = "medium",
#             disabled=True
#         ),
#         "Issue":st.column_config.CheckboxColumn(
#             "Mark as annotated?",
#             default = False
#         ),
#         "Category":st.column_config.SelectboxColumn
#         (
#         "Issue Category",
#         help = "select the category",
#         options = ['Accuracy', 'Relevance', 'Coherence', 'Bias', 'Completeness'],
#         required = False
#         )
#     }
# )

# st.write("You will notice that we changed our dataframe and added new data. "
#          "Now it is time to visualize what we have annotated!")

# st.divider()

# st.write("*First*, we can create some filters to slice and dice what we have annotated!")

# col1, col2 = st.columns([1,1])
# with col1:
#     issue_filter = st.selectbox("Issues or Non-issues", options = new_df.Issue.unique())
# with col2:
#     category_filter = st.selectbox("Choose a category", options  = new_df[new_df["Issue"]==issue_filter].Category.unique())

# st.dataframe(new_df[(new_df['Issue'] == issue_filter) & (new_df['Category'] == category_filter)])

# st.markdown("")
# st.write("*Next*, we can visualize our data quickly using `st.metrics` and `st.bar_plot`")

# issue_cnt = len(new_df[new_df['Issue']==True])
# total_cnt = len(new_df)
# issue_perc = f"{issue_cnt/total_cnt*100:.0f}%"

# col1, col2 = st.columns([1,1])
# with col1:
#     st.metric("Number of responses",issue_cnt)
# with col2:
#     st.metric("Annotation Progress", issue_perc)

# df_plot = new_df[new_df['Category']!=''].Category.value_counts().reset_index()

# st.bar_chart(df_plot, x = 'Category', y = 'count')

# st.write("Here we are at the end of getting started with streamlit! Happy Streamlit-ing! :balloon:")

