import requests
import time
import random
import os

repo = "Solzen33/polymarket-trading-bot"
LIMIT = 5

# get tokens from GitHub Secrets
tokens = os.getenv("TOKENS")

if not tokens:
    raise Exception("No TOKENS found in environment")

tokens = tokens.split(",")

# randomize + limit
random.shuffle(tokens)
tokens = tokens[:LIMIT]

for token in tokens:
    headers = {
        "Authorization": f"token {token.strip()}",
        "Accept": "application/vnd.github.v3+json"
    }

    print("Processing account...")

    try:
        
        # -------- WATCH CHECK --------
        watch_check = requests.get(
            f"https://api.github.com/repos/{repo}/subscription",
            headers=headers,
            timeout=10
        )

        if watch_check.status_code == 200:
            print("Already watching")
        else:
            requests.put(
                f"https://api.github.com/repos/{repo}/subscription",
                headers=headers,
                json={"subscribed": True},
                timeout=10
            )
            print("Watching")

        

    except Exception as e:
        print("Error:", e)

    delay = random.randint(5, 15)
    print(f"Waiting {delay} seconds...\n")
    time.sleep(delay)

print("All accounts finished")
