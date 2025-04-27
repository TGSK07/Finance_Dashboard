import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os

st.set_page_config(page_title="Personal Finance Dashbaord",page_icon="assests/icon.png",layout="wide")

cat_file = "categories.json"

if 'categories' not in st.session_state:
    st.session_state.categories = {
        'Uncategorized':[],
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
            details = row['Details'].lower().strip()
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
        st.error(f"An Error occurs during processing a file {str(e)}")
        return None


def main():
    st.title("Personal Finance Dashbaord")
    
    uploaded_file = st.file_uploader("Upload your finance transaction here...(as csv file)",type=["csv"])
    if uploaded_file is not None:
        df = load_transactions(uploaded_file)
        if df is not None:
            debits_data = df[df['Debit/Credit']=='Debit'].copy() 
            credits_data = df[df['Debit/Credit']=='Credit'].copy()

            st.session_state.debits_data = debits_data.copy()

            tab1, tab2 = st.tabs(['Expenses (Debits)',"Payments (Credits)"])

            with tab1:
                new_cat = st.text_input("New Category Name")
                add_button = st.button("Add Category")
                
                if add_button and new_cat:
                    if new_cat not in st.session_state.categories:
                        st.session_state.categories[new_cat] = []
                        save_cat()
                        st.success(f"{new_cat} category added successfully.")
                        time.sleep(1)
                        st.rerun()

                st.subheader("Your Expenses")
                total_payments = debits_data['Amount'].sum()
                st.metric('Total Expenses',f"{total_payments:.2f}")
                edit_df = st.data_editor(
                    st.session_state.debits_data[['Date','Details','Amount','Category']],
                    column_config = {
                        'Date': st.column_config.DateColumn('Date',format='DD/MM/YYYY'),
                        'Amount':st.column_config.NumberColumn('Amount',format="%.2f"),
                        "Category":st.column_config.SelectboxColumn(
                            'Category',options=list(st.session_state.categories.keys())
                        )
                    },
                    hide_index = True, use_container_width=True, key='category_editor'
                )
                save_button = st.button('Apply Changes',type='primary')
                if save_button:
                    for idx,row in edit_df.iterrows():
                        new_cat = row['Category']
                        
                        if new_cat == st.session_state.debits_data.at[idx,'Category']:
                            continue

                        details = row['Details']
                        st.session_state.debits_data.at[idx,'Category'] = new_cat

                        add_keyword_to_cat(new_cat, details)

                st.subheader('Expense Summary')
                cat_totals = st.session_state.debits_data.groupby('Category')['Amount'].sum().reset_index()
                cat_totals = cat_totals.sort_values('Amount',ascending=False)

                st.dataframe(
                    cat_totals, 
                    column_config={'Amount':st.column_config.NumberColumn("Amount",format="%.2f")},
                    use_container_width=True,
                    hide_index=True
                )
                fig = px.pie(
                    cat_totals,
                    values='Amount',
                    names='Category',
                    title='Expenses by Category'
                )
                st.plotly_chart(fig, use_container_width=True)
                
            with tab2:
                st.subheader("Payments Summary")
                total_payments = credits_data['Amount'].sum()
                st.metric('Total Payments',f"{total_payments:.2f}")
                st.write(credits_data)

    
if __name__=="__main__":
    main()
