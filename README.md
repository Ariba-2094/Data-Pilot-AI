# DataPilot AI

DataPilot AI is a portfolio project for exploring tabular datasets. This first release creates an interactive dashboard from an uploaded CSV, profiles fields automatically, and applies one shared filter state to KPI cards, charts, and the data table.

## Live features

- Upload a CSV or open the included customer-churn sample
- Detect numeric, date, and categorical columns in the browser
- Generate a histogram, category breakdown, and numeric relationship chart
- Filter categories with multi-select controls
- Filter numeric values with range controls
- Click a category bar to cross-filter the dashboard
- Reset filters and inspect the filtered rows

## Run locally

This release is a static web application. From the `datapilot-ai` directory, serve the files with any local web server:

```powershell
python -m http.server 8000
```

Open `http://localhost:8000` in a browser. Use a local server because the sample dataset is loaded with `fetch`.

## Project roadmap

1. **Interactive analytics** - complete in this prototype.
2. **Backend** - FastAPI upload endpoint, dataset versions, DuckDB aggregates, and saved dashboards.
3. **Machine learning** - target selection, classification/regression pipelines, baseline comparisons, and experiment tracking.
4. **Explainability and AI** - SHAP views, grounded insights, and validated natural-language queries.
5. **Deployment** - CI checks, managed storage, authentication, and a deployed demo.

## Repository structure

```text
datapilot-ai/
├── index.html                 # Dashboard interface
├── app.js                     # Parsing, profiling, filter state, and charts
├── styles.css                 # Responsive design
└── sample-data/               # Safe demo dataset
```

## GitHub checklist

Before publishing, add a dashboard screenshot or short GIF to this README, enable GitHub Pages, and replace this section with the deployed URL. Do not commit private datasets, API keys, or `.env` files.

## Next technical decision

The dashboard currently profiles CSV files locally so it is simple to run and deploy. The next release will add a FastAPI backend and persistent storage while preserving the dashboard's shared filter-state behavior.
