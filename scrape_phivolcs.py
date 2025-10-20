import requests
import pandas as pd
from datetime import datetime
import urllib3
from io import StringIO
import time
import os

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

MONTH_NAMES = ["January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"]

def scrape_phivolcs_data_from_html(year, month_name):
    """
    Fetches earthquake data by reading the HTML table from the PHIVOLCS monthly page.
    """
    url = (
        f"https://earthquake.phivolcs.dost.gov.ph/EQLatest-Monthly/"
        f"{year}/{year}_{month_name}.html"
    )
    
    try:
        print(f"  Fetching: {month_name} {year}...", end=" ")
        
        session = requests.Session()
        session.verify = False 
        
        response = session.get(url, timeout=15)
        response.raise_for_status()
        
        # Parse HTML tables
        tables = pd.read_html(StringIO(response.text), skiprows=1)
        
        # Find the table with earthquake data
        df = None
        for table in tables:
            if table.shape[1] >= 5:
                df = table
                break
        
        if df is None or df.empty:
            print(f"✗ No data")
            return None
        
        # Set column names
        expected_columns = [
            'Date-Time',
            'Latitude',
            'Longitude',
            'Depth',
            'Magnitude',
            'Location'
        ]
        
        if df.shape[1] == 6:
            df.columns = expected_columns
        elif df.shape[1] > 6:
            df = df.iloc[:, :6]
            df.columns = expected_columns
        else:
            print(f"✗ Invalid columns ({df.shape[1]})")
            return None
        
        # Remove header rows
        mask = (
            df['Date-Time'].astype(str).str.contains('Date|Time|Philippine', case=False, na=False) |
            df['Latitude'].astype(str).str.contains('Latitude|ºN|°N', case=False, na=False) |
            df['Longitude'].astype(str).str.contains('Longitude|ºE|°E', case=False, na=False)
        )
        df = df[~mask].reset_index(drop=True)
        
        # Remove summary and month abbreviation rows
        if not df.empty:
            first_col = df.iloc[:, 0].astype(str).str.strip()
            summary_mask = first_col.str.lower().str.contains('total|no. of events', na=False, regex=True)
            month_abbrev_mask = first_col.str.match(r'^[A-Z][a-z]{2}-\d{2}$', na=False)
            df = df[~(summary_mask | month_abbrev_mask)]
        
        # Remove empty rows
        df = df.dropna(how='all').reset_index(drop=True)
        
        # Add metadata columns
        df['Month'] = month_name
        df['Year'] = year
        
        print(f"✓ {len(df)} records")
        
        return df
        
    except requests.exceptions.HTTPError as errh:
        print(f"✗ HTTP {errh.response.status_code}")
        return None
    except Exception as e:
        print(f"✗ Error: {e}")
        return None


def scrape_year_data(year, output_dir="data"):
    """
    Scrapes earthquake data for all months in a given year.
    Returns the combined DataFrame for that year.
    """
    print(f"\n{'─'*70}")
    print(f"📅 Scraping Year: {year}")
    print(f"{'─'*70}")
    
    all_data = []
    successful_months = []
    failed_months = []
    
    for month_name in MONTH_NAMES:
        df = scrape_phivolcs_data_from_html(year, month_name)
        
        if df is not None and not df.empty:
            all_data.append(df)
            successful_months.append(month_name)
        else:
            failed_months.append(month_name)
        
        # Be polite to the server
        time.sleep(0.5)
    
    # Combine and save data for this year
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Save to separate file for this year
        output_filename = os.path.join(output_dir, f"phivolcs_earthquake_{year}.csv")
        combined_df.to_csv(output_filename, index=False, encoding='utf-8-sig')
        
        print(f"\n✓ Year {year} Complete:")
        print(f"  • Total records: {len(combined_df)}")
        print(f"  • Successful months: {len(successful_months)}")
        print(f"  • File saved: {output_filename}")
        
        return combined_df
    else:
        print(f"\n✗ No data retrieved for {year}")
        return None


def scrape_multiple_years(years_back=3, output_dir="data"):
    """
    Scrapes earthquake data for the last N years.
    Each year is saved as a separate CSV file.
    """
    current_year = datetime.now().year
    start_year = current_year - years_back + 1
    
    print(f"\n{'='*70}")
    print(f"🌏 PHIVOLCS EARTHQUAKE DATA SCRAPER")
    print(f"{'='*70}")
    print(f"📊 Scraping Range: {start_year} - {current_year}")
    print(f"📁 Output Directory: {output_dir}/")
    print(f"{'='*70}")
    
    all_years_data = []
    scrape_summary = {}
    
    # Scrape each year
    for year in range(start_year, current_year + 1):
        df = scrape_year_data(year, output_dir)
        
        if df is not None:
            all_years_data.append(df)
            scrape_summary[year] = len(df)
        else:
            scrape_summary[year] = 0
    
    # Create a combined file with all years
    if all_years_data:
        combined_all = pd.concat(all_years_data, ignore_index=True)
        combined_filename = os.path.join(output_dir, f"phivolcs_earthquake_all_years.csv")
        combined_all.to_csv(combined_filename, index=False, encoding='utf-8-sig')
        
        # Print final summary
        print(f"\n{'='*70}")
        print(f"✅ SCRAPING COMPLETE!")
        print(f"{'='*70}")
        print(f"\n📊 Summary by Year:")
        for year, count in scrape_summary.items():
            print(f"  • {year}: {count:,} earthquakes")
        print(f"\n📈 Total Records: {len(combined_all):,}")
        print(f"\n📁 Files Created:")
        for year in range(start_year, current_year + 1):
            if scrape_summary.get(year, 0) > 0:
                print(f"  • {output_dir}/phivolcs_earthquake_{year}.csv")
        print(f"  • {output_dir}/phivolcs_earthquake_all_years.csv (combined)")
        print(f"\n{'='*70}\n")
        
        return combined_all, scrape_summary
    else:
        print(f"\n✗ No data was retrieved for any year.")
        return None, {}


def display_statistics(df):
    """
    Display basic statistics about the scraped data.
    """
    if df is None or df.empty:
        return
    
    print(f"{'='*70}")
    print(f"📈 DATA STATISTICS")
    print(f"{'='*70}\n")
    
    # Magnitude statistics
    print("🔢 Magnitude Statistics:")
    print(df['Magnitude'].describe())
    
    # Yearly breakdown
    print(f"\n📅 Earthquakes by Year:")
    yearly_counts = df.groupby('Year').size().sort_index()
    for year, count in yearly_counts.items():
        print(f"  • {year}: {count:,} earthquakes")
    
    # Top 10 strongest earthquakes
    print(f"\n💥 Top 10 Strongest Earthquakes:")
    top_10 = df.nlargest(10, 'Magnitude')[['Date-Time', 'Magnitude', 'Location', 'Year']]
    for idx, row in top_10.iterrows():
        print(f"  • Mag {row['Magnitude']} - {row['Location'][:50]} ({row['Year']})")
    
    print(f"\n{'='*70}\n")


if __name__ == "__main__":
    # Configuration
    YEARS_TO_SCRAPE = 3  # Last 3 years (including current year)
    OUTPUT_DIR = "data"
    
    # Run the scraper
    combined_df, summary = scrape_multiple_years(
        years_back=YEARS_TO_SCRAPE,
        output_dir=OUTPUT_DIR
    )
    
    # Display statistics
    if combined_df is not None:
        display_statistics(combined_df)
