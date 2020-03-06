#!/usr/bin/python3

import datetime
import json
import os

from statistics import mean
from typing import List


REPO_URLS_LOC = "data/tmp" #"data/repo_commits"

class UtcTzinfo(datetime.tzinfo):
    """Helper class to compare dates in different timezones."""
    def __init__(self): pass
    def utcoffset(self, dt): return datetime.timedelta(0)
    def dst(self, dt): return 0
    def tzname(self, dt): return "UTC"
    def fromutc(self, dt): return dt

DATE_LIMIT = datetime.datetime(2018, 10, 19, tzinfo=UtcTzinfo())


def compute_commits(json_entry, script):
    count = 0
    for commit in json_entry["commits"]:
        if script in commit["files"]:
            count += 1
    return count


def compute_developers(json_entry, script):
    if len(json_entry["pp_cmtrs"]) == 1:
        return 1

    count = 0
    devs = set()
    for commit in json_entry["commits"]:
        if script in commit["files"]:
            devs.add(commit["cmtr"])
    return len(devs)


def compute_fix_related_commits(json_entry, script):
    pass


def compute_age(json_entry, script):
    """
    Compute script age in months, as of 19 October 2018.
    """
    for commit in json_entry["commits"]:
        if script in commit["files"]:
            creation_date = get_time(commit["date"])
            break
    
    diff: datetime.timedelta = DATE_LIMIT - creation_date
    return (diff.days + 15) // 30



def compute_average_edit_time(json_entry, script):
    """
    Compute average edit time in days, or zero if the script has not been edited.
    """
    for commit in json_entry["commits"]:
        if script in commit["files"]:
            prev = get_time(commit["date"])
            break
    
    differences: List[datetime.timedelta] = []
    for commit in json_entry["commits"]:
        if script in commit["files"]:
            curr = get_time(commit["date"])
            differences.append((curr - prev).days)
            prev = curr

    return mean(differences)


def compute_process_metrics(json_entry, script):
    """
    Compute process metrics for a given script.
    """
    return {
        "commits": compute_commits(json_entry, script),
        "developers": compute_developers(json_entry, script),
        "fix_commits": compute_fix_related_commits(json_entry, script),
        "age": compute_age(json_entry, script),
        "avg_edit_time": compute_average_edit_time(json_entry, script)
    }


def compute_process_metrics_for_all_scripts():
    print("Loading repository info from disk. This may take a while...")
    json_entries = []
    for json_file in os.listdir(REPO_URLS_LOC):
        with open(os.path.join(REPO_URLS_LOC, json_file)) as f:
            try:
                json_entries.append(json.load(f))
            except Exception as e:
                print(f"❌ Failed to load {json_file} with error:\n{e}.")
    print("Loaded repository info to memory.")

    for json_entry in json_entries:
        print_underline(f"Computing process metrics for {json_entry['url']}")
        for script in json_entry["pp_files"]:
            if script is not None:
                print(f"Process metrics for {script}:")
                process_metrics = compute_process_metrics(json_entry, script)
                print(process_metrics)

        print()


def print_underline(string, maxlen=80):
    """
    Prints a string and underlines it, up to maxlen dashes. Example

        string
        ------
    """
    print(string)
    print("-" * min(len(string), maxlen))


def get_time(date_string) -> datetime.datetime:
    return datetime.datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S%z")


if __name__ == "__main__":
    compute_process_metrics_for_all_scripts()
