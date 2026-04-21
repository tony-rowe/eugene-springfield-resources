#!/usr/bin/env python3
"""
Parse the index.html file and extract organization data.
Output as JSON for use in Streamlit app.
"""
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup

def parse_html(html_file):
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    
    # Find all category sections
    sections = soup.find_all('section', class_='category-section')
    data = []
    
    for section in sections:
        cat = section.get('data-cat')
        # Section title
        header = section.find('div', class_='section-header')
        if header:
            title_elem = header.find('div', class_='section-title')
            title = title_elem.get_text(strip=True) if title_elem else ''
            desc_elem = header.find('div', class_='section-desc')
            desc = desc_elem.get_text(strip=True) if desc_elem else ''
        else:
            title = desc = ''
        
        # Process each org card in this section
        cards = section.find_all('article', class_='org-card')
        for card in cards:
            # data-cat may be overridden per card
            card_cat = card.get('data-cat', cat)
            search = card.get('data-search', '')
            
            org_name = card.find('div', class_='org-name')
            org_name_text = org_name.get_text(strip=True) if org_name else ''
            
            org_tags = card.find('div', class_='org-tags')
            tags = []
            if org_tags:
                for tag in org_tags.find_all('span', class_='tag'):
                    tag_text = tag.get_text(strip=True)
                    tag_class = tag.get('class', [])
                    tags.append({
                        'text': tag_text,
                        'class': tag_class
                    })
            
            org_desc = card.find('p', class_='org-desc')
            desc_text = org_desc.get_text(strip=True) if org_desc else ''
            
            # Meta rows: each meta-row contains either a link or text
            meta_rows = card.find_all('div', class_='meta-row')
            meta = []
            for row in meta_rows:
                # Extract icon type? ignore for now
                # Look for links and spans
                link = row.find('a')
                if link:
                    href = link.get('href', '')
                    text = link.get_text(strip=True)
                    meta.append({
                        'type': 'link',
                        'href': href,
                        'text': text
                    })
                else:
                    # plain text
                    span = row.find('span')
                    if span:
                        text = span.get_text(strip=True)
                        meta.append({
                            'type': 'text',
                            'text': text
                        })
                    else:
                        # maybe just text content
                        text = row.get_text(strip=True)
                        meta.append({
                            'type': 'text',
                            'text': text
                        })
            
            data.append({
                'category': card_cat,
                'section_title': title,
                'section_desc': desc,
                'search_keywords': search,
                'name': org_name_text,
                'tags': tags,
                'description': desc_text,
                'meta': meta
            })
    
    return data

def main():
    html_file = Path(__file__).parent / 'index.html'
    data = parse_html(html_file)
    
    # Save as JSON
    output = Path(__file__).parent / 'data.json'
    with open(output, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"Extracted {len(data)} entries to {output}")
    
    # Print categories and counts
    from collections import Counter
    cats = Counter([d['category'] for d in data])
    print("Categories:", cats)

if __name__ == '__main__':
    main()