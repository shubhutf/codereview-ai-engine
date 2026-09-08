import json
from datetime import datetime
import os

def save_pr_state(state, folder="pr_states"):
    os.makedirs(folder, exist_ok=True)

    filename = f"{folder}/pr_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    with open(filename, "w") as f:
        json.dump(state, f, indent=4)

    return filename