#!/usr/bin/python3

import datetime
import json
import os

from statistics import mean
from typing import List


REPO_URLS_LOC = "data/repo_commits"
PROCESS_METRICS_LOC = "data/process_metrics"

class UtcTzinfo(datetime.tzinfo):
    """Helper class to compare dates in different timezones."""
    def __init__(self): pass
    def utcoffset(self, dt): return datetime.timedelta(0)
    def dst(self, dt): return 0
    def tzname(self, dt): return "UTC"
    def fromutc(self, dt): return dt

DATE_LIMIT = datetime.datetime(2018, 10, 19, tzinfo=UtcTzinfo())


# For large datasets, it is better to combine all this logic in one function
# so only one iteration is needed 

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
    count = 0
    for commit in json_entry["commits"]:
        if script in commit["files"]:
            if is_fix_related(commit["msg"]):
                count += 1
    return count


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
        "file": script,
        "process_metrics": {
            "commits": compute_commits(json_entry, script),
            "developers": compute_developers(json_entry, script),
            "fix_commits": compute_fix_related_commits(json_entry, script),
            "age": compute_age(json_entry, script),
            "avg_edit_time": compute_average_edit_time(json_entry, script)
        }
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

    repo_pm_entries = []
    for json_entry in json_entries:
        print(f"Computing process metrics for {json_entry['url']}")
        names = json_entry['url'].split("/")
        repo_pm_entry = {
            "proj_name": f"{names[-2]}_{names[-1]}",
            "url": json_entry['url'],
            "process_metrics": []
        }
        for script in json_entry["pp_files"]:
            if script is not None:
                repo_pm_entry["process_metrics"].append(
                    compute_process_metrics(json_entry, script))
        repo_pm_entries.append(repo_pm_entry)
    
    print("Writing process metric info to disk. This may take a while...")
    for entry in repo_pm_entries:
        with open(f"{PROCESS_METRICS_LOC}/{entry['proj_name']}.json", "w+") as f:
            f.write(json.dumps(entry, indent=2))


def get_time(date_string) -> datetime.datetime:
    return datetime.datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S%z")


def is_fix_related(commit_msg: str) -> bool:
    commit_msg = commit_msg.lower()
    return "fix" in commit_msg


if __name__ == "__main__":
    compute_process_metrics_for_all_scripts()
