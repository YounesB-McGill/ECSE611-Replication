from git import Repo
import os

def clone_repo(repo_name):
	dirName = repo_name.replace('https://github.com/','')
	dirName = dirName.replace('/','-')
	print(dirName)

	checkout_command = 'git checkout "`git rev-list master  -n 1 --first-parent --before=2018-10-20`"'

	try:
		os.mkdir(dirName)
		Repo.clone_from(repo_name, dirName)
		os.chdir(dirName)
		print(os.getcwd())
		os.system(checkout_command)
		os.system('git fetch')
	except OSError:
		("problem creating directory")


os.chdir("../source-code-repos")

print(os.getcwd())

clone_repo('https://github.com/openstack/puppet-octavia')