import requests
import time
import random
import os

repo = "tinyhumansai/neocortex"
LIMIT = 20

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
        # -------- STAR CHECK --------
        star_check = requests.get(
            f"https://api.github.com/user/starred/{repo}",
            headers=headers,
            timeout=10
        )

        if star_check.status_code == 204:
            print("Already starred")
        else:
            requests.put(
                f"https://api.github.com/user/starred/{repo}",
                headers=headers,
                timeout=10
            )
            print("Starred")

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

        # -------- FORK --------
        fork = requests.post(
            f"https://api.github.com/repos/{repo}/forks",
            headers=headers,
            timeout=10
        )

        if fork.status_code == 202:
            print("Forked")
        else:
            print(f"Fork failed / already forked ({fork.status_code})")

    except Exception as e:
        print("Error:", e)

    delay = random.randint(5, 15)
    print(f"Waiting {delay} seconds...\n")
    time.sleep(delay)

print("All accounts finished")
