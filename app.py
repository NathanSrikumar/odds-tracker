import requests
import tkinter as tk
from tkinter import ttk

API_KEY = "09895d621cabd23c44eab8a9d4c28530"

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

def fetch_and_display():
    results_text.delete("1.0", tk.END)
    sharp = sharp_var.get()
    if not sharp:
        results_text.insert(tk.END, "Please select a sharp book.")
        return
    games = get_odds()
    if not games:
        results_text.insert(tk.END, "Error fetching odds. Check your API key.")
        return
    opportunities = find_ev_opportunities(games, sharp)
    if not opportunities:
        results_text.insert(tk.END, "No +EV opportunities found right now.")
    else:
        for o in opportunities:
            results_text.insert(tk.END, f"Game:       {o['game']}\n")
            results_text.insert(tk.END, f"Team:       {o['team']}\n")
            results_text.insert(tk.END, f"{o['sharp']}:  {o['sharp_odds']}  |  {o['book']}: {o['book_odds']}\n")
            results_text.insert(tk.END, "-" * 50 + "\n")

# build window
root = tk.Tk()
root.title("NBA +EV Odds Tracker")
root.geometry("600x500")
root.resizable(False, False)

# title
title_label = tk.Label(root, text="NBA +EV Odds Tracker", font=("Arial", 16, "bold"))
title_label.pack(pady=15)

# dropdown
sharp_var = tk.StringVar()
games_data = get_odds()
books = get_available_books(games_data) if games_data else []

dropdown_label = tk.Label(root, text="Select Sharp Book:", font=("Arial", 11))
dropdown_label.pack()

dropdown = ttk.Combobox(root, textvariable=sharp_var, values=books, state="readonly", width=30)
dropdown.pack(pady=8)

# button
fetch_button = tk.Button(root, text="Find +EV Opportunities", font=("Arial", 11), command=fetch_and_display)
fetch_button.pack(pady=10)

# results
results_text = tk.Text(root, font=("Courier", 10), wrap=tk.WORD, padx=10, pady=10)
results_text.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

root.mainloop()