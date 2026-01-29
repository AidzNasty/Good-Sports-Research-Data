import streamlit as st
import pandas as pd
import os

# Page config
st.set_page_config(
    page_title="Good Sports Research Statistics",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for Good Sports branding
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');
    
    /* Main app styling */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%);
    }
    
    /* Custom header */
    .custom-header {
        background: linear-gradient(135deg, #FF6B35 0%, #FF8C42 100%);
        padding: 2rem 2rem 1.5rem 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(255, 107, 53, 0.2);
    }
    
    .custom-header h1 {
        color: white;
        font-family: 'Montserrat', sans-serif;
        font-weight: 700;
        font-size: 2.5rem;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .custom-header p {
        color: white;
        font-family: 'Montserrat', sans-serif;
        font-size: 1.1rem;
        margin-top: 0.5rem;
        opacity: 0.95;
    }
    
    /* Dropdown styling */
    .stSelectbox > div > div {
        background-color: white;
        border: 2px solid #FF6B35;
        border-radius: 8px;
        font-family: 'Montserrat', sans-serif;
        font-weight: 600;
    }
    
    /* Stat cards */
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        border-left: 5px solid #FF6B35;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .stat-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 15px rgba(255, 107, 53, 0.15);
    }
    
    .year-badge {
        background: linear-gradient(135deg, #4A90E2 0%, #357ABD 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 700;
        font-size: 1.1rem;
        display: inline-block;
        margin-bottom: 1rem;
        font-family: 'Montserrat', sans-serif;
        box-shadow: 0 2px 5px rgba(74, 144, 226, 0.3);
    }
    
    .stat-text {
        color: #2C3E50;
        font-size: 1.05rem;
        line-height: 1.6;
        font-family: 'Montserrat', sans-serif;
        margin: 1rem 0;
    }
    
    .source-link {
        color: #4A90E2;
        font-size: 0.9rem;
        font-weight: 600;
        text-decoration: none;
        font-family: 'Montserrat', sans-serif;
    }
    
    .source-link:hover {
        color: #FF6B35;
        text-decoration: underline;
    }
    
    /* Category selector label */
    label {
        font-family: 'Montserrat', sans-serif;
        font-weight: 600;
        color: #2C3E50;
        font-size: 1.1rem;
    }
    
    /* Info boxes */
    .stInfo {
        background-color: #E8F4F8;
        border-left: 5px solid #4A90E2;
        border-radius: 8px;
        font-family: 'Montserrat', sans-serif;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #7F8C8D;
        font-family: 'Montserrat', sans-serif;
        margin-top: 3rem;
    }
    
    /* Stats counter */
    .stats-counter {
        background: linear-gradient(135deg, #4A90E2 0%, #357ABD 100%);
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 25px;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 1.5rem;
        font-family: 'Montserrat', sans-serif;
        box-shadow: 0 3px 10px rgba(74, 144, 226, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# File path
EXCEL_FILE = '2025 Good Sports Research Project_Aidan Conte.xlsx'

# Load data
@st.cache_data
def load_data():
    try:
        df = pd.read_excel(EXCEL_FILE, sheet_name='Research', engine='openpyxl')
        return df, None
    except ImportError:
        try:
            df = pd.read_excel(EXCEL_FILE, sheet_name='Research')
            return df, None
        except Exception as e:
            return None, f"❌ Error: Install openpyxl with: pip install openpyxl\n\nDetails: {str(e)}"
    except FileNotFoundError:
        return None, f"❌ Error: Could not find '{EXCEL_FILE}' in the current directory."
    except Exception as e:
        return None, f"❌ Error loading file: {str(e)}"

# Custom header
st.markdown("""
<div class="custom-header">
    <h1>📊 Good Sports Research Statistics</h1>
    <p>Comprehensive data supporting youth sports and physical activity initiatives</p>
</div>
""", unsafe_allow_html=True)

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

# Category dropdown with custom styling
st.markdown("### 🔍 Select a Research Category")
selected_category = st.selectbox(
    "Choose a category to view all related statistics:",
    ["-- Select a Category --"] + categories,
    label_visibility="collapsed"
)

# Display stats if category is selected
if selected_category != "-- Select a Category --":
    st.markdown(f"## {selected_category}")
    
    # Filter data
    filtered_df = df[df['Category'] == selected_category].copy()
    
    if len(filtered_df) == 0:
        st.info("No statistics found for this category.")
    else:
        # Count stats
        st.markdown(
            f'<div class="stats-counter">📈 {len(filtered_df)} statistic(s) found</div>',
            unsafe_allow_html=True
        )
        
        # Display each stat
        for idx, (orig_idx, row) in enumerate(filtered_df.iterrows(), 1):
            # Create stat card
            year = row['Year'] if pd.notna(row['Year']) else "N/A"
            stat_text = row['Stat'] if pd.notna(row['Stat']) else "No description available"
            source = row['Source'] if pd.notna(row['Source']) else None
            
            # Build HTML for stat card
            card_html = f'''
            <div class="stat-card">
                <div class="year-badge">📅 {year}</div>
                <div class="stat-text">{stat_text}</div>
            '''
            
            if source:
                card_html += f'<div>📄 <span style="color: #7F8C8D; font-family: Montserrat;">Source:</span> <span class="source-link">{source}</span></div>'
            
            card_html += '</div>'
            
            st.markdown(card_html, unsafe_allow_html=True)
else:
    # Show welcome message with category preview
    st.info("👆 Please select a category from the dropdown above to view statistics.")
    
    # Show available categories in an expander
    with st.expander("📋 View All Available Categories"):
        cols = st.columns(2)
        for i, cat in enumerate(categories):
            with cols[i % 2]:
                st.markdown(f"**•** {cat}")

# Footer
st.markdown("""
<div class="footer">
    <strong>Good Sports Research Project</strong> | 2025<br>
    <em>Empowering youth through sports and physical activity</em>
</div>
""", unsafe_allow_html=True)
