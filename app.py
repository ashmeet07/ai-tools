import streamlit as st
import json
import os

# Load tools data
with open("data/tools.json", "r", encoding="utf-8") as f:
    tools_data = json.load(f)

# Deduplicate categories
seen = set()
filtered_tools_data = []
for item in tools_data:
    if item['category'] not in seen:
        filtered_tools_data.append(item)
        seen.add(item['category'])

# Streamlit config
st.set_page_config(page_title="🧠 100 AI Tools Directory", layout="wide")
st.markdown("<h1 class='title'>🧠 100 AI Tools Directory</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Explore 100+ categories of curated AI tools. Click any to learn more!</p>", unsafe_allow_html=True)

# Load custom CSS
def load_css(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css(os.path.join("style", "style.css"))

# Sidebar filters
st.sidebar.markdown("## 🔎 Filter Tools")
categories = sorted([item["category"] for item in filtered_tools_data])
selected_category = st.sidebar.selectbox("📂 Select a Category", categories)
search_query = st.sidebar.text_input("🔍 Search (Name or Description)")

# Filter logic
display_tools = []
for category_item in filtered_tools_data:
    if category_item["category"] == selected_category:
        for tool in category_item["tools"]:
            if search_query.lower() in tool["name"].lower() or search_query.lower() in tool["description"].lower():
                display_tools.append(tool)

display_tools.sort(key=lambda x: x['name'].lower())

# Responsive grid display
cols = st.columns(3)

for idx, tool in enumerate(display_tools):
    col = cols[idx % 3]
    pricing_class = tool['pricing'].replace(" ", "")
    with col:
        st.markdown(f"""
            <div class="tool-card">
                <img src="{tool['logo']}" alt="{tool['name']} logo" class="tool-logo" onerror="this.style.display='none'" />
                <div class="tool-content">
                    <h3 class="tool-title">{tool['name']} <span class="badge {pricing_class}">{tool['pricing']}</span></h3>
                    <p class="tool-description">{tool['description']}</p>
                    <a href="{tool['link']}" class="visit-button" target="_blank">🌐 Visit Tool</a>
                </div>
            </div>
        """, unsafe_allow_html=True)

if not display_tools:
    st.warning("😕 No tools found matching your search.")
