#!/usr/bin/env python3
"""
Transform CSS by prefixing selectors with .resource-app, except for :root and @rules.
"""
import re

def transform_css(css_text):
    # Keep :root block unchanged
    # For each rule block, prefix selectors
    lines = css_text.split('\n')
    output = []
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        # Skip empty lines
        if not line.strip():
            output.append(line)
            i += 1
            continue
        # Check if line starts with @ or :root
        stripped = line.strip()
        if stripped.startswith('@') or stripped.startswith(':root'):
            # Keep as is, include until closing brace
            # Find matching brace (simplistic: assume @ rule ends with } on same line or later)
            output.append(line)
            # Count braces
            open_braces = line.count('{') - line.count('}')
            while open_braces > 0 and i + 1 < len(lines):
                i += 1
                next_line = lines[i]
                output.append(next_line)
                open_braces += next_line.count('{') - next_line.count('}')
            i += 1
            continue
        # Check if line contains '{' (start of rule)
        if '{' in line:
            # Prefix selectors before '{'
            parts = line.split('{', 1)
            selectors = parts[0]
            # Split selectors by comma, prefix each
            selector_list = [s.strip() for s in selectors.split(',')]
            prefixed = []
            for sel in selector_list:
                # Skip empty
                if not sel:
                    continue
                # Don't prefix if already starts with .resource-app
                if sel.startswith('.resource-app'):
                    prefixed.append(sel)
                else:
                    prefixed.append('.resource-app ' + sel)
            new_selectors = ', '.join(prefixed)
            output.append(new_selectors + ' {' + parts[1])
            i += 1
            continue
        # Regular line
        output.append(line)
        i += 1
    
    return '\n'.join(output)

def main():
    with open('style.css', 'r', encoding='utf-8') as f:
        css = f.read()
    transformed = transform_css(css)
    with open('transformed.css', 'w', encoding='utf-8') as f:
        f.write(transformed)
    print("Transformed CSS written to transformed.css")

if __name__ == '__main__':
    main()