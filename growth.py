import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="data sweeper", layout="wide")

# custom css
st.markdown(
    """
    <style>
    .stApp{
        background-color: black;
        color:white;
        }
    </style>
        """,
        unsafe_allow_html=True
)

# title and description

st.title("Datasweeper Sterling Integrator by Komal Khan")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization creating the project for quarter 3!")

# file uploader

uploaded_file = st.file_uploader("Upload your files (accepts CSV and Excel)", type=["csv", "xlsx"], accept_multiple_files=True)
if uploaded_file:
    for file in uploaded_file:
        file_ext = os.path.splitext(file.name)[-1].lower()
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"File type not supported: {file_ext}")
        continue

# file details

st.write("preview the head of the DataFrame")
st.dataframe(df.head())

# data cleaning

st.subheader("Data Cleaning Options")
if st.checkbox(f"clean data for {file.name}"):
    col1, col2 = st.columns(2)
    with col1:
        st.button(f"Remove Dublicates from the file {file.name}")
        df.drop_duplicates(inplace=True)
        st.write("Dublicates removed!")
        with col2:
            st.button(f"fill missing values in the file {file.name}")
            numeric_cols = df.slected_dtypes(include=["number"]).columns
            df[numeric_cols]  = df[numeric_cols].fillna(df[numeric_cols].mean())
            st.write("Missing values filled!")

        st.subheader("Select Columns to Keep")
        columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default= df.columns)
        df = df[columns]


        # data visualization
        st.subheader("Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include=["number"]).iloc[:, :2])

        #Converstion Options
        st.subheader("Converstion Options")    
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        if st.button(f"Covert{file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".CSV")
                mime_type = "text/CSV"
                
            elif conversion_type == "Excel":
                df.to.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            st.download_button(f"Click here to download {file_name} as {conversion_type}", data=buffer, file_name=file_name, mime=mime_type
            )

st.success(f"{file.name} successfully converted to {conversion_type}")