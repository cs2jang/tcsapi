import pickle
from pathlib import Path

import streamlit_authenticator as stauth
import streamlit as st


st.set_page_config(page_title="Analysis Traffic", page_icon=":signal_strength:", layout="wide")
name_list = ['관리자', '사용자']
username_list = ['admin', 'stcuser']

file_path = Path(__file__).parent / "hash_pw.pkl"
with file_path.open('rb') as file:
    hash_passwords = pickle.load(file)

authenticator = stauth.Authenticate(
    name_list, username_list, hash_passwords, 'analysis traffic', 'abcd', 30
    )

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
elif authentication_status:

    authenticator.logout("Logout", "sidebar")
    st.sidebar.title(f"Welcome {name}")
    st.sidebar.header("Please Filter Here:")

    with st.container():
        st.subheader("Hi, I am Sven :wave:")
        st.title("A Data Analyst From Germany")
        st.write(
            "I am passionate about finding ways to use Python and VBA to be more efficient and effective in business settings."
        )
        st.write("[Learn More >](https://pythonandvba.com)")


    with st.container():
        st.write("---")
        left_column, right_column = st.columns(2)
        with left_column:
            st.header("What I do")
            st.write("##")
            st.write(
                """
                On my YouTube channel I am creating tutorials for people who:
                - are looking for a way to leverage the power of Python in their day-to-day work.
                - are struggling with repetitive tasks in Excel and are looking for a way to use Python and VBA.
                - want to learn Data Analysis & Data Science to perform meaningful and impactful analyses.
                - are working with Excel and found themselves thinking - "there has to be a better way."
                If this sounds interesting to you, consider subscribing and turning on the notifications, so you don’t miss any content.
                """
            )
        with right_column:
            st.write("[YouTube Channel >](https://youtube.com/c/CodingIsFun)")
            
        hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
        st.markdown(hide_st_style, unsafe_allow_html=True)
