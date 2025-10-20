# 🌏 PHIVOLCS Earthquake Data Scraper

[![Scrape PHIVOLCS Data](https://github.com/zekejulia/phivolcs-earthquake-scraper/actions/workflows/scrape-earthquake-data.yml/badge.svg)](https://github.com/zekejulia/phivolcs-earthquake-scraper/actions/workflows/scrape-earthquake-data.yml)

Automated daily scraping of earthquake data from the [Philippine Institute of Volcanology and Seismology (PHIVOLCS)](https://earthquake.phivolcs.dost.gov.ph/).

## 📊 About This Project

This repository automatically collects and archives earthquake data from PHIVOLCS, providing:
- **Daily automated updates** via GitHub Actions
- **Historical data** for the last 3 years
- **Separate yearly archives** for easy analysis
- **Clean, structured CSV format** ready for data analysis

## 🤖 Automated Updates

- **Schedule:** Daily at 10:00 AM Philippine Time (2:00 AM UTC)
- **Data Source:** [PHIVOLCS Latest Earthquake Information](https://earthquake.phivolcs.dost.gov.ph/EQLatest-Monthly/)
- **No manual intervention required** - Everything runs automatically!

## 📁 Data Files

All earthquake data is stored in the `data/` folder:

| File | Description |
|------|-------------|
| `phivolcs_earthquake_2023.csv` | All earthquakes from 2023 |
| `phivolcs_earthquake_2024.csv` | All earthquakes from 2024 |
| `phivolcs_earthquake_2025.csv` | All earthquakes from 2025 (current year) |
| `phivolcs_earthquake_all_years.csv` | Combined data from all years |

### Data Columns

Each CSV file contains the following columns:

- **Date-Time** - Date and time of the earthquake (Philippine Time)
- **Latitude** - Latitude coordinate (degrees North)
- **Longitude** - Longitude coordinate (degrees East)
- **Depth** - Depth of the earthquake (kilometers)
- **Magnitude** - Earthquake magnitude
- **Location** - Descriptive location of the earthquake
- **Month** - Month name
- **Year** - Year

## 🚀 Quick Start

### View the Data

Simply browse to the [`data/`](./data/) folder to see the latest earthquake data.

### Download the Data

Click on any CSV file in the `data/` folder, then click "Download" or "Raw" to get the data.

### Use in Your Project

You can directly link to the raw CSV files in your applications:

```
https://raw.githubusercontent.com/zekejulia/phivolcs-earthquake-scraper/main/data/phivolcs_earthquake_all_years.csv
```

## 💻 Running Locally

### Prerequisites

```bash
pip install requests pandas lxml html5lib
```

### Run the Scraper

```bash
python scrape_phivolcs.py
```

The script will automatically:
1. Detect the current year
2. Scrape data for the last 3 years
3. Save separate CSV files for each year
4. Create a combined CSV with all data

## 📈 Data Statistics

The scraper provides automatic statistics including:
- Total number of earthquakes per year
- Magnitude distribution
- Top 10 strongest earthquakes
- Monthly breakdown

Example output:
```
📊 Summary by Year:
  • 2023: 15,234 earthquakes
  • 2024: 16,789 earthquakes
  • 2025: 8,456 earthquakes

📈 Total Records: 40,479
```

## 🔧 Configuration

### Change the Scraping Period

Edit `scrape_phivolcs.py` and modify:

```python
YEARS_TO_SCRAPE = 3  # Change to scrape more/fewer years
```

### Change the Schedule

Edit `.github/workflows/scrape-earthquake-data.yml`:

```yaml
on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM UTC (10 AM PHT)
```

**Common schedules:**
- Every 6 hours: `'0 */6 * * *'`
- Every Monday: `'0 2 * * 1'`
- Twice daily: `'0 2,14 * * *'`

[Learn more about cron syntax](https://crontab.guru/)

## 📂 Repository Structure

```
phivolcs-earthquake-scraper/
├── .github/
│   └── workflows/
│       └── scrape-earthquake-data.yml    # GitHub Actions workflow
├── data/
│   ├── phivolcs_earthquake_2023.csv      # 2023 data
│   ├── phivolcs_earthquake_2024.csv      # 2024 data
│   ├── phivolcs_earthquake_2025.csv      # 2025 data
│   └── phivolcs_earthquake_all_years.csv # Combined data
├── scrape_phivolcs.py                    # Main scraper script
└── README.md                             # This file
```

## 🎯 Use Cases

This dataset can be used for:

- 📊 **Data Analysis** - Analyze earthquake patterns and trends
- 🗺️ **Visualization** - Create maps and charts of seismic activity
- 🔔 **Alerts** - Build earthquake notification systems
- 📚 **Research** - Academic research on Philippine seismology
- 🤖 **Machine Learning** - Train models to predict earthquake patterns
- 📱 **Applications** - Build earthquake monitoring apps

## 🛠️ Manual Trigger

You can manually trigger the scraper from GitHub:

1. Go to the **Actions** tab
2. Click **"Scrape PHIVOLCS Earthquake Data"**
3. Click **"Run workflow"**
4. Click the green **"Run workflow"** button

## 📊 Example: Loading Data in Python

```python
import pandas as pd

# Load the latest year's data
df = pd.read_csv('data/phivolcs_earthquake_2025.csv')

# Display basic info
print(f"Total earthquakes: {len(df)}")
print(f"Average magnitude: {df['Magnitude'].mean():.2f}")

# Filter for strong earthquakes (magnitude >= 5.0)
strong_quakes = df[df['Magnitude'] >= 5.0]
print(f"Strong earthquakes: {len(strong_quakes)}")
```

## 📊 Example: Loading Data in R

```r
library(tidyverse)

# Load the data
df <- read_csv('data/phivolcs_earthquake_2025.csv')

# Summary statistics
summary(df$Magnitude)

# Plot magnitude distribution
ggplot(df, aes(x = Magnitude)) +
  geom_histogram(binwidth = 0.5, fill = "steelblue") +
  theme_minimal() +
  labs(title = "Earthquake Magnitude Distribution")
```

## ⚠️ Important Notes

- Data is scraped from publicly available PHIVOLCS sources
- The scraper respects server resources with rate limiting
- Historical data depends on PHIVOLCS archive availability
- Some months may have missing data if not yet published by PHIVOLCS

## 🤝 Contributing

Contributions are welcome! Feel free to:

- Report bugs or issues
- Suggest new features
- Submit pull requests
- Improve documentation

## 📝 Data Source & Attribution

All earthquake data is sourced from:
- **PHIVOLCS** (Philippine Institute of Volcanology and Seismology)
- Official Website: https://earthquake.phivolcs.dost.gov.ph/

This project is for educational and research purposes. Please cite PHIVOLCS as the original data source when using this data.

## 📜 License

This project is open source and available under the [MIT License](LICENSE).

The earthquake data itself belongs to PHIVOLCS and is subject to their terms of use.

## 📧 Contact

For questions or suggestions, please [open an issue](https://github.com/YOUR_USERNAME/phivolcs-earthquake-scraper/issues).

## 🔄 Last Updated

This README was last updated: October 2025

Check the commit history or GitHub Actions runs for the latest data update timestamp.

---

**Made with ❤️ for the Philippine data science community**

If you find this project useful, please ⭐ star the repository!
