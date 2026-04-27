# Steam Game Review Scraper

A lightweight Python script that scrapes all user reviews for any game on Steam using the official Steam API. It automatically retrieves the game's name, handles pagination smartly, and exports the data into a clean CSV file.

## ✨ Features

* **URL Parsing**: Simply paste the Steam store URL. The script automatically extracts the App ID.
* **Auto Game Name Extraction**: Fetches the official game name directly from the Steam Store API to name your output file dynamically.
* **Smart Scraping Logic**: 
    * Reads the official total review count and stops automatically once all reviews are fetched.
    * Includes a failsafe to stop fetching if Steam stops returning data (accounting for hidden/deleted reviews).
* **Clean CSV Export**: Exports data directly to a UTF-8 (with BOM) encoded CSV file, meaning it opens perfectly in Microsoft Excel without character encoding issues.
* **Rate-Limit Friendly**: Built-in 1-second delay between requests to prevent your IP from being temporarily blocked by Steam.

## 🛠️ Prerequisites

* Python 3.6 or higher
* The `requests` library

## 📦 Installation

1. Clone or download this repository/script.
2. Install the required Python dependency using pip:

```bash
pip install requests
```

## 🚀 Usage

1. Run the script from your terminal or command prompt:

```bash
python user_review_api.py
```

2. When prompted, paste the full URL of the Steam game you want to scrape. For example:
   `🔗 請貼上你要抓取的 Steam 遊戲網址: https://store.steampowered.com/app/1086940/Baldurs_Gate_3/`

3. The script will automatically detect the game name, show the expected review count, and display a real-time progress tracker.

4. Once finished, a CSV file will be generated in the same directory, named formatted as:
   `{Game_Name}_全部評論.csv` (e.g., `Baldurs Gate 3_全部評論.csv`).

## 📊 Output Data Structure

The generated CSV file contains the following three columns:

| Column Header (Original) | English Translation | Description |
| :--- | :--- | :--- |
| **推薦與否** | Recommendation | `推薦` (Recommended) or `不推薦` (Not Recommended). |
| **遊玩時數(小時)** | Playtime (Hours) | Total playtime of the reviewer, rounded to one decimal place. |
| **評論內容** | Review Content | The text body of the review (line breaks are removed for better CSV formatting). |

## ⚠️ Notes

* **Hidden Reviews**: The official "total review count" provided by Steam sometimes includes private or deleted reviews. If the script cannot fetch the exact total number, its built-in failsafe will automatically stop the process once no new data is returned.
* **Public API**: This script uses the public `appreviews` Steam API. No authentication or API keys are required.
