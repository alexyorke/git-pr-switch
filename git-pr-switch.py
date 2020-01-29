import browser_cookie3
import requests
import json
import subprocess
gitFolderPath = r"GIT_FOLDER_PATH"
url = "https://dev.azure.com/COMPANY_NAME/_apis/git/repositories/REPO_ID/pullRequests"

prevBranchWorkingDirChanges = subprocess.check_output(r'cd ' + gitFolderPath + ' && git diff', shell=True).decode("utf-8").strip()
prevBranch = subprocess.check_output(r'cd ' + gitFolderPath + ' && git rev-parse --abbrev-ref HEAD', shell=True).decode("utf-8").strip()

cj = browser_cookie3.firefox()

r = requests.get(url, cookies=cj, stream=True)

prs = {}

for pr in json.loads(r.content)['value']:
    prId = str(pr['pullRequestId'])
    title = pr['title']
    branchName = pr['sourceRefName'].replace("refs/heads/", "")

    print("#" + prId + ": " + title + " - " + branchName)
    prs[prId] = {"title": title, "branchName": branchName}

branchToSwitchTo = None
prId = list(prs.keys())[0]
if (len(prs) > 1):
    while True:
        prId = input("Type the PR number you want to switch to: ")
        if prId in prs:
            branchToSwitchTo = prs[prId]['branchName']
        else:
            print("Not found, try again.")
else:
    branchToSwitchTo = prs[list(prs.keys())[0]]['branchName']

subprocess.call(r'cd ' + gitFolderPath + ' && git stash && git fetch --all && git checkout ' + prs[prId]['branchName'] + " && git pull --rebase", shell=True)

toPrint = "Reviewing #" + str(prId) + ": " + prs[prId]['title']
print()
print("=" * len(toPrint))
print(toPrint)
print("=" * len(toPrint))
print()
print("Previous branch: " + prevBranch + ". Press enter to return to branch.")
input()

# check for changes made to the PR that have not been committed
workingDirChanges = subprocess.check_output(r'cd ' + gitFolderPath + ' && git diff', shell=True).decode("utf-8").strip()
if (len(workingDirChanges) > 0):
    print("Discard changes made in PR? (y/n)")
    if (input().lower().strip() == "yes" or input().lower().strip() == "ye" or input().lower().strip() == "y"):
        subprocess.call(r'cd ' + gitFolderPath + ' && git reset --hard', shell=True)
    else:
        print("Cancelling...")
        exit()

# check if we stashed any changes; if not, we should not apply the stash as it could be something else
if len(prevBranchWorkingDirChanges) > 0:
    subprocess.call(r'cd ' + gitFolderPath + ' && git checkout ' + prevBranch + " && git stash apply", shell=True)
else:
    subprocess.call(r'cd ' + gitFolderPath + ' && git checkout ' + prevBranch, shell=True)
    
