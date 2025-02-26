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


# Title and description
st.title("📀 Datasweeper Sterling Integrator by Komal Khan")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization for Quarter 3!")
# file uploader
# File uploader
uploaded_files = st.file_uploader("Upload your files (CSV/Excel)", type=["csv", "xlsx"], accept_multiple_files=True)

# Initialize lists for storing DataFrames and filenames
dfs = []
file_names = []

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"File type not supported: {file_ext}")
            continue  # Skip unsupported files

        # Store the DataFrame and filename
        dfs.append(df)
        file_names.append(file.name)

    # Combine all uploaded DataFrames into one
    if dfs:
        final_df = pd.concat(dfs, ignore_index=True)
        st.write("📊 Merged Data Preview:")
        st.dataframe(final_df)

        st.write("🔍 Preview the head of the DataFrame")
        st.dataframe(final_df.head())  # Show first few rows
    else:
        st.warning("No valid files uploaded.")

# Data cleaning section
st.subheader("🛠 Data Cleaning Options")

for name, df in zip(file_names, dfs):  # ✅ Corrected unpacking
    if st.checkbox(f"Clean data for {name}"):
        st.write(f"Cleaning data for {name}...")
        st.dataframe(df.head())

        col1, col2 = st.columns(2)

        with col1:
            if st.button(f"Remove Duplicates from {name}"):
                df.drop_duplicates(inplace=True)
                st.write("✅ Duplicates removed!")

        with col2:
            if st.button(f"Fill missing values in {name}"):
                numeric_cols = df.select_dtypes(include=["number"]).columns  # ✅ Fixed typo
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                st.write("✅ Missing values filled!")
        # Column selection
        st.subheader("🎯 Select Columns to Keep")
        selected_columns = st.multiselect(f"Choose columns for {name}", df.columns, default=df.columns)
        df = df[selected_columns]

        # Data visualization
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"Show Visualization for {name}"):
            st.bar_chart(df.select_dtypes(include=["number"]).iloc[:, :2])

        # File conversion
        st.subheader("🔄 Conversion Options")
        conversion_type = st.radio(f"Convert {name} to:", ["CSV", "Excel"], key=name)

        if st.button(f"Convert {name}"):
            buffer = BytesIO()
            file_ext = os.path.splitext(name)[-1].lower()

            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_type == "Excel":
                with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
                    df.to_excel(writer, index=False)
                file_name = name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)

            st.download_button(
                label=f"Download {name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

st.success("🎉 All files processed successfully!")

