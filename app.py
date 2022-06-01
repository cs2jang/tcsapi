import pickle
from pathlib import Path
from datetime import datetime, date, timedelta
import plotly.express as px
import streamlit as st
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu
from tcsapi import tcsapi

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
    with st.container():
        selected = option_menu (
            menu_title = None, 
            options=["TCS Data Home", "Machine Learning Projects", "Contact"],
            default_index=0, 
            orientation="horizontal"
        )
        
    with st.container():
        st.title(f"Welcome {name}")
        authenticator.logout("Logout", "main")
        tcs = tcsapi()
        st.subheader(f"Hi, {name} :wave:")
        st.title("TCS Data")
        max_value = datetime.now() + timedelta(days=-3)
        min_value = date(2003, 1, 1)
        dates = st.date_input("Select Dates", value=(), min_value=min_value, max_value=max_value)
        if st.button('Get Data') and len(dates) == 2:
            d_start = dates[0].strftime("%Y%m%d")
            d_end = dates[1].strftime("%Y%m%d")
            print(d_start, d_end)
            df_tcs = tcs.getDataFrame(d_start, d_end)
            st.dataframe(df_tcs)
            fig = px.scatter(df_tcs, x="req_date", y="sum", color='sum')
            st.plotly_chart(fig, use_container_width=True)


    with st.container():
        st.write("---")
        left_column, right_column = st.columns(2)
        with left_column:
            st.header("What I do")
            st.write("##")
            st.write(
                """
                left column space.
                """
            )
        with right_column:
            st.write("right column space")
            
        hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
        st.markdown(hide_st_style, unsafe_allow_html=True)
