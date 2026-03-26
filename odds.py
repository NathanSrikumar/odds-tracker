import requests

API_KEY = "5d7e561bd2a0546feb4ed10b670e745a"

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
    else:
        print(f"Error: {response.status_code}")
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

def main():
    games = get_odds()
    if not games:
        return

    available_books = get_available_books(games)
    print("\nAvailable books:")
    for book in available_books:
        print(f"  {book}")

    sharp = input("\nEnter the sharp book: ").strip()
    if sharp not in available_books:
        print(f"'{sharp}' not found. Check spelling and capitalization.")
        return

    opportunities = find_ev_opportunities(games, sharp)

    if not opportunities:
        print("\nNo +EV opportunities found right now.")
    else:
        print(f"\n+EV opportunities using {sharp} as sharp:\n")
        for o in opportunities:
            print(f"  {o['game']}")
            print(f"  Team: {o['team']}")
            print(f"  {o['sharp']}: {o['sharp_odds']} | {o['book']}: {o['book_odds']}")
            print()

main()