import streamlit as st

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