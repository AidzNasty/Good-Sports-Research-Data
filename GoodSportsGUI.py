import streamlit as st
import pandas as pd
import openpyxl
import os
import base64
import re

# Page config
st.set_page_config(
    page_title="Good Sports Research Statistics",
    page_icon="📊",
    layout="wide"
)

# Function to convert image to base64
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None

logo_base64 = get_base64_image("good_sports_logo.png")

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');
    .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #ffffff 100%); }
    .custom-header {
        background: linear-gradient(135deg, #8B9F3E 0%, #A8B968 100%);
        padding: 2rem; border-radius: 15px; margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(139, 159, 62, 0.3);
        display: flex; align-items: center; gap: 2rem;
    }
    .logo-container { flex-shrink: 0; }
    .logo-container img { height: 80px; background: white; padding: 10px 20px; border-radius: 10px; }
    .custom-header h1 { color: white; font-family: 'Montserrat', sans-serif; font-weight: 700; font-size: 2.5rem; margin: 0; }
    .custom-header p { color: white; font-family: 'Montserrat', sans-serif; font-size: 1.1rem; opacity: 0.95; }
    .filter-section { background: white; padding: 1.5rem; border-radius: 12px; margin-bottom: 2rem; border-top: 4px solid #8B9F3E; }
    .stat-card { background: white; padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem; border-left: 5px solid #8B9F3E; transition: transform 0.2s; }
    .stat-card:hover { transform: translateY(-3px); box-shadow: 0 4px 15px rgba(139, 159, 62, 0.2); }
    .stat-card.new-data { border-left: 5px solid #FF6B35; background: linear-gradient(to right, #FFF5F0 0%, white 10%); }
    .stat-card.updated-data { border-left: 5px solid #0066A1; background: linear-gradient(to right, #E8F4F8 0%, white 10%); }
    .stat-card.old-data { border-left: 5px solid #95A5A6; background: linear-gradient(to right, #F5F5F5 0%, white 10%); }
    .year-badge { background: linear-gradient(135deg, #0066A1 0%, #0082CC 100%); color: white; padding: 0.5rem 1rem; border-radius: 20px; font-weight: 700; display: inline-block; margin-bottom: 1rem; }
    .new-badge { background: linear-gradient(135deg, #FF6B35 0%, #FF8C42 100%); color: white; padding: 0.4rem 0.9rem; border-radius: 15px; font-weight: 600; margin-left: 0.5rem; }
    .updated-badge { background: linear-gradient(135deg, #0066A1 0%, #0082CC 100%); color: white; padding: 0.4rem 0.9rem; border-radius: 15px; font-weight: 600; margin-left: 0.5rem; }
    .old-badge { background: linear-gradient(135deg, #95A5A6 0%, #7F8C8D 100%); color: white; padding: 0.4rem 0.9rem; border-radius: 15px; font-weight: 600; margin-left: 0.5rem; }
    .stat-text { color: #2C3E50; font-size: 1.05rem; line-height: 1.6; font-family: 'Montserrat', sans-serif; margin: 1rem 0; }
    .read-more-btn { background: linear-gradient(135deg, #8B9F3E 0%, #A8B968 100%); color: white; padding: 0.6rem 1.5rem; border-radius: 25px; text-decoration: none; font-weight: 600; display: inline-block; margin: 0.5rem 0.5rem 0 0; }
    .source-text { color: #7F8C8D; font-size: 0.9rem; margin-top: 0.5rem; }
    .stats-counter { background: linear-gradient(135deg, #0066A1 0%, #0082CC 100%); color: white; padding: 0.75rem 1.5rem; border-radius: 25px; font-weight: 600; display: inline-block; margin-bottom: 1.5rem; }
    .category-title { color: #8B9F3E; font-weight: 700; border-bottom: 3px solid #8B9F3E; padding-bottom: 0.5rem; margin-bottom: 1.5rem; }
    
    /* Linked stat preview box */
    .linked-stat-preview {
        background: #F8F9FA;
        border: 2px solid #0066A1;
        border-radius: 10px;
        padding: 1rem;
        margin-top: 1rem;
        font-family: 'Montserrat', sans-serif;
    }
    .linked-stat-preview.old-version {
        border-color: #95A5A6;
        background: #F5F5F5;
    }
    .linked-stat-preview.updated-version {
        border-color: #0066A1;
        background: #E8F4F8;
    }
    .preview-year {
        background: #0066A1;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.9rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 0.5rem;
    }
    .preview-year.old {
        background: #95A5A6;
    }
    .preview-text {
        color: #2C3E50;
        font-size: 0.95rem;
        line-height: 1.5;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

EXCEL_FILE = '2025 Good Sports Research Project_Aidan Conte.xlsx'

@st.cache_data
def load_data():
    try:
        df = pd.read_excel(EXCEL_FILE, sheet_name='Research', engine='openpyxl')
        df['Category'] = df['Category'].ffill()
        df['Year'] = df['Year'].ffill()
        return df, None
    except Exception as e:
        return None, f"❌ Error: {str(e)}"

@st.cache_resource
def load_workbook():
    try:
        return openpyxl.load_workbook(EXCEL_FILE)
    except:
        return None

def get_hyperlink(workbook, row_index):
    if workbook is None:
        return None
    try:
        sheet = workbook['Research']
        cell = sheet.cell(row=row_index + 2, column=2)
        if cell.hyperlink:
            return cell.hyperlink.target
    except:
        pass
    return None

def extract_row_numbers(text):
    if pd.isna(text):
        return []
    return [int(m) for m in re.findall(r'ROW\s*(\d+)', str(text), re.IGNORECASE)]

def excel_row_to_pandas_index(excel_row):
    return excel_row - 2

def categorize_stat(row, row_index):
    priority = str(row.get('Priority for Updated Stat', '')).strip()
    stat_updated = str(row.get('Stat updated? (see comment)', '')).strip()
    excel_row = row_index + 2
    
    if 79 <= excel_row <= 121:
        if priority == 'New Data':
            return 'new'
        elif 'Updated' in priority and 'ROW' in priority:
            return 'updated'
        else:
            return 'new'
    
    if 'Updated' in priority and 'ROW' in priority:
        return 'updated'
    if stat_updated.startswith('Yes') and 'ROW' in stat_updated:
        return 'old'
    return 'current'

def get_linked_rows(row, row_category):
    if row_category == 'old':
        stat_updated = str(row.get('Stat updated? (see comment)', '')).strip()
        excel_rows = extract_row_numbers(stat_updated)
        return [excel_row_to_pandas_index(r) for r in excel_rows]
    elif row_category == 'updated':
        priority = str(row.get('Priority for Updated Stat', '')).strip()
        excel_rows = extract_row_numbers(priority)
        return [excel_row_to_pandas_index(r) for r in excel_rows]
    return []

# Header
if logo_base64:
    st.markdown(f"""<div class="custom-header"><div class="logo-container"><img src="data:image/png;base64,{logo_base64}"></div>
    <div><h1>Research Statistics Database</h1><p>Comprehensive data supporting youth sports and physical activity initiatives</p></div></div>""", unsafe_allow_html=True)
else:
    st.markdown("""<div class="custom-header"><div><h1>📊 Good Sports Research Statistics</h1>
    <p>Comprehensive data supporting youth sports and physical activity initiatives</p></div></div>""", unsafe_allow_html=True)

# Load data
df, error = load_data()
if error:
    st.error(error)
    st.stop()

workbook = load_workbook()
categories = sorted([cat for cat in df['Category'].unique() if pd.notna(cat)])
df['data_category'] = df.apply(lambda row: categorize_stat(row, row.name), axis=1)

# Filters
st.markdown('<div class="filter-section"><h3>🔍 Filter Research Statistics</h3>', unsafe_allow_html=True)
col1, col2 = st.columns([2, 1])

with col1:
    selected_category = st.selectbox("Select Category:", ["-- All Categories --"] + categories)
with col2:
    data_filter = st.selectbox("Data Status:", ["Current Data", "New Data", "Updated Data", "Old Data"])

st.markdown('</div>', unsafe_allow_html=True)

# Apply filters
if selected_category == "-- All Categories --":
    filtered_df = df.copy()
    display_title = "All Statistics"
else:
    filtered_df = df[df['Category'] == selected_category].copy()
    display_title = selected_category

if data_filter == "New Data":
    filtered_df = filtered_df[filtered_df['data_category'] == 'new']
    display_title += " - New Data"
elif data_filter == "Updated Data":
    filtered_df = filtered_df[filtered_df['data_category'] == 'updated']
    display_title += " - Updated Data"
elif data_filter == "Old Data":
    filtered_df = filtered_df[filtered_df['data_category'] == 'old']
    display_title += " - Old Data"
else:
    filtered_df = filtered_df[filtered_df['data_category'] != 'old']

# Display results
if len(filtered_df) == 0:
    st.info("No statistics found matching your filters.")
else:
    st.markdown(f'<h2 class="category-title">{display_title}</h2>', unsafe_allow_html=True)
    
    total = len(filtered_df)
    new_count = sum(filtered_df['data_category'] == 'new')
    updated_count = sum(filtered_df['data_category'] == 'updated')
    
    stats_info = f'<div class="stats-counter">📈 {total} statistic(s) found'
    if data_filter == "Current Data":
        if new_count > 0:
            stats_info += f' • {new_count} new'
        if updated_count > 0:
            stats_info += f' • {updated_count} updated'
    stats_info += '</div>'
    st.markdown(stats_info, unsafe_allow_html=True)
    
    for idx, (orig_idx, row) in enumerate(filtered_df.iterrows(), 1):
        category = row['data_category']
        card_class = f"stat-card {category}-data" if category != 'current' else "stat-card"
        
        year = row['Year']
        if isinstance(year, float) and not pd.isna(year):
            year = int(year)
        elif pd.isna(year):
            year = "N/A"
        
        stat_text = row['Stat'] if pd.notna(row['Stat']) else "No description available"
        source = row['Source'] if pd.notna(row['Source']) else None
        hyperlink = get_hyperlink(workbook, orig_idx)
        
        # Main stat card
        card_html = f'<div class="{card_class}"><div class="year-badge">📅 {year}</div>'
        
        if category == 'new':
            card_html += '<span class="new-badge">✨ NEW DATA</span>'
        elif category == 'updated':
            card_html += '<span class="updated-badge">🔄 UPDATED</span>'
        elif category == 'old':
            card_html += '<span class="old-badge">📦 OLD VERSION</span>'
        
        card_html += f'<div class="stat-text">{stat_text}</div>'
        if source:
            card_html += f'<div class="source-text">📄 <strong>Source:</strong> {source}</div>'
        
        st.markdown(card_html, unsafe_allow_html=True)
        
        # Get linked stats
        linked_indices = get_linked_rows(row, category)
        
        # Show expanders for linked stats
        if linked_indices:
            for link_idx in linked_indices:
                if 0 <= link_idx < len(df):
                    linked_row = df.iloc[link_idx]
                    link_year = linked_row['Year']
                    if isinstance(link_year, float) and not pd.isna(link_year):
                        link_year = int(link_year)
                    elif pd.isna(link_year):
                        link_year = "N/A"
                    
                    link_stat = linked_row['Stat'] if pd.notna(linked_row['Stat']) else "No description available"
                    link_source = linked_row['Source'] if pd.notna(linked_row['Source']) else None
                    
                    # Create expander label
                    if category == 'old':
                        expander_label = f"🔄 View Updated Version ({link_year})"
                        preview_class = "updated-version"
                        badge_class = ""
                    else:  # category == 'updated'
                        expander_label = f"📜 View Original Data ({link_year})"
                        preview_class = "old-version"
                        badge_class = "old"
                    
                    # Create collapsible expander
                    with st.expander(expander_label):
                        preview_html = f'''
                        <div class="linked-stat-preview {preview_class}">
                            <div class="preview-year {badge_class}">📅 {link_year}</div>
                            <div class="preview-text">{link_stat[:300]}{'...' if len(link_stat) > 300 else ''}</div>
                        '''
                        if link_source:
                            preview_html += f'<div class="source-text">📄 <strong>Source:</strong> {link_source}</div>'
                        preview_html += '</div>'
                        st.markdown(preview_html, unsafe_allow_html=True)
        
        # Article link
        if hyperlink:
            st.markdown(f'<a href="{hyperlink}" target="_blank" class="read-more-btn">🔗 Read Full Article</a>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""<div style="text-align: center; padding: 2rem; color: #7F8C8D; font-family: 'Montserrat', sans-serif; margin-top: 3rem;">
<strong style="color: #8B9F3E;">Good Sports Research Project</strong> | 2025<br>
<em>Empowering youth through sports and physical activity</em></div>""", unsafe_allow_html=True)
