

import streamlit as st
import pandas as pd
import os

# Page config
st.set_page_config(page_title="Good Sports Research Statistics", layout="wide")

# File path - UPDATE THIS to match your file location
EXCEL_FILE = '/Users/aidanconte/Library/CloudStorage/OneDrive-SuffolkUniversity/Good Sports Internship/2025 Good Sports Research Project_Aidan Conte.xlsx'

# Load data
@st.cache_data
def load_data():
    try:
        df = pd.read_excel(EXCEL_FILE, sheet_name='Research')
        return df, None
    except FileNotFoundError:
        return None, f"❌ Error: Could not find '{EXCEL_FILE}' in the current directory."
    except Exception as e:
        return None, f"❌ Error loading file: {str(e)}"

# Main app
st.title("📊 Good Sports Research Statistics")
st.markdown("---")

# Load data
df, error = load_data()

if error:
    st.error(error)
    st.info(f"**Current working directory:** `{os.getcwd()}`")
    st.info("**Make sure your Excel file is in the same folder as this script, or update the EXCEL_FILE path at the top of the script.**")
    st.stop()

# Get unique categories
categories = sorted([cat for cat in df['Category'].unique() if pd.notna(cat)])

# Category dropdown
selected_category = st.selectbox("Select a Category:", ["-- Select --"] + categories)

# Display stats if category is selected
if selected_category != "-- Select --":
    st.markdown(f"### {selected_category}")
    
    # Filter data
    filtered_df = df[df['Category'] == selected_category].copy()
    
    if len(filtered_df) == 0:
        st.info("No statistics found for this category.")
    else:
        # Display each stat
        for idx, (orig_idx, row) in enumerate(filtered_df.iterrows()):
            with st.container():
                col1, col2 = st.columns([1, 10])
                
                with col1:
                    year = row['Year'] if pd.notna(row['Year']) else "N/A"
                    st.markdown(f"**{year}**")
                
                with col2:
                    # Display stat
                    stat_text = row['Stat'] if pd.notna(row['Stat']) else "No description available"
                    st.markdown(stat_text)
                    
                    # Display source (text only)
                    source = row['Source'] if pd.notna(row['Source']) else None
                    if source:
                        st.caption(f"📄 Source: {source}")
                
                st.markdown("---")
else:
    st.info("👆 Please select a category from the dropdown above to view statistics.")

# Footer
st.markdown("---")
st.caption("Good Sports Research Project | 2025")
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
