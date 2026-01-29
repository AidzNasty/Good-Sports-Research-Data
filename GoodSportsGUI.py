#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 29 09:48:03 2026

@author: aidanconte
"""

import streamlit as st
import pandas as pd
import openpyxl

# Page config
st.set_page_config(page_title="Good Sports Research Statistics", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_excel('/mnt/user-data/uploads/2025 Good Sports Research Project_Aidan Conte.xlsx', 
                       sheet_name='Research')
    return df

@st.cache_resource
def load_workbook():
    return openpyxl.load_workbook('/mnt/user-data/uploads/2025 Good Sports Research Project_Aidan Conte.xlsx')

def get_hyperlink(workbook, row_num):
    """Extract hyperlink from Excel cell"""
    try:
        sheet = workbook['Research']
        # +2 because Excel is 1-indexed and has header row
        cell = sheet.cell(row=row_num + 2, column=2)
        if cell.hyperlink:
            return cell.hyperlink.target
    except:
        pass
    return None

# Main app
st.title("📊 Good Sports Research Statistics")
st.markdown("---")

# Load data
df = load_data()
workbook = load_workbook()

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
                    
                    # Get and display hyperlink
                    hyperlink = get_hyperlink(workbook, orig_idx)
                    if hyperlink:
                        st.markdown(f"[📖 Read More]({hyperlink})")
                    else:
                        # Check if Source has text (even without hyperlink)
                        source = row['Source'] if pd.notna(row['Source']) else None
                        if source:
                            st.caption(f"Source: {source}")
                
                st.markdown("---")
else:
    st.info("👆 Please select a category from the dropdown above to view statistics.")

# Footer
st.markdown("---")
st.caption("Good Sports Research Project | 2025")
