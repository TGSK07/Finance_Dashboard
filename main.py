import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os

st.set_page_config(page_title="Personal Finance Dashbaord",page_icon="assests/icon.png",layout="wide")


def load_transactions(file):
    try:
        df = pd.read_csv(file)
        df.columns = [col.strip() for col in df.columns if col]
        st.write(df)
    except Exception as e:
        st.error(f"An Error occurs during processing a file {e}")


def main():
    st.title("Personal Finance Dashbaord")
    
    uploaded_file = st.file_uploader("Upload your finance transaction here...(as csv file)",type=["csv"])
    if uploaded_file is not None:
        df = load_transactions(uploaded_file)
    
if __name__=="__main__":
    main()