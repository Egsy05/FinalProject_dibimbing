import streamlit as st
import pandas as pd
import altair as alt
import streamlit.components.v1 as com
from streamlit_option_menu import option_menu
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import sigmoid_kernel

selected = option_menu(
    menu_title=None,
    options=['Home','Explore','Find','Summary'],
    icons=['house','airplane','binoculars','card-checklist'],
    default_index=0,
    orientation='horizontal'
)



#HOME PAGE
if selected == 'Home':
    st.balloons()
    st.title("Welcome! "
            "Here is my analysis about the steam games, "
            "from 2008 to 2023")
    st.markdown("Did **YOU** know, that there are over **70.000** games in steam!")

    st.header('About the Project!')



    #ABOUT STEAM
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
            'The majority of people love free stuff but is that also included in games that are provided in steam? '
            "If it is, then why do they want it? If not, why they don't want it?")

    st.subheader("Who is most favorite? free games or paid games", divider='blue')
    st.write("In this question, we will find out whether the free games is the most favorite or not"
            "If yes, then many game developers and publisher would likely to post new free games, "
            "but if not then the opposite")



    #ABOUT DATA
    st.header("About the Data")

    st.write("Our data has been engineered to become easy to read and understand, "
            "you can click the link below to go to the original data set.")
    st.link_button("Data","https://www.kaggle.com/datasets/mexwell/steamgames")



    #TRY SEARCHING GAMES
    data = pd.read_csv('new_games_full.csv')
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

    #TOP TRENDING GAMES
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



#EXPLORING PAGE
elif selected == 'Explore':
    data = pd.read_csv("new_games_full.csv")
    data1 = pd.read_csv("games_recommend_image_movies_website.csv")
    data = data.drop(columns=['Supported languages','Full audio languages'])
    data1 = data1.drop(columns=['Genres','Header image','Movies','Website'])

    st.header("Let's explore about steam! "
              "So what do we get from our data...",divider='blue')

    st.subheader("Developers and Publishers with the most users")
    st.write("")
    st.write("Top Developers by their Users")
    dev_data = data[['Name',
                    'Developers',
                    'Release date',
                    'Peak CCU',
                    'Price',
                    'Positive',
                    'Negative',
                    'Average playtime forever',
                    'Genres',
                    'Release_date_day',
                    'Release_date_month',
                    'Release date_year']]
    dev_data['Recommendations'] = data1['Recommendations']
    dev_data['Review_score'] = data['Positive']-data['Negative']
    dev_data['Estimate_users'] = data['Peak CCU']+data['Positive']+data['Negative']+data1['Recommendations']
    a = dev_data.groupby(['Developers']).agg(total_reco=('Recommendations','sum'),
                                             review=('Review_score','sum'),
                                             users=('Estimate_users','sum')).sort_values(by='users',ascending=False).head(10).reset_index()
    st.altair_chart(alt.Chart(a)
        .mark_bar(orient='horizontal')
        .encode(
            x='users',
            y=alt.Y('Developers').sort('-x'),
        ),
        use_container_width=True)
# 
# 
# 
# 
    st.write("Top Publishers by their Users")
    pub_data = data[['Name',
                    'Publishers',
                    'Release date',
                    'Peak CCU',
                    'Price',
                    'Positive',
                    'Negative',
                    'Average playtime forever',
                    'Genres',
                    'Release_date_day',
                    'Release_date_month',
                    'Release date_year']]
    pub_data['Recommendations'] = data1['Recommendations']
    pub_data['Review_score'] = data['Positive']-data['Negative']
    pub_data['Estimate_users'] = data['Peak CCU']+data['Positive']+data['Negative']+data1['Recommendations']
    b = pub_data.groupby(['Publishers']).agg(total_reco=('Recommendations','sum'),
                                             review=('Review_score','sum'),
                                             users=('Estimate_users','sum')).sort_values(by='users',ascending=False).head(10).reset_index()
    st.altair_chart(alt.Chart(b)
        .mark_bar(orient='horizontal')
        .encode(
            x='users',
            y=alt.Y('Publishers').sort('-x'),
        ),
        use_container_width=True)

    st.write(" **INTRRESTING**! Turns out one of the Developers are also the Publishers!")
    st.write("")
# 
# 
# 
    st.subheader("Now let see if their profit are also as high as their users!")
# 
# 
# 
    dev_data['Estimate_profit'] = dev_data['Estimate_users']*dev_data['Price']
    pub_data['Estimate_profit'] = pub_data['Estimate_users']*pub_data['Price']
    c = dev_data.groupby(['Developers']).agg(users = ('Estimate_users','sum'),profit = ('Estimate_profit','sum')).sort_values('profit',ascending=False).head(10).reset_index()
    d = pub_data.groupby(['Publishers']).agg(users = ('Estimate_users','sum'),profit = ('Estimate_profit','sum')).sort_values('profit',ascending=False).head(10).reset_index()
    rockstar = pub_data.groupby(['Publishers']).agg(users = ('Estimate_users','sum'),profit = ('Estimate_profit','sum')).sort_values('profit',ascending=False).reset_index()
# 
# 
    st.write("Before we continue our jurney let's have a little quiz!")
    st.text("From graph above, who do you thing in developers that have the highest profit?")
    answer_A = st.button("A. Valve")
    answer_B = st.button("B. Rockstar Games")
    answer_C = st.button("C. Ubisoft Montreal")
    answer_D = st.button("D. CD PROJEKT RED")

    if answer_A:
        st.subheader("Sorry, Wrong Answer :slightly_frowning_face: ")
        st.image("Valve-Logo-1996.png",width= 500)
        st.write(c[c['Developers']=='Valve'])
        st.write("**Valve** have total profit gross around 25 million dollars of all games that they have develop")
        st.write("Crazy that number still not the highest one...")
        st.write("Here is the Top Developers by their Profit!")
        st.altair_chart(alt.Chart(c)
            .mark_bar(orient='horizontal')
            .encode(
                x='profit',
                y=alt.Y('Developers').sort('-x'),
            ),
            use_container_width=True)

    elif answer_B:
        st.subheader("Sorry, Wrong Answer :slightly_frowning_face:")
        st.image("rockstar-games-logo.png",width= 500)
        st.write(rockstar[rockstar['Publishers']=='Rockstar Games'])
        st.write("**Rockstar Games** is not a developers! but **Rockstar North** is!") 
        st.write("They both are the same company but only have a different role")
        st.write("**Rockstar Games** have total gross profit around 11 million dollars")
        st.write("Here is the Top Developers by their Profit!")
        st.altair_chart(alt.Chart(c)
            .mark_bar(orient='horizontal')
            .encode(
                x='profit',
                y=alt.Y('Developers').sort('-x'),
            ),
            use_container_width=True)
        
    elif answer_C:
        st.subheader("Sorry, Wrong Answer :slightly_frowning_face:")
        st.image("Ubisoft-Logo.png",width= 500)
        st.write(c[c['Developers']=='Ubisoft Montreal'])
        st.write("**Ubisoft Montreal** has total gross profit around 60 Million Dollars")
        st.write("Here is the Top Developers by their Profit!")
        st.altair_chart(alt.Chart(c)
            .mark_bar(orient='horizontal')
            .encode(
                x='profit',
                y=alt.Y('Developers').sort('-x'),
            ),
            use_container_width=True)
        
    elif answer_D:
        st.subheader("That's Right! :smile:")
        st.image("CD-PROJEKT-RED-Logo.png",width= 500)
        st.write(c[c['Developers']=='CD PROJEKT RED'])
        st.write("**CD PROJEKT RED** have total gross profit around 60 million dollars")
        st.write("Here is the Top Developers by their Profit!")
        st.altair_chart(alt.Chart(c)
            .mark_bar(orient='horizontal')
            .encode(
                x='profit',
                y=alt.Y('Developers').sort('-x'),
            ),
            use_container_width=True)



    st.write("let's have another quiz! this time for the Publishers!")
    st.text("Who is the Publisher with the highest profit?")
    answer_A_ = st.button("A. Activision")
    answer_B_ = st.button("B. Ubisoft")
    answer_C_ = st.button("C. Electronic Arts")
    answer_D_ = st.button("D. Bethesda Softworks")
    answer_skip = st.button("Skip")

    if answer_A_:
        st.subheader("Sorry, Wrong Answer :slightly_frowning_face:")
        st.image("Activision-logo.png",width= 500)
        st.write(d[d['Publishers']=='Activision'])
        st.write("**Activision** has total gross profit around 68 Million Dollars")
        st.write("Here is the Top Publishers by their Profit")
        st.altair_chart(alt.Chart(d)
        .mark_bar(orient='horizontal')
        .encode(
            x='profit',
            y=alt.Y('Publishers').sort('-x'),
        ),
        use_container_width=True)

    elif answer_B_:
        st.subheader("That's Correct! :smile:")
        st.image("Ubisoft-Logo.wine.png",width= 500)
        st.write(d[d['Publishers']=='Ubisoft'])
        st.write("**Ubisoft** has total gross profit around 105 Million Dollars")
        st.write("Here is the Top Publishers by their Profit")
        st.altair_chart(alt.Chart(d)
        .mark_bar(orient='horizontal')
        .encode(
            x='profit',
            y=alt.Y('Publishers').sort('-x'),
        ),
        use_container_width=True)
        
    elif answer_C_:
        st.subheader("Sorry, Wrong Answer :slightly_frowning_face:")
        st.image("electronic-arts-logo.png",width= 500)
        st.write(d[d['Publishers']=='Electronic Arts'])
        st.write("**Electronic Arts** has total gross profit around 62 Million Dollars")
        st.write("Here is the Top Publishers by their Profit")
        st.altair_chart(alt.Chart(d)
        .mark_bar(orient='horizontal')
        .encode(
            x='profit',
            y=alt.Y('Publishers').sort('-x'),
        ),
        use_container_width=True)
        
    elif answer_D_:
        st.subheader("Sorry, Wrong Answer :slightly_frowning_face:")
        st.image("Bethesda_Softworks-Logo.wine.png",width= 500)
        st.write(d[d['Publishers']=='Bethesda Softworks'])
        st.write("**Bethesda Softworks** have total gross profit around 54 million dollars")
        st.write("Here is the Top Publishers by their Profit")
        st.altair_chart(alt.Chart(d)
        .mark_bar(orient='horizontal')
        .encode(
            x='profit',
            y=alt.Y('Publishers').sort('-x'),
        ),
        use_container_width=True)
    
    elif answer_skip:
        st.subheader("Okk.. your in a hurry :flushed:")
        st.write("Here is the Top Publishers by their Profit")
        st.altair_chart(alt.Chart(d)
        .mark_bar(orient='horizontal')
        .encode(
            x='profit',
            y=alt.Y('Publishers').sort('-x'),
        ),
        use_container_width=True)
# 
# 
# 
    st.write("")
    st.text("Is there any Developers or Publishers you know? "
             "If you do, you should be proud!")
    st.text("because of you, they made it to top 10 :)")
    st.write("")
# 
# 
# 
    st.subheader("Now This is the game that made by our Developers with high users", divider='blue')
    f = dev_data[dev_data['Developers'].isin(a['Developers'].values)]
    g = f[['Developers','Name','Price','Estimate_users','Estimate_profit','Recommendations','Review_score','Genres']]
    unique_value_dev = g['Developers'].unique()
    selected_dev = st.selectbox('Search Developer',list(unique_value_dev), index=None,placeholder= "Find Developer")
    price_dev = st.radio("Filter Price Developers",["All", "Paid", "Free"],captions = ["All Price", "Paid Games", "Free to Play"])
    if  selected_dev:
        filter_result = g[g['Developers']==selected_dev]
        if price_dev == "All":
            st.write(filter_result)
            st.scatter_chart(filter_result, x='Recommendations', y='Review_score', color='Developers')
        elif price_dev == "Paid":
            filter_result = filter_result[filter_result['Price']!=0]
            st.write(filter_result)
            st.scatter_chart(filter_result, x='Recommendations', y='Review_score', color='Developers')
        elif price_dev == "Free":
            filter_result = filter_result[filter_result['Price']==0]
            st.write(filter_result)
            st.scatter_chart(filter_result, x='Recommendations', y='Review_score', color='Developers')
    else :
        filter_result = g
        if price_dev == "All":
            st.write(filter_result)
            st.scatter_chart(filter_result, x='Recommendations', y='Review_score', color='Developers')
        elif price_dev == "Paid":
            filter_result = filter_result[filter_result['Price']!=0]
            st.write(filter_result)
            st.scatter_chart(filter_result, x='Recommendations', y='Review_score', color='Developers')
        elif price_dev == "Free":
            filter_result = filter_result[filter_result['Price']==0]
            st.write(filter_result)
            st.scatter_chart(filter_result, x='Recommendations', y='Review_score', color='Developers')

    st.subheader("This the games that are published by our Publishers with high users", divider='blue')
    h = pub_data[pub_data['Publishers'].isin(b['Publishers'].values)]
    i = h[['Publishers','Name','Price','Estimate_users','Estimate_profit','Recommendations','Review_score','Genres']]
    unique_value_pub = i['Publishers'].unique()
    selected_pub = st.selectbox('Search Publishers',list(unique_value_pub), index=None,placeholder= "Find Publishers")
    price_pub = st.radio("Filter Price Publishers",["All", "Paid", "Free"],captions = ["All Price", "Paid Games", "Free to Play"])
    if  selected_pub:
        filter_result = i[i['Publishers']==selected_pub]
        if price_pub == "All":
            st.write(filter_result)
            st.scatter_chart(filter_result, x='Recommendations', y='Review_score', color='Publishers')
        elif price_pub == "Paid":
            filter_result = filter_result[filter_result['Price']!=0]
            st.write(filter_result)
            st.scatter_chart(filter_result, x='Recommendations', y='Review_score', color='Publishers')
        elif price_pub == "Free":
            filter_result = filter_result[filter_result['Price']==0]
            st.write(filter_result)
            st.scatter_chart(filter_result, x='Recommendations', y='Review_score', color='Publishers')
    else :
        filter_result = i
        if price_pub == "All":
            st.write(filter_result)
            st.scatter_chart(filter_result, x='Recommendations', y='Review_score', color='Publishers')
        elif price_pub == "Paid":
            filter_result = filter_result[filter_result['Price']!=0]
            st.write(filter_result)
            st.scatter_chart(filter_result, x='Recommendations', y='Review_score', color='Publishers')
        elif price_pub == "Free":
            filter_result = filter_result[filter_result['Price']==0]
            st.write(filter_result)
            st.scatter_chart(filter_result, x='Recommendations', y='Review_score', color='Publishers')
# 
# 
# 
# 
    st.subheader("Full distribution of all games",divider='blue')
    st.write("This distribution is based on customer review and their activity to recommend the game")
    distri_game = data[['Name','Price','Positive','Negative']]
    distri_game['Recommendations'] = data1['Recommendations']
    distri_game['Review_score'] = data['Positive']-data['Negative']

    filter_distri = st.radio("Filter price",["All", "Paid", "Free"],captions = ["All Price", "Paid Games", "Free to Play"])
    mode = st.checkbox("Comparison Mode?")
    st.write("Games Distribution Base on Their Price tag")
    if filter_distri == 'All':
        if mode:
            output = distri_game
            output = distri_game[distri_game['Price']!=0]
            plot1 = alt.Chart(output).mark_circle(size=60).encode(
                x=alt.X('Recommendations'),
                y=alt.Y('Review_score'),
                tooltip=['Recommendations',"Review_score",'Name']
            ).properties(
                title="Scatter Plot Free to Play"
            )
            st.altair_chart(plot1, use_container_width=True)
        else:
            output = distri_game[distri_game['Price']!=0]
            plot1 = alt.Chart(output).mark_circle(size=60).encode(
                x=alt.X('Recommendations'),
                y=alt.Y('Review_score'),
                tooltip=['Recommendations',"Review_score",'Name']
            ).properties(
                title="Scatter Plot Free to Play"
            )
            st.altair_chart(plot1, use_container_width=True)
    elif filter_distri == 'Paid':
        if mode:
            output_1 = distri_game[distri_game['Price']!=0]
            output_2 = distri_game[distri_game['Price']==0]
            plot1 = alt.Chart(output_1).mark_circle(size=60).encode(
                x=alt.X('Recommendations'),
                y=alt.Y('Review_score'),
                tooltip=['Recommendations',"Review_score",'Name']
            ).properties(
                title="Scatter Plot Paid to Play"
            )
            plot2 = alt.Chart(output_2).mark_circle(size=60).encode(
                x=alt.X('Recommendations'),
                y=alt.Y('Review_score'),
                tooltip=['Recommendations',"Review_score",'Name']
            ).properties(
                title="Scatter Plot Free to Play"
            )
            col1, col2 = st.columns(2)
            with col1:
                st.altair_chart(plot1, use_container_width=True)
            with col2:
                st.altair_chart(plot2, use_container_width=True)
        else:   
            output = distri_game[distri_game['Price']!=0]
            plot1 = alt.Chart(output).mark_circle(size=60).encode(
                x=alt.X('Recommendations'),
                y=alt.Y('Review_score'),
                tooltip=['Recommendations',"Review_score",'Name']
            ).properties(
                title="Scatter Plot Free to Play"
            )
            st.altair_chart(plot1, use_container_width=True)
    elif filter_distri == 'Free':
        if mode:
            output_1 = distri_game[distri_game['Price']==0]
            output_2 = distri_game[distri_game['Price']!=0]
            plot1 = alt.Chart(output_1).mark_circle(size=60).encode(
                x=alt.X('Recommendations'),
                y=alt.Y('Review_score'),
                tooltip=['Recommendations',"Review_score",'Name']
            ).properties(
                title="Scatter Plot Free to Play"
            )
            plot2 = alt.Chart(output_2).mark_circle(size=60).encode(
                x=alt.X('Recommendations'),
                y=alt.Y('Review_score'),
                tooltip=['Recommendations',"Review_score",'Name']
            ).properties(
                title="Scatter Plot Paid to Play"
            )
            col1, col2 = st.columns(2)
            with col1:
                st.altair_chart(plot1, use_container_width=True)
            with col2:
                st.altair_chart(plot2, use_container_width=True)
        else:   
            output = distri_game[distri_game['Price']!=0]
            plot1 = alt.Chart(output).mark_circle(size=60).encode(
                x=alt.X('Recommendations'),
                y=alt.Y('Review_score'),
                tooltip=['Recommendations',"Review_score",'Name']
            ).properties(
                title="Scatter Plot Free to Play"
            )
            st.altair_chart(plot1, use_container_width=True)









#FIND FILTER THE DATA
elif selected == "Find":
    customer_type = st.radio("Which one is suite you? ",
                             ["Newcomers", "Explorer", "Gamers","Recommended"],
                             captions = ["Search By Genres", 
                                         "Finding Best Game by content", 
                                         "Finding Similar Games",
                                         "Let us help you"],horizontal=True)
    if customer_type == "Newcomers":
        st.header("Hello Newcomers!", divider='blue')
        data_genres = pd.read_csv("genres.csv")
        data = pd.read_csv("new_games_full.csv")
        data1 = pd.read_csv("games_recommend_image_movies_website.csv")

        #feature engineering
        data_modif = data[['Name','Release date','Required age','Price','Developers','Publishers','Genres']]
        data_modif['Estimate Users'] = data["Peak CCU"]+data["Positive"]+data["Negative"]+data1['Recommendations']
        data_modif['Estimate Profit'] = data["Price"]*data_modif["Estimate Users"]
        data_modif['Recommendation'] = data1["Recommendations"]
        data_modif['Review Score'] = data["Positive"]-data["Negative"]

        selected_genres = st.selectbox('Search Genres',data_genres, index=None,placeholder= "Find Genres")
        slide_price = st.slider("How much is your budget?", min_value=0,max_value=199)
        if selected_genres:
            show_genres = data_modif[data_modif['Genres'].str.contains(selected_genres)]
            price_data = show_genres[show_genres['Price']>=slide_price]
            st.write(price_data)
        else:
            price_data = data_modif[data_modif['Price']>=slide_price]
            show_data = price_data
            st.write(show_data)

    


    elif customer_type == "Explorer":
        data_genres = pd.read_csv("genres.csv")
        data = pd.read_csv("new_games_full.csv")
        data1 = pd.read_csv("games_recommend_image_movies_website.csv")

        #feature engineering
        data_modif = data[['Name',
                           'Release date',
                           'Required age',
                           'Price',
                           'Developers',
                           'Publishers',
                           'Genres']]
        data_modif['Estimate Users'] = data["Peak CCU"]+data["Positive"]+data["Negative"]+data1['Recommendations']
        data_modif['Estimate Profit'] = data["Price"]*data_modif["Estimate Users"]
        data_modif['Recommendation'] = data1["Recommendations"]
        data_modif['Review Score'] = data["Positive"]-data["Negative"]

        st.header("Greetings Explorer!", divider='blue')
        dev_list = data_modif["Developers"].unique()
        pub_list = data_modif["Publishers"].unique()
        col1, col2, col3 = st.columns(3)
        with col1:
            selected_genres = st.selectbox('Search Genres',data_genres, index=None,placeholder= "Find Genres")
        with col2:
            selected_Developers = st.selectbox('Search Developers',dev_list, index=None,placeholder= "Find Genres")
        with col3:
            selected_Publishers = st.selectbox('Search Publishers',pub_list, index=None,placeholder= "Find Genres")
        slide_price = st.slider("How much is your budget?", min_value=0,max_value=200)
        sort = ["Estimate Users","Estimate Profit","Recommendation","Review Score","Price"]
        ages = data_modif['Required age'].unique()
        ages = sorted(ages, reverse=False)
        col4, col5 = st.columns(2)
        with col4:
            selected_sort = st.selectbox('Sort by...',sort, index=None,placeholder= "Users")
        with col5:
            selected_age = st.multiselect('Age',ages,placeholder= "All Age")
        if selected_genres:
            show_genres = data_modif[data_modif['Genres'].str.contains(selected_genres)]
            if selected_Developers:
                show_dev = show_genres[show_genres['Developers'].str.contains(selected_Developers)]
            else:
                show_dev = show_genres
            if selected_Publishers:
                show_pub = show_dev[show_dev['Publishers'].str.contains(selected_Publishers)]
            else:
                show_pub = show_dev
            
            price_data = show_pub[show_pub['Price']>=slide_price]
            if selected_age:
                age_data = price_data[price_data["Required age"].isin(selected_age)]
            else:
                age_data = price_data
            if selected_sort:
                sorted_data = age_data.sort_values(selected_sort,ascending=False).head(10)
                st.write(sorted_data)
            else:
                sorted_data = age_data.sort_values("Estimate Users",ascending=False).head(10)
                st.write(sorted_data)
        else:
            if selected_Developers:
                show_dev = data_modif[data_modif['Developers'].str.contains(selected_Developers)]
            else:
                show_dev = data_modif
            if selected_Publishers:
                show_pub = show_dev[show_dev['Publishers'].str.contains(selected_Publishers)]
            else:
                show_pub = show_dev
            price_data = show_pub[show_pub['Price']>=slide_price]
            if selected_age:
                age_data = price_data[price_data["Required age"].isin(selected_age)]
            else:
                age_data = price_data
            if selected_sort:
                show_data = age_data.sort_values(selected_sort,ascending=False).head(10).reset_index()
                st.write(show_data)
            else:
                show_data = age_data.sort_values("Estimate Users",ascending=False).reset_index()
                st.write(show_data)


    
    elif customer_type == "Gamers":
        data = pd.read_csv("games_.csv")
        data1 = pd.read_csv("new_games_full.csv")
        data2 = pd.read_csv("games_recommend_image_movies_website.csv")
        data['Genres'] = data1['Genres']
        data_modif = data1[['Name',
                           'Release date',
                           'Required age',
                           'Price',
                           'Developers',
                           'Publishers',
                           'Genres']]
        data_modif['Estimate Users'] = data1["Peak CCU"]+data1["Positive"]+data1["Negative"]+data2['Recommendations']
        data_modif['Estimate Profit'] = data1["Price"]*data_modif["Estimate Users"]
        data_modif['Recommendation'] = data2["Recommendations"]
        data_modif['Review Score'] = data1["Positive"]-data1["Negative"]
        

        
        data['Genres'] = data1['Genres']
        st.header("Welcome Players!", divider='blue')
        name_value = data['Name'].unique()
        select_game = st.selectbox("You can select your games here and we will find the games that are similar to your game",
                                   name_value,index=None,placeholder= "Select your game here...")
        if select_game:
            filter_table = data[data['Name'].str.contains(select_game)]
            grab_cluster = filter_table['clusters'].unique()
            grab_genre = filter_table['Genres'].unique()
            cluster_game = data[data["clusters"].isin(grab_cluster)]
            similar_game = cluster_game[cluster_game['Genres'].isin(grab_genre)]
            grab_games = similar_game['Name'].unique()
            show_filter = data_modif[data_modif['Name'].isin(grab_games)].sort_values('Review Score',ascending=False).head(10).reset_index()
            st.write("This could be your next adventure!")
            st.write(show_filter)
        else:
            filter_table = data
            st.write("What is on your mind? ")
            st.write(filter_table)

        # st.scatter_chart(filter_table, x='Positive_Negative_dif', y='Peak CCU', color='Name',size='days_since_release')
    
    elif customer_type == "Recommended":
        data = pd.read_csv("genres.csv")
        data1 = pd.read_csv("games_.csv")
        data1['Genres'] = data['Genres']
        # data1['About the game'] = data['About the game']
        # data1 = data1[data1["Estimate users"]>=5000].reset_index()

        st.header("Let the Machine Decide!", divider='blue')
        data_game = data1.Name.unique()
        select_game = st.selectbox("Input Game Name",data_game)
        if select_game:
            filter = data1[data1['Name'].str.contains(select_game)]
            grab_cluster = filter["clusters"].unique()
            similar_game = data1[data1['clusters'].isin(grab_cluster)].reset_index()
    
            ### Reco system
            similar_game["Content"] = similar_game['Genres']+" "+similar_game['About the game']
            tfidf = TfidfVectorizer(min_df = 3,
                            stop_words='english',
                            max_features=None,
                            strip_accents='unicode',
                            analyzer='word',
                            token_pattern=r'\w{1,}',
                            ngram_range=(1,3))
            similar_game["Content"] = similar_game["Content"].fillna(" ")

            tfidf_matrix = tfidf.fit_transform(similar_game['Content'])

            sig = sigmoid_kernel(tfidf_matrix, tfidf_matrix)
            indices = pd.Series(similar_game.index, index=similar_game["Name"])

            idx = indices[select_game]
            sig_score=list(enumerate(sig[idx]))
            sig_score=sorted(sig_score, key=lambda x: x[1], reverse=True)
            sig_score=sig_score[1:11]
            games_indices = [i[0] for i in sig_score]
            st.write("This Could be your potential games!")
            st.write(similar_game['Name'].iloc[games_indices])
            ###
        else:
            st.write("Please Select Game")


elif selected == 'Summary':
    st.header("Summary Page",divider='blue')
    st.subheader("Explore Page summary")
    st.write("1. Some Developers are in Publishers," 
             "this could mean developers and publishers are in the same Company.")
    st.write("2. High users does not mean high profit! " 
             "This could mean some developers and publishers with high users, "
             "can have small profit")
    st.write("The profit is only gross profit")
    st.write("")
    st.write("Recommendation does not effect the review score, "
             "This could possibly means that some users who recommend the game but forgot to review it")
    st.write("")
    st.subheader("Explore Page summary")
    st.write("Different type different treatment but you can try all of it. "
             "Newcomers are for new in gaming world an looking for something that suite their genres. "
             "Explorer are for they who want to see more games by filter that they control." 
             "Gamers is the one who knows about game and likely to find more games that are "
             "similar to their games.")
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
