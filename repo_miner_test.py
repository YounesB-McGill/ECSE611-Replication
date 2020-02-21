#!/usr/bin/python3

import json
import os

DATA_PATH = "data/repo_commits"

def test():
    for json_file in os.listdir(DATA_PATH):
        with open(os.path.join(DATA_PATH, json_file)) as f:
            try:
                json_entry = json.load(f)
                print(f"✔️ Successfully loaded {json_file}. The url is {json_entry['url']}.")
            except Exception as e:
                print(f"❌ Failed to load {json_file} with error:\n{e}.")


if __name__ == "__main__":
    test()
