#!/usr/bin/python3

import datetime
import json
import os
import pandas as pd

from statistics import mean
from typing import Dict, List, Tuple


REPO_URLS_LOC = "data/repo_commits"
PROCESS_METRICS_LOC = "data/process_metrics"
FILTERED_PROCESS_METRICS_LOC = "data/filtered_process_metrics"

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


def compute_process_metrics(json_entry: dict, script: str, defect_status: int):
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
            "avg_edit_time": compute_average_edit_time(json_entry, script),
            "defect_status": defect_status
        }
    }


def compute_process_metrics_for_all_scripts():
    json_entries = get_json_entries()

    repo_pm_entries = []
    for json_entry in json_entries:
        print(f"Computing process metrics for {json_entry['url']}")
        names = json_entry['url'].split("/")
        proj_name = f"{names[-2]}_{names[-1]}"
        repo_pm_entry = {
            "proj_name": proj_name,
            "url": json_entry['url'],
            "process_metrics": []
        }
        for script in json_entry["pp_files"]:
            if script is not None:
                ds = get_defect_status_if_known(proj_name, script)
                if ds is not None:
                    repo_pm_entry["process_metrics"].append(
                        compute_process_metrics(json_entry, script, ds))
        repo_pm_entries.append(repo_pm_entry)
    
    print("Writing process metric info to disk. This may take a while...")
    for entry in repo_pm_entries:
        with open(f"{FILTERED_PROCESS_METRICS_LOC}/{entry['proj_name']}.json", "w+") as f:
            f.write(json.dumps(entry, indent=2))


def get_defect_status_if_known(proj_name: str, script: str) -> int:
    fn_ds = get_csv_filenames_and_defect_status_for_all_projects()[proj_name.split("_")[0]]
    if "/" in script:
        script = "/".join(script.split("/")[-2:])
    for n, d in fn_ds:
        #print(script, n)
        if script in n:
            return d



def get_json_entries():
    print("Loading repository info from disk. This may take a while...")
    json_entries = []
    for json_file in os.listdir(REPO_URLS_LOC):
        with open(os.path.join(REPO_URLS_LOC, json_file)) as f:
            try:
                json_entries.append(json.load(f))
            except Exception as e:
                print(f"❌ Failed to load {json_file} with error:\n{e}.")
    print("Loaded repository info to memory.")
    return json_entries


def get_csv_filenames_and_defect_status_for_all_projects() -> Dict[str, List[Tuple[str, int]]]:
    return {
        "Mirantis": get_csv_filenames_and_defect_status("data/IST_MIR.csv"),
        "mozilla-releng": get_csv_filenames_and_defect_status("data/IST_MOZ.csv"),
        "openstack": get_csv_filenames_and_defect_status("data/IST_OST.csv"),
        "wikimedia": get_csv_filenames_and_defect_status("data/IST_WIK.csv")
    }

def get_csv_filenames_and_defect_status(csv) -> List[Tuple[str, int]]:
    return list(zip(get_file_list(csv), get_defect_status(csv)))


def get_file_list(csv: str) -> List[str]:
    files = pd.read_csv(csv)["file_"].tolist()
    files = [fn.split("-downloads/")[1] for fn in files]
    return files


def get_defect_status(csv: str) -> List[int]:
    return pd.read_csv(csv)["defect_status"].tolist()


def get_time(date_string) -> datetime.datetime:
    return datetime.datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S%z")


def is_fix_related(commit_msg: str) -> bool:
    commit_msg = commit_msg.lower()
    return "fix" in commit_msg or "closes-bug" in commit_msg


if __name__ == "__main__":
    compute_process_metrics_for_all_scripts()
    #print(
    #get_csv_filenames_and_defect_status_for_all_projects()
        #)
