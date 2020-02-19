from git import Repo
import os

def clone_repo(repo_name, dir_name)
	dirName = "mozilla-releng-build-puppet"

	try:
		os.mkdir(dirName)
		Repo.clone_from("https://github.com/mozilla-releng/build-puppet", dirName)
	except OSError:
		("problem creating directory")


os.chdir("../source-code-repos")

print(os.getcwd())