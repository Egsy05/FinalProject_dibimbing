import streamlit as st
import pandas as pd
import altair as alt
import streamlit.components.v1 as com
from streamlit_option_menu import option_menu

selected = option_menu(
    menu_title=None,
    options=['Home','About','Analysis','Clusters'],
    icons=['house','info','graph-up','globe'],
    default_index=0,
    orientation='horizontal'
)
if selected == 'Home':
    st.balloons()
    st.title("Welcome! "
            "Here is my analysis about the steam games, "
            "from 2008 to 2023")
    st.markdown("Did **YOU** know, that there are over **70.000** games in steam!")
    st.header("About the Data")

    st.write("Our data has been engineered to become easy to read and understand, "
            "you click this link below to lookup to the original data.")
    st.link_button("Data","https://www.kaggle.com/datasets/mexwell/steamgames")

    data = pd.read_csv('games_.csv')

    name_to_search = st.text_input('Search your game here:')
    if name_to_search.strip() == '':
        st.dataframe(data)
    else:
        filtered_df = data[data['Name'].str.contains(name_to_search, case=False, na=False)]
        if not filtered_df.empty:
            st.write('Is this what you looking for? ')
            st.dataframe(filtered_df)
        else:
            st.write('No results found.')

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

elif selected == 'About':
    st.header('About the Project!')

    st.subheader('What is Steam?', divider='blue')
    st.write('Some people already know that steam is a platform for games and other application for computer. '
            'In this episode, we will talk about games that are in steam. '
            'You can download many games in any category that suite you, and of course you need to pay first. '
            'Some of the games are free and it called *free to play*. '
            'Many people love free games and '
            'some of them have no problem buying the games that they want. '
            'This bring up to the story of game prices')

    st.subheader('Why we need to analyze steam game?',divider='blue')
    st.write('There are two simple type of prices in steam game, '
            'There are free games and paid games. '
            'The majority of people love free stuff but is that also included in games that are provided in steam?'
            "If it is, then why do they want it? If not, why they don't want it?")

    st.subheader("Who is most favorite? free games or paid games", divider='blue')
    st.write("In this question, we will find out whether the free game is the most favorite or not"
            "If yes, then many game developers and publisher would likely to post new free games,"
            "but if not then the opposite")
if selected == "Analysis":
    data = pd.read_csv("new_games_full.csv")
    data = data.drop(columns=['Supported languages','Full audio languages'])

    st.header("So what do we get from our data...",divider='blue')

    st.subheader("Here is our developers with the most users")
    a = data.groupby(['Developers']).agg(count_user=('Peak CCU','sum')).sort_values(by='count_user',ascending=False).head(10).reset_index()
    st.altair_chart(alt.Chart(a)
        .mark_bar(orient='horizontal')
        .encode(
            x='count_user',
            y=alt.Y('Developers').sort('-x'),
        ),
        use_container_width=True)

    st.subheader("Publisher with the most users")
    b = data.groupby(['Publishers']).agg(count_user=('Peak CCU','sum')).sort_values(by='count_user',ascending=False).head(10).reset_index()
    st.altair_chart(alt.Chart(b)
        .mark_bar(orient='horizontal')
        .encode(
            x='count_user',
            y=alt.Y('Publishers').sort('-x'),
        ),
        use_container_width=True)

    st.write(" **INTRRESTING**! Turns out one of the Developers are also the Publishers!")

    st.subheader("Now let see if their profit are also as high as their users!")
    data['Profit'] = data['Peak CCU']*data['Price']
    c = data.groupby(['Developers']).agg(total_user = ('Peak CCU','sum'),profit = ('Profit','sum')).sort_values('profit',ascending=False).head(10).reset_index()
    d = data.groupby(['Publishers']).agg(users = ('Peak CCU','sum'),profit = ('Profit','sum')).sort_values('profit',ascending=False).head(10).reset_index()

    st.write("Developers Profit")
    st.altair_chart(alt.Chart(c)
        .mark_bar(orient='horizontal')
        .encode(
            x='profit',
            y=alt.Y('Developers').sort('-x'),
        ),
        use_container_width=True)

    st.write("Publishers Profit")
    st.altair_chart(alt.Chart(d)
        .mark_bar(orient='horizontal')
        .encode(
            x='profit',
            y=alt.Y('Publishers').sort('-x'),
        ),
        use_container_width=True)

    st.text("Is there any Developers or Publishers you know? "
             "If you do, you should be proud!")
    st.text("because of you, they made it to top 10 :)")

    st.write("")

    st.subheader("Now This is the game that made by our Developers with high users", divider='blue')
    f = data[data['Developers'].isin(a['Developers'].values)]
    g = f[['Developers','Name','Peak CCU','Price','Profit']]
    unique_value_dev = g['Developers'].unique()
    selected_dev = st.selectbox('Search Developer',list(unique_value_dev), index=None,placeholder= "Find Developer")
    price_dev = st.radio("Filter Price Developers",["All", "Paid", "Free"],captions = ["All Price", "Paid Games", "Free to Play"])
    if  selected_dev:
        filter_result = g[g['Developers']==selected_dev]
        if price_dev == "All":
            st.write(filter_result)
        elif price_dev == "Paid":
            filter_result = filter_result[filter_result['Price']!=0]
            st.write(filter_result)
        elif price_dev == "Free":
            filter_result = filter_result[filter_result['Price']==0]
            st.write(filter_result)
    else :
        filter_result = g
        if price_dev == "All":
            st.write(filter_result)
        elif price_dev == "Paid":
            filter_result = filter_result[filter_result['Price']!=0]
            st.write(filter_result)
        elif price_dev == "Free":
            filter_result = filter_result[filter_result['Price']==0]
            st.write(filter_result)

    st.subheader("This the games that are published by our Publishers with high users", divider='blue')
    h = data[data['Publishers'].isin(b['Publishers'].values)]
    i = h[['Publishers','Name','Peak CCU','Price','Profit']]
    unique_value_pub = i['Publishers'].unique()
    selected_pub = st.selectbox('Search Publishers',list(unique_value_pub), index=None,placeholder= "Find Publishers")
    price_pub = st.radio("Filter Price Publishers",["All", "Paid", "Free"],captions = ["All Price", "Paid Games", "Free to Play"])
    if  selected_pub:
        filter_result = i[i['Publishers']==selected_pub]
        if price_pub == "All":
            st.write(filter_result)
        elif price_pub == "Paid":
            filter_result = filter_result[filter_result['Price']!=0]
            st.write(filter_result)
        elif price_pub == "Free":
            filter_result = filter_result[filter_result['Price']==0]
            st.write(filter_result)
    else :
        filter_result = i
        if price_pub == "All":
            st.write(filter_result)
        elif price_pub == "Paid":
            filter_result = filter_result[filter_result['Price']!=0]
            st.write(filter_result)
        elif price_pub == "Free":
            filter_result = filter_result[filter_result['Price']==0]
            st.write(filter_result)

elif selected == 'Clusters':
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