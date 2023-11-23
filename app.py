from streamlit_authenticator import Authenticate
import yaml
from yaml.loader import SafeLoader
from src.main_content import render_main_content

with open("./config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

import streamlit as st


GPT_MODEL = "gpt-3.5-turbo-1106"

authenticator = Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
    config["preauthorized"],
)

st.title("Rose Rocket Assistant 🌹")

name, authentication_status, username = authenticator.login("Login", "main")


if authentication_status:
    render_main_content(authenticator, name)
elif authentication_status is False:
    st.error("Username/password is incorrect")
elif authentication_status is None:
    st.warning("Please enter your username and password")
