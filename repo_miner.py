#!/usr/bin/python3

import datetime
import json
import requests
import os

from pydriller import RepositoryMining
from pydriller.domain.commit import Commit
from typing import Iterable, List

RAW_IST_LOC = "data"

# Mozilla only has one repo, so no need to include it here
RAW_IST_FILES = [
    f"{RAW_IST_LOC}/IST_MIR.csv",
    f"{RAW_IST_LOC}/IST_OST.csv",
    f"{RAW_IST_LOC}/IST_WIK.csv",
]

GITHUB_USERNAMES = ["Mirantis", "openstack", "wikimedia"]

REPO_URLS_LOC = "data/repo_urls.txt"

class UtcTzinfo(datetime.tzinfo):
    """Helper class to compare dates in different timezones."""
    def __init__(self): pass
    def utcoffset(self, dt): return datetime.timedelta(0)
    def dst(self, dt): return 0
    def tzname(self, dt): return "UTC"
    def fromutc(self, dt): return dt

# Do not include commits made on or after this date
DATE_LIMIT = datetime.datetime(2018, 10, 19, tzinfo=UtcTzinfo())


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
        for p in get_project_names_from_csv(f):
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
    Return True if the input url exists.
    """
    return requests.head(url).status_code == 200


def mine_repos(repos: List[str]):
    """
    Mine repos for information about commits using pydriller. This function is very slow when run
    on lots of data!

    Sample JSON output for one repo:

        {
          "url": "https://github.com/mozilla-releng/build-puppet",
          "commits": [{
            "hash": "0d3456eaa47fa44f5adeadc619277c55d90b8adb",
            "msg": "initial site.pp",
            "cmtr": "<pydriller.domain.developer.Developer object at 0x7f1415941b50>",
            "date": "2011-08-22 18:13:36-05:00",
            "files": ["site.pp"]
          },...]
        }
    """

    for repo in repos:
        names = repo.split("/")

        # To facilitate repository analysis, certain global properties should be computed from the
        # commits, eg the list of Puppet files in the entire project.
        pp_files = set()
        pp_committers = set()
        num_pp_commits = 0
        num_tot_commits = 0

        # '{\n  "repos": [\n'  # TODO Use this when merging files
        output_json: str = ""
        
        for commit in RepositoryMining(path_to_repo=repo, to=DATE_LIMIT).traverse_commits():
            if commit_includes_pp_file(commit):
                output_json += make_commit_json(commit)
                pp_files.update(get_modified_pp_files(commit))
                pp_committers.add(get_committer_name(commit))
                num_pp_commits += 1

            num_tot_commits += 1
            # if num_tot_commits == 10: break  # use this to limit the depth if it gets too large

        # [:-8] to remove trailing comma from last commit
        output_json = make_output_json_header(
            repo, pp_files, pp_committers, num_pp_commits, num_tot_commits
        ) + output_json[:-8] + "]\n    }\n"

        with open(f"data/repo_commits/{names[-2]}_{names[-1]}.json", "w+") as f:
            f.write(output_json)

        print(f"Processed {num_pp_commits} Puppet commits out of {num_tot_commits} in total in "
              f"the {repo} repo.")


def commit_includes_pp_file(commit: Commit) -> bool:
    for modification in commit.modifications:
        if modification.filename[-3:] == ".pp":
            return True
    return False


def make_modified_files_list(commit: Commit) -> str:
    """
    Return a string of files which is compatible with JSON arrays, eg ["a", "b", "c"].
    """
    result = "[\n"
    for modification in commit.modifications:
        result += f'            "{modification.new_path}",\n'
    result += "]"
    result = "".join(result.rsplit(",\n", 1))  # remove trailing comma
    return result


def get_modified_pp_files(commit: Commit) -> List[str]:
    result = []
    
    for modification in commit.modifications:
        if modification.filename[-3:] == ".pp":
            result.append(modification.new_path)
    
    return result


def get_committer_name(commit: Commit) -> str:
    return commit.committer.name.replace('"', "").replace("\\", "\\\\")


def make_output_json_header(repo_url: str, pp_files: Iterable[str], pp_committers: Iterable[str],
                            num_pp_commits: int, num_tot_commits: int) -> str:
    return f'''    {{
      "url": "{repo_url}",
      "pp_files": {json.dumps(list(pp_files), indent=8).replace("]", "      ]")},
      "pp_cmtrs": {json.dumps(list(pp_committers))},
      "num_pp_commits": {num_pp_commits},
      "num_tot_commits": {num_tot_commits},
      "commits": ['''


def make_commit_json(commit: Commit) -> str:
    msg = commit.msg.replace("\\", "\\\\").replace("\n", "\\n").replace("\r", "") \
                    .replace("\t", " ").replace('"', '\\\"')
    return f"""{{
        "hash": "{commit.hash}",
        "msg": "{msg}",
        "cmtr": "{get_committer_name(commit)}",
        "date": "{commit.committer_date}",
        "files": {make_modified_files_list(commit)}
      }},\n      """


if __name__ == "__main__":
    urls = get_repo_urls()
    mine_repos(urls)
    #mine_repos(urls[1:2])  # was 6

