#!/usr/bin/env python3
from bs4 import BeautifulSoup
import re

with open('index.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'html.parser')

style_tag = soup.find('style')
if style_tag:
    css = style_tag.string
    # Prefix all selectors with .resource-app to scope them
    # This is a simplistic approach; we'll just keep as is for now
    with open('style.css', 'w', encoding='utf-8') as out:
        out.write(css)
    print(f"Written {len(css)} chars to style.css")
else:
    print("No style tag found")