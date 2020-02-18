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
    This function is much faster. Because all repos here are mentioned in Sec. 3.4 (surveys were
    sent only to developers of valid repos), they must have passed the criteria mentioned in
    Sec. 3.1.1.
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


def mine_repos(repos: List[str]):
    """
    Mines repos for information about commits using pydriller. This function is very slow when run
    on lots of data!

    Sample output:

        32cda6f8735817ed08df40f6154725c7ad956559,change message,Dustin J. Mitchell,2011-08-24 18:05:14-05:00
        e48046ad0a27aa855c32142c8ad71317c540f7e6,initial base-image.sh,Dustin J. Mitchell,2011-08-30 14:21:46-05:00
        cfc25c2cbc4fbdaf6b1563ac7f2942d2568eaf65,update base-image.sh,Dustin J. Mitchell,2011-08-30 14:23:53-05:00
    """

    i = 0
    for commit in RepositoryMining(path_to_repo=repos).traverse_commits():
        
        # TODO We can filter files by type (.pp) using commit.modifications
        print(f"{commit.hash},{commit.msg},{commit.committer.name},{commit.author_date}")

        i += 1
        if i == 5:
            break

    print(f"Total commits: {i}")


if __name__ == "__main__":
    urls = get_repo_urls()
    mine_repos(urls[0:1])

