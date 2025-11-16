import streamlit as st

st.title("Hello Streamlit!")
st.write("Welcome to your empty Streamlit app running on Python 3.14 with uv.")

# Add some basic examples
st.header("Example Components")
st.button("Click me")
st.text_input("Enter some text")
st.slider("Select a value", 0, 100, 50)
