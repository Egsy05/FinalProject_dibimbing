import streamlit as st
import pandas as pd
import altair as alt

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