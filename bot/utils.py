import os

SEASON_NUMBER = 1
BASE_DIR = f"generated/tweets/season_{SEASON_NUMBER:02d}"
COUNTER_FILE = os.path.join(BASE_DIR, "counter.txt")

def get_next_episode_number():
    os.makedirs(BASE_DIR, exist_ok=True)
    if not os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "w") as f:
            f.write("1")
        return 1
    with open(COUNTER_FILE, "r") as f:
        return int(f.read().strip())

def increment_episode_number(n):
    with open(COUNTER_FILE, "w") as f:
        f.write(str(n + 1))
