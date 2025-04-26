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

def cat_transactions(df):
    df["Category"] = "Uncategorized"
    for cat,keywords in st.session_state.categories.items():
        if cat=="Uncategorized" or not keywords:
            continue
        lowered_keywords = [keyword.lower().strip() for keyword in keywords]
        
        for idx, row in df.iterrows():
            details = row['Details'].lower()
            if details in lowered_keywords:
                df.at[idx,"Category"] = cat
    return df

def add_keyword_to_cat(cat,keyword):
    keyword = keyword.strip()
    if keyword and keyword not in st.session_state.categories[cat]:
        st.session_state.categories[cat].append(keyword)
        save_cat()
        return True
    return False


def load_transactions(file):
    try:
        df = pd.read_csv(file)
        df.columns = [col.strip() for col in df.columns if col]
        df["Amount"] = df['Amount'].str.replace(",","").astype(float)
        df["Date"] = pd.to_datetime(df['Date'],format='%d %b %Y')

        return cat_transactions(df)
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

            st.session_state

            tab1, tab2 = st.tabs(['Expenses (Debits)',"Payments (Credits)"])

            with tab1:
                new_cat = st.text_input("New Category Name")
                add_button = st.button("Add Category")
                if add_button and new_cat:
                    if new_cat not in st.session_state.categories:
                        st.session_state.categories[new_cat] = []
                        save_cat()
                        st.success(f"{new_cat} category added successfully.")
                        st.rerun()

                st.subheader("Your Expense")
                edit_df = st.data_editor(
                    st.session_state.debits_df[['Date','Details','Amount','Category']],
                    column_config = {
                        'Date': st.column_config.DateColumn('Date',format='DD/MM/YYYY'),
                        'Amount':st.column_config.NumberColumn('Amount',format="%.2f"),
                        "Category":st.column_config.SelectionColumn(
                            'Category',options=list(st.session_state.categories.keys())
                        )
                    },
                    hide_index = True, use_container_width=True,key='category_editor'
                )
                save_button = st.button('Apply Changes',types='primary')
                if save_button:
                    for idx,row in edit_df.iterrows():
                        if row["Category"] != st.session_state.debits_df.at[idx,'Category']:
                            continue
                        details = row['Details']
                        st.session_state.debits_df.at[idx,'Category'] = new_cat
                        add_keyword_to_cat(new_cat,details)
                
            with tab2:
                st.write(credit_data)

    
if __name__=="__main__":
    main()