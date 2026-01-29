
import streamlit as st
import pandas as pd
import os

# Page config
st.set_page_config(page_title="Good Sports Research Statistics - DEBUG", layout="wide")

st.title("🔍 DEBUG MODE - File Finder")
st.markdown("---")

# Show current directory
st.subheader("Current Working Directory:")
st.code(os.getcwd())

# List ALL files in current directory
st.subheader("Files in Current Directory:")
try:
    files = os.listdir('.')
    if files:
        for file in sorted(files):
            st.write(f"📄 {file}")
    else:
        st.warning("Directory is empty!")
except Exception as e:
    st.error(f"Error listing files: {e}")

st.markdown("---")

# Try to find any .xlsx files
st.subheader("Looking for Excel files (.xlsx):")
xlsx_files = [f for f in os.listdir('.') if f.endswith('.xlsx')]
if xlsx_files:
    st.success(f"Found {len(xlsx_files)} Excel file(s):")
    for file in xlsx_files:
        st.write(f"✅ {file}")
else:
    st.error("No .xlsx files found in current directory!")

st.markdown("---")

# Let user try different filenames
st.subheader("Test File Loading:")
test_filename = st.text_input("Enter exact filename to test:", value="2025 Good Sports Research Project_Aidan Conte.xlsx")

if st.button("Try Loading This File"):
    try:
        df = pd.read_excel(test_filename, sheet_name='Research')
        st.success(f"✅ Successfully loaded '{test_filename}'!")
        st.write(f"Shape: {df.shape}")
        st.write("First few rows:")
        st.dataframe(df.head())
    except FileNotFoundError:
        st.error(f"❌ File '{test_filename}' not found")
    except Exception as e:
        st.error(f"❌ Error: {e}")

st.markdown("---")
st.info("📝 Copy the EXACT filename from the list above and paste it into the test box to verify.")
