#!/usr/bin/python3

import requests

from pydriller import RepositoryMining
from typing import List

RAW_IST_LOC = "data"

# Mozilla only has one repo, so no need to include it here
RAW_IST_FILES = [
    f"{RAW_IST_LOC}/IST_MIR.csv",
    f"{RAW_IST_LOC}/IST_OST.csv",
    f"{RAW_IST_LOC}/IST_WIK.csv",
]

GITHUB_USERNAMES = ["Mirantis", "openstack", "wikimedia"]

REPO_URLS_LOC = "data/repo_urls.txt"


def get_repo_urls() -> List[str]:
    """
    Returns a list of valid URLs which were precomputed using get_repo_urls_from_raw_data().
    This function is much faster.
    """
    urls = []

    with open(REPO_URLS_LOC) as f:
        for line in f.readlines():
            urls.append(line.replace("\n", ""))        

    return urls



def get_repo_urls_from_raw_data() -> List[str]:
    """
    Returns a list of valid URLs based on the raw data files.
    """
    urls = ["https://github.com/mozilla-releng/build-puppet"]

    for u, f in zip(GITHUB_USERNAMES, RAW_IST_FILES):
        project_names = get_project_names_from_csv(f)
        for p in project_names:
            url = make_repo_url(u, p)
            if url_exists(url):
                urls.append(url)

    return urls


def get_project_names_from_csv(filename: str) -> List[str]:
    """
    Returns a list of project names from the given raw data file
    """
    names = set()

    with open(filename) as f:
        lines = f.readlines()

    for line in lines[1:-1]:
        names.add(line.split(",")[1].split("-downloads/")[1].split("/")[0])

    return list(names)


def make_repo_url(github_username: str, project_name: str) -> str:
    return f"https://github.com/{github_username}/{project_name}"


def url_exists(url: str) -> bool:
    """
    Returns True if the input url exists.
    """
    return requests.head(url).status_code == 200


# TODO Use RepositoryMining to get information about each repo

# i = 0
# for commit in RepositoryMining(path_to_repo=REPO_URLS).traverse_commits():
#     print(commit)
#     i += 1
#     print(f"commit {commit.hash}, date {commit.author_date}")

# print(f"Total commits: {i}")

if __name__ == "__main__":
    urls = get_repo_urls()
    for url in urls:
        print(url)

