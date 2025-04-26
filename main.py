import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os

st.set_page_config(page_title="Personal Finance Dashbaord",page_icon="assests/icon.png",layout="wide")

cat_file = "categories.json"

if 'categories' not in st.session_state:
    st.session_state.categories = {
        'Uncategorized':[]
    }
     
if os.path.exists(cat_file):
    with open(cat_file,"r") as f:
        st.session_state.categories = json.load(f)

def save_cat():
    with open(cat_file,"w") as f:
        json.dump(st.session_state.categories,f)



def load_transactions(file):
    try:
        df = pd.read_csv(file)
        df.columns = [col.strip() for col in df.columns if col]
        df["Amount"] = df['Amount'].str.replace(",","").astype(float)
        df["Date"] = pd.to_datetime(df['Date'],format='%d %b %Y')

        return df
    except Exception as e:
        st.error(f"An Error occurs during processing a file {e}")
        return None


def main():
    st.title("Personal Finance Dashbaord")
    
    uploaded_file = st.file_uploader("Upload your finance transaction here...(as csv file)",type=["csv"])
    if uploaded_file is not None:
        df = load_transactions(uploaded_file)
        
        if df is not None:
            debit_data = df[df['Debit/Credit']=='Debit'].copy() 
            credit_data = df[df['Debit/Credit']=='Credit'].copy() 

            tab1, tab2 = st.tabs(['Express (Debits)',"Payments (Credit)"])

            with tab1:
                st.write(debit_data)

            with tab2:
                st.write(credit_data)

    
if __name__=="__main__":
    main()