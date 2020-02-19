from git import Repo
import os

os.chdir("../source-code-repos")

print(os.getcwd())

dirName = "mozilla-releng/build-puppet"

try:
	os.mkdir(dirName)
	Repo.clone_from("https://github.com/mozilla-releng/build-puppet", dirName)
except OSError:
	("problem creating directory")