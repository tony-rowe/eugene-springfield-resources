# Lane County Community Resource Directory — Streamlit App

A Streamlit version of the Lane County Community Resource Directory for Eugene & Springfield, Oregon. This app provides a searchable, filterable directory of 108 community organizations across 19 categories.

## Features

- **Hero section** with stats and emergency contacts
- **Emergency banner** with immediate help numbers
- **Search** by name, description, or keywords
- **Category filter** dropdown
- **Responsive card layout** with organization details
- **Styled UI** that closely matches the original HTML design
- **Grouped by category** with section headers

## Deployment on Streamlit Community Edition

1. Clone this repository or upload the files to your GitHub repository.
2. Go to [Streamlit Community Edition](https://share.streamlit.io) and connect your repository.
3. Set the main file path to `app.py`.
4. Deploy!

The app uses only Streamlit as a dependency; no additional setup required.

## Files

- `app.py` – Main Streamlit application
- `data.json` – Extracted organization data (parsed from original HTML)
- `final_global.css` – CSS styles (including Google Fonts)
- `requirements.txt` – Python dependencies (Streamlit only)
- `index.html` – Original static page (for reference)

## Data Source

Data was extracted from the original `index.html` file using `parse_data.py`. The parsing script uses BeautifulSoup4 but is not required for runtime.

## Development

To run locally:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Credits

Original design and data compiled by Lane County community resources. This adaptation maintains the visual style and functionality as much as possible within Streamlit's framework.

## License

Community resource – free to use and modify.