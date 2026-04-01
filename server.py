from flask import Flask, jsonify, render_template, request
import requests

app = Flask(__name__)

API_KEY = "94ccbe0ca2a674bdf04bb15d9d78bca0"

def get_odds():
    url = "https://api.the-odds-api.com/v4/sports/basketball_nba/odds"
    params = {
        "apiKey": API_KEY,
        "regions": "us",
        "markets": "h2h",
        "oddsFormat": "american"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    return []

def get_available_books(games):
    books = set()
    for game in games:
        for bookmaker in game["bookmakers"]:
            books.add(bookmaker["title"])
    return sorted(books)

def find_ev_opportunities(games, sharp):
    opportunities = []
    for game in games:
        bookmakers = {b["title"]: b for b in game["bookmakers"]}
        if sharp not in bookmakers:
            continue
        sharp_outcomes = {}
        for outcome in bookmakers[sharp]["markets"][0]["outcomes"]:
            sharp_outcomes[outcome["name"]] = outcome["price"]
        for book_name, book in bookmakers.items():
            if book_name == sharp:
                continue
            for outcome in book["markets"][0]["outcomes"]:
                team = outcome["name"]
                other_odds = outcome["price"]
                sharp_odds = sharp_outcomes.get(team)
                if sharp_odds is None:
                    continue
                if other_odds > sharp_odds:
                    opportunities.append({
                        "game": f"{game['home_team']} vs {game['away_team']}",
                        "team": team,
                        "sharp": sharp,
                        "sharp_odds": sharp_odds,
                        "book": book_name,
                        "book_odds": other_odds
                    })
    return opportunities

@app.route("/")
def home():
    games = get_odds()
    books = get_available_books(games) if games else []
    return render_template("index.html", books=books)

@app.route("/odds")
def odds():
    sharp = request.args.get("sharp")
    games = get_odds()
    opportunities = find_ev_opportunities(games, sharp)
    return jsonify(opportunities)

@app.route("/books")
def books():
    games = get_odds()
    available_books = get_available_books(games) if games else []
    return jsonify(available_books)

if __name__ == "__main__":
    app.run(debug=True)