#!/usr/bin/env python3
"""
Streamlit app for Lane County Community Resource Directory
Styled to match original HTML design.
"""
import streamlit as st
import json
from pathlib import Path
from collections import defaultdict

# Load data
@st.cache_data
def load_data():
    with open(Path(__file__).parent / 'data.json', 'r', encoding='utf-8') as f:
        return json.load(f)

# Load CSS
@st.cache_data
def load_css():
    css_path = Path(__file__).parent / 'final_global.css'
    if not css_path.exists():
        st.error(f"CSS file not found: {css_path}")
        return ''
    with open(css_path, 'r', encoding='utf-8') as f:
        return f.read()

def inject_css():
    css = load_css()
    st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)

def render_hero():
    hero_html = """
    <div class="hero" style="background-color: #1c3d2f; color: white; padding: 72px 24px 60px; text-align: center;">
        <div class="hero-badge">Community Resource Directory</div>
        <h1>Lane County Community Resources<br><span style="color: #e09060;">Eugene & Springfield, OR</span></h1>
        <p class="hero-sub">A comprehensive directory of community services and organizations serving Eugene, Springfield, and Lane County, Oregon.</p>
        <div class="hero-stats">
            <div class="stat-pill"><strong>108</strong> organizations</div>
            <div class="stat-pill"><strong>19</strong> categories</div>
            <div class="stat-pill"><strong>24/7</strong> crisis lines</div>
        </div>
    </div>
    """
    st.markdown(hero_html, unsafe_allow_html=True)

def render_emergency_banner():
    banner_html = """
    <div class="emergency-bar" style="background: #7b1e1e; color: #fff; padding: 12px 24px; text-align: center; font-size: 0.85rem; font-weight: 500; letter-spacing: 0.01em;">
        <strong>Need immediate help?</strong> Call <a href="tel:211" style="color: #ffc9a0; text-decoration: none; font-weight: 600;">211</a> for all services or <a href="tel:988" style="color: #ffc9a0; text-decoration: none; font-weight: 600;">988</a> for mental health crisis.
        <span class="divider" style="display: inline-block; margin: 0 12px; opacity: 0.5;">|</span>
        <a href="#sec-crisis" style="color: #ffc9a0; text-decoration: none; font-weight: 600;">Crisis & emergency resources</a>
    </div>
    """
    st.markdown(banner_html, unsafe_allow_html=True)

def render_controls(categories, cat_to_title):
    # Use columns for search and filter buttons
    col1, col2 = st.columns([2, 3])
    with col1:
        search_query = st.text_input("Search organizations", "", key="search",
                                     placeholder="Search by name, keyword, or service...")
    with col2:
        # Filter buttons as a horizontal scroll? Use multiselect or radio
        selected_category = st.selectbox(
            "Filter by category",
            options=["all"] + categories,
            format_func=lambda x: "All Categories" if x == "all" else cat_to_title.get(x, x),
            key="category"
        )
    return search_query, selected_category

def render_card(item):
    # Build tags HTML
    tags_html = ""
    for tag in item['tags']:
        tag_class = ' '.join(tag['class'])
        # Determine style based on class
        style = "font-size: 0.72rem; font-weight: 500; padding: 2px 9px; border-radius: 20px; font-family: 'DM Mono', monospace; letter-spacing: 0.02em;"
        if 'urgent' in tag['class']:
            style += " background: #fde8e8; color: #8b1a1a;"
        elif 'free' in tag['class']:
            style += " background: #e8f5ee; color: #1c5e38;"
        elif 'tag-closing' in tag['class']:
            style += " background: #fff3e6; color: #8a4b00; border: 1px solid #ffb366;"
        else:
            style += " background: #ede6d6; color: #3d3d38;"
        tags_html += f'<span class="{tag_class}" style="{style}">{tag["text"]}</span>'
    
    # Build meta rows HTML
    meta_html = ""
    for meta in item['meta']:
        if meta['type'] == 'link':
            meta_html += f'<div class="meta-row" style="display: flex; align-items: center; gap: 8px; font-size: 0.85rem; color: #6b6b62; margin-top: 4px;"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="flex-shrink: 0;"><path d="M10 13a5 5 0 007.54.54l3-3a5 5 0 00-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 00-7.54-.54l-3 3a5 5 0 007.07 7.07l1.71-1.71"/></svg><a href="{meta["href"]}" target="_blank" rel="noopener" style="color: #4d8c65; text-decoration: none;">{meta["text"]}</a></div>'
        else:
            # Use a generic icon for text (calendar, location, etc.) We'll use a simple icon.
            meta_html += f'<div class="meta-row" style="display: flex; align-items: center; gap: 8px; font-size: 0.85rem; color: #6b6b62; margin-top: 4px;"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="flex-shrink: 0;"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg><span>{meta["text"]}</span></div>'
    
    card_html = f"""
    <article class="org-card cat-{item['category']}" data-cat="{item['category']}" data-search="{item['search_keywords']}" style="background: #ffffff; border-radius: 16px; box-shadow: 0 1px 3px rgba(28,61,47,0.1), 0 1px 2px rgba(28,61,47,0.08); padding: 20px 22px; border: 1px solid rgba(28,61,47,0.07); margin-bottom: 16px;">
        <div class="org-name" style="font-family: 'Playfair Display', serif; font-size: 1.05rem; font-weight: 700; color: #1c3d2f; line-height: 1.25; margin-bottom: 6px;">{item['name']}</div>
        <div class="org-tags" style="display: flex; flex-wrap: wrap; gap: 5px; margin-bottom: 10px;">{tags_html}</div>
        <p class="org-desc" style="font-size: 0.9rem; color: #3d3d38; line-height: 1.5; margin-bottom: 12px;">{item['description']}</p>
        <div class="org-meta" style="display: flex; flex-direction: column; gap: 8px;">{meta_html}</div>
    </article>
    """
    return card_html

def render_section(cat, items, cat_to_title, cat_to_desc):
    # Section header
    icon_map = {
        'crisis': '🚨',
        'housing': '🏠',
        'food': '🍴',
        'health': '🏥',
        'disability': '♿',
        'youth': '👦',
        'seniors': '👵',
        'lgbtq': '🏳️‍🌈',
        'multicultural': '🌍',
        'legal': '⚖️',
        'employment': '💼',
        'education': '📚',
        'arts': '🎨',
        'environment': '🌳',
        'faith': '🛐',
        'animals': '🐾',
        'essential': '🛠️',
        'calendar': '📅',
        'veterans': '🎖️'
    }
    icon = icon_map.get(cat, '📋')
    header_html = f"""
    <div class="section-header" style="display: flex; align-items: center; gap: 14px; margin-bottom: 22px; padding-bottom: 14px; border-bottom: 2px solid rgba(28,61,47,0.1);">
        <div class="section-icon" style="width: 44px; height: 44px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 1.35rem; flex-shrink: 0;">{icon}</div>
        <div>
            <div class="section-title" style="font-family: 'Playfair Display', serif; font-size: 1.5rem; font-weight: 700; color: #1c3d2f; line-height: 1.2;">{cat_to_title.get(cat, cat)}</div>
            <div class="section-desc" style="font-size: 0.84rem; color: #6b6b62; margin-top: 2px;">{cat_to_desc.get(cat, '')}</div>
        </div>
        <span class="section-count" style="margin-left: auto; font-family: 'DM Mono', monospace; font-size: 0.78rem; color: #6b6b62; background: #ede6d6; padding: 3px 10px; border-radius: 20px; flex-shrink: 0;">{len(items)} listing{'s' if len(items) != 1 else ''}</span>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)
    
    # Cards grid: we'll use columns (max 3 per row)
    # Determine number of columns based on screen width, we'll use 3
    cols = st.columns(3)
    for idx, item in enumerate(items):
        col = cols[idx % 3]
        with col:
            card_html = render_card(item)
            st.markdown(card_html, unsafe_allow_html=True)

def main():
    st.set_page_config(
        page_title="Lane County Community Resource Directory — Eugene & Springfield, OR",
        page_icon="🏠",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    
    # Inject CSS
    inject_css()
    
    # Wrap entire app content in resource-app div
    st.markdown('<div class="resource-app">', unsafe_allow_html=True)
    
    # Load data
    data = load_data()
    
    # Extract categories and map to title/desc
    categories = sorted(set(item['category'] for item in data))
    cat_to_title = {}
    cat_to_desc = {}
    for item in data:
        cat = item['category']
        if cat not in cat_to_title:
            cat_to_title[cat] = item['section_title']
            cat_to_desc[cat] = item['section_desc']
    
    # Render hero and emergency banner
    render_hero()
    render_emergency_banner()
    
    # Controls
    st.markdown('<div class="controls">', unsafe_allow_html=True)
    search_query, selected_category = render_controls(categories, cat_to_title)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Filter data
    filtered = []
    for item in data:
        if selected_category != "all" and item['category'] != selected_category:
            continue
        if search_query:
            searchable = f"{item['name']} {item['description']} {item['search_keywords']}".lower()
            if search_query.lower() not in searchable:
                continue
        filtered.append(item)
    
    # Show results count
    if filtered:
        st.markdown(f'<div class="results-count" id="resultsCount" style="font-size: 0.8rem; color: #6b6b62; white-space: nowrap; font-family: \'DM Mono\', monospace;">{len(filtered)} result{"s" if len(filtered) != 1 else ""}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="empty-state visible" id="emptyState" style="text-align: center; padding: 40px 20px; color: #6b6b62;"><p>No organizations match your search. Try a different keyword or category.</p></div>', unsafe_allow_html=True)
    
    # Group filtered data by category
    grouped = defaultdict(list)
    for item in filtered:
        grouped[item['category']].append(item)
    
    # Main content container
    st.markdown('<main class="main">', unsafe_allow_html=True)
    
    # Render each category section
    for cat, items in sorted(grouped.items(), key=lambda kv: cat_to_title.get(kv[0], kv[0])):
        render_section(cat, items, cat_to_title, cat_to_desc)
    
    st.markdown('</main>', unsafe_allow_html=True)
    
    # Footer
    footer_html = """
    <footer>
        <p><strong>Eugene & Springfield Community Resource Directory</strong></p>
        <p>Serving Lane County, Oregon · Built for and by the community</p>
        <p style="margin-top:12px;">
            Always verify hours and availability directly with each organization.<br>
            For immediate needs call <strong>211</strong> (all services) or <strong>988</strong> (mental health crisis).<br>
            To suggest an addition or correction, please <a href="https://github.com">open an issue on GitHub</a>.
        </p>
        <p style="margin-top:16px; font-size:.78rem;">
            Data compiled from Lane County public records, 211info.org, Eugene Public Library, and verified organizational websites.
            Not affiliated with any individual organization. Updated April 2026.
        </p>
    </footer>
    """
    st.markdown(footer_html, unsafe_allow_html=True)
    
    # Close resource-app div
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == '__main__':
    main()