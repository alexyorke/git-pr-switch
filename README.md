# git-pr-switch
Switches your Git context to a PR, and then back again like nothing happened. This is mostly an experiment, and the code is atrocious--PRs are welcome. 

It lists all open PRs in your Azure DevOps repo, then allows you to choose one to switch to. If there is only one PR open, it will switch to it automatically.

When it switches, it:
- stashes all changes, if any
- fetches all branches from remote
- switches to the PR branch
- pulls branch to get latest changes

When the user is done, it will:
- ask the user to discard any changes (if any were made to the PR.) It will not discard commits; just uncommited changes.
- if not, it will switch to the previous branch the user was on
- re-apply all stashed changes if there was changes originally


## How to run

Log into your Azure DevOps account in Firefox. Change the `GIT_REPO` folder path and the `AZURE_URL` in the script. Then,

`pip3 install -r requirements.txt`
`python3 git-pr-switch.py`

Follow the on-screen prompts.
