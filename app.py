import streamlit as st
import json
import os

# Load tools data from JSON
with open("data/tools.json", "r", encoding="utf-8") as f:
    tools_data = json.load(f)

# Remove duplicate categories, keep only first occurrence
seen = set()
filtered_tools_data = []
for item in tools_data:
    if item['category'] not in seen:
        filtered_tools_data.append(item)
        seen.add(item['category'])

# Streamlit config
st.set_page_config(page_title="🧠 100 AI Tools Directory", layout="wide")
st.title("🧠 100 AI Tools Directory")
st.markdown("Browse 100 categories of AI tools with references. Click to explore!")

# Load CSS file and inject styles
def load_css(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css(os.path.join("style", "style.css"))

# Sidebar for filters
st.sidebar.header("Filter Tools")
categories = sorted([item["category"] for item in filtered_tools_data])
selected_category = st.sidebar.selectbox("Select a Category", categories)

search_query = st.sidebar.text_input("Search Tools (name or description)")

# Filter tools by category and search query
display_tools = []
for category_item in filtered_tools_data:
    if category_item["category"] == selected_category:
        for tool in category_item["tools"]:
            # Filter by search query (case-insensitive)
            if search_query.lower() in tool["name"].lower() or search_query.lower() in tool["description"].lower():
                display_tools.append(tool)

# Sort tools alphabetically by name
display_tools.sort(key=lambda x: x['name'].lower())

# Display tools in a grid with cards
cols = st.columns(3)  # 3 columns grid

for idx, tool in enumerate(display_tools):
    col = cols[idx % 3]
    pricing_class = tool['pricing'].replace(" ", "")  # For CSS class usage
    
    with col:
        st.markdown(f"""
            <div class='tool-box' style='min-height: 180px; margin-bottom: 1rem;'>
                <img class='tool-logo' src="{tool['logo']}" alt="{tool['name']} logo" onerror="this.style.display='none'" />
                <div class='tool-info'>
                    <div class='tool-name'>{tool['name']} <span class='pricing {pricing_class}'>{tool['pricing']}</span></div>
                    <div class='tool-desc'>{tool['description']}</div>
                    <a class='tool-link' href="{tool['link']}" target='_blank'>🌐 Visit Tool</a>
                </div>
            </div>
        """, unsafe_allow_html=True)

if not display_tools:
    st.info("No tools found matching your search.")

