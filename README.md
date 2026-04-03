# NBA +EV Odds Tracker

A web application that identifies positive expected value (+EV) betting 
opportunities across major sportsbooks in real time.

## What It Does

The app fetches live NBA odds from multiple sportsbooks via the Odds API 
and compares them to a user-selected "sharp" book — the book considered 
the most accurate predictor of true probability for a given market. When 
another book offers higher odds on the same outcome, that discrepancy 
represents a +EV opportunity.

## How It Works

- Select a sharp book from the dropdown (e.g. DraftKings, FanDuel)
- Click **Find +EV Opportunities**
- The app fetches live odds, compares all books against your sharp, and 
  displays any discrepancies as cards
- Results auto-refresh every 15 seconds

## Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript
- **Data:** [The Odds API](https://the-odds-api.com)

## Setup

1. Clone the repo
2. Install dependencies: `pip install flask requests`
3. Add your Odds API key to `server.py`
4. Run: `python server.py`
5. Open `localhost:5000` in your browser

## Notes

Built for NBA markets. Odds are displayed in American format.
Free tier API keys have limited monthly requests.