import streamlit as st

st.set_page_config(page_title="Test App", page_icon="🚀")

st.title("🚀 Test App - Hello World!")
st.write("If you can see this, Streamlit is working!")

if st.button("Click me!"):
    st.balloons()
    st.success("It works! 🎉")