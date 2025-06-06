import streamlit as st

def app1():
    st.title("App 1")
    st.write("This is the first app")

def app2():
    st.title("App 2")
    st.write("This is the second app")

app_mode = st.sidebar.selectbox("Choose App", ["App 1", "App 2"])

if app_mode == "App 1":
    app1()
else:
    app2()
