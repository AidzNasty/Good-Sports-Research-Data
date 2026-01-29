import streamlit as st
import pandas as pd
import os

# Page config
st.set_page_config(page_title="Good Sports Research Statistics", layout="wide")

# File path
EXCEL_FILE = '2025 Good Sports Research Project_Aidan Conte.xlsx'

# Load data
@st.cache_data
def load_data():
    try:
        # Use engine='openpyxl' but pandas will handle it internally
        df = pd.read_excel(EXCEL_FILE, sheet_name='Research', engine='openpyxl')
        return df, None
    except ImportError:
        # If openpyxl not available, try without specifying engine
        try:
            df = pd.read_excel(EXCEL_FILE, sheet_name='Research')
            return df, None
        except Exception as e:
            return None, f"❌ Error: Install openpyxl with: pip install openpyxl\n\nDetails: {str(e)}"
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
    st.info("**Make sure:**")
    st.markdown("1. Your Excel file is in the same folder as this script")
    st.markdown("2. openpyxl is installed: `pip install openpyxl`")
    st.markdown("3. Restart Streamlit completely (Ctrl+C then rerun)")
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
        # Count stats
        st.caption(f"Found {len(filtered_df)} statistic(s)")
        st.markdown("---")
        
        # Display each stat
        for idx, (orig_idx, row) in enumerate(filtered_df.iterrows(), 1):
            with st.container():
                # Year in a colored box
                year = row['Year'] if pd.notna(row['Year']) else "N/A"
                col1, col2 = st.columns([1, 9])
                
                with col1:
                    st.markdown(f"### {year}")
                
                with col2:
                    # Display stat
                    stat_text = row['Stat'] if pd.notna(row['Stat']) else "No description available"
                    st.write(stat_text)
                    
                    # Display source
                    source = row['Source'] if pd.notna(row['Source']) else None
                    if source:
                        st.caption(f"📄 **Source:** {source}")
                
                st.markdown("---")
else:
    st.info("👆 Please select a category from the dropdown above to view statistics.")
    
    # Show available categories
    with st.expander("📋 Available Categories"):
        for cat in categories:
            st.write(f"• {cat}")

# Footer
st.markdown("---")
st.caption("Good Sports Research Project | 2025")
