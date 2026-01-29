import streamlit as st
import pandas as pd
import openpyxl
import os
import base64

# Page config
st.set_page_config(
    page_title="Good Sports Research Statistics",
    page_icon="📊",
    layout="wide"
)

# Function to convert image to base64
def get_base64_image(image_path):
    """Convert image to base64 for embedding in HTML"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None

# Try to load logo (place logo file in same directory as script)
logo_base64 = get_base64_image("good_sports_logo.png")

# Custom CSS with Good Sports actual colors
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');
    
    /* Main app styling */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%);
    }
    
    /* Custom header with logo */
    .custom-header {
        background: linear-gradient(135deg, #8B9F3E 0%, #A8B968 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(139, 159, 62, 0.3);
        display: flex;
        align-items: center;
        gap: 2rem;
    }
    
    .logo-container {
        flex-shrink: 0;
    }
    
    .logo-container img {
        height: 80px;
        background: white;
        padding: 10px 20px;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .header-text {
        flex-grow: 1;
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
    
    /* Dropdown styling with Good Sports green */
    .stSelectbox > div > div {
        background-color: white;
        border: 2px solid #8B9F3E;
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
        border-left: 5px solid #8B9F3E;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    
    .stat-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 15px rgba(139, 159, 62, 0.2);
    }
    
    .year-badge {
        background: linear-gradient(135deg, #0066A1 0%, #0082CC 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 700;
        font-size: 1.1rem;
        display: inline-block;
        margin-bottom: 1rem;
        font-family: 'Montserrat', sans-serif;
        box-shadow: 0 2px 5px rgba(0, 102, 161, 0.3);
    }
    
    .stat-text {
        color: #2C3E50;
        font-size: 1.05rem;
        line-height: 1.6;
        font-family: 'Montserrat', sans-serif;
        margin: 1rem 0;
    }
    
    .read-more-btn {
        background: linear-gradient(135deg, #8B9F3E 0%, #A8B968 100%);
        color: white;
        padding: 0.6rem 1.5rem;
        border-radius: 25px;
        text-decoration: none;
        font-weight: 600;
        display: inline-block;
        font-family: 'Montserrat', sans-serif;
        transition: transform 0.2s, box-shadow 0.2s;
        box-shadow: 0 2px 8px rgba(139, 159, 62, 0.3);
    }
    
    .read-more-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(139, 159, 62, 0.4);
        text-decoration: none;
        color: white;
        background: linear-gradient(135deg, #9BB04A 0%, #B8C777 100%);
    }
    
    .source-text {
        color: #7F8C8D;
        font-size: 0.9rem;
        font-family: 'Montserrat', sans-serif;
        margin-top: 0.5rem;
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
        border-left: 5px solid #0066A1;
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
        background: linear-gradient(135deg, #0066A1 0%, #0082CC 100%);
        color: white;
        padding: 0.75rem 1.5rem;
        border-radius: 25px;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 1.5rem;
        font-family: 'Montserrat', sans-serif;
        box-shadow: 0 3px 10px rgba(0, 102, 161, 0.3);
    }
    
    /* Category title with accent */
    .category-title {
        color: #8B9F3E;
        font-family: 'Montserrat', sans-serif;
        font-weight: 700;
        border-bottom: 3px solid #8B9F3E;
        padding-bottom: 0.5rem;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# File path
EXCEL_FILE = '2025 Good Sports Research Project_Aidan Conte.xlsx'

# Load data and hyperlinks
@st.cache_data
def load_data():
    try:
        df = pd.read_excel(EXCEL_FILE, sheet_name='Research', engine='openpyxl')
        return df, None
    except Exception as e:
        return None, f"❌ Error loading file: {str(e)}"

@st.cache_resource
def load_workbook():
    """Load workbook to extract hyperlinks"""
    try:
        return openpyxl.load_workbook(EXCEL_FILE)
    except Exception as e:
        st.warning(f"Could not load hyperlinks: {e}")
        return None

def get_hyperlink(workbook, row_index):
    """Extract hyperlink from Excel cell in the Source column (column B)"""
    if workbook is None:
        return None
    try:
        sheet = workbook['Research']
        # row_index is from pandas (0-indexed), Excel is 1-indexed + 1 for header
        excel_row = row_index + 2
        cell = sheet.cell(row=excel_row, column=2)  # Column B = Source column
        if cell.hyperlink:
            return cell.hyperlink.target
    except Exception as e:
        pass
    return None

# Custom header with logo
if logo_base64:
    header_html = f"""
    <div class="custom-header">
        <div class="logo-container">
            <img src="data:image/png;base64,{logo_base64}" alt="Good Sports Logo">
        </div>
        <div class="header-text">
            <h1>Research Statistics Database</h1>
            <p>Comprehensive data supporting youth sports and physical activity initiatives</p>
        </div>
    </div>
    """
else:
    # Fallback without logo
    header_html = """
    <div class="custom-header">
        <div class="header-text">
            <h1>📊 Good Sports Research Statistics</h1>
            <p>Comprehensive data supporting youth sports and physical activity initiatives</p>
        </div>
    </div>
    """

st.markdown(header_html, unsafe_allow_html=True)

# Load data
df, error = load_data()

if error:
    st.error(error)
    st.info(f"**Current working directory:** `{os.getcwd()}`")
    st.info("**Make sure:**")
    st.markdown("1. Your Excel file is in the same folder as this script")
    st.markdown("2. openpyxl is installed: `pip install openpyxl`")
    st.markdown("3. The Good Sports logo (good_sports_logo.png) is in the same folder")
    st.stop()

# Load workbook for hyperlinks
workbook = load_workbook()

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
    st.markdown(f'<h2 class="category-title">{selected_category}</h2>', unsafe_allow_html=True)
    
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
            
            # Get hyperlink from Excel
            hyperlink = get_hyperlink(workbook, orig_idx)
            
            # Build HTML for stat card
            card_html = f'''
            <div class="stat-card">
                <div class="year-badge">📅 {year}</div>
                <div class="stat-text">{stat_text}</div>
            '''
            
            if source:
                card_html += f'<div class="source-text">📄 <strong>Source:</strong> {source}</div>'
            
            if hyperlink:
                card_html += f'<br><a href="{hyperlink}" target="_blank" class="read-more-btn">🔗 Read Full Article</a>'
            
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

# Footer with Good Sports branding
st.markdown("""
<div class="footer">
    <strong style="color: #8B9F3E;">Good Sports Research Project</strong> | 2025<br>
    <em>Empowering youth through sports and physical activity</em>
</div>
""", unsafe_allow_html=True)
