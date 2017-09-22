# Contributing
This document outlines key considerations for anyone contributing to the Sleuth repository.

## Repository Structure
Source code will be organized into three main folders within the Sleuth repository:

### sleuth_frontend
This is where all the client-side code will live. File and directory structure under this folder will be governed by React conventions.

### sleuth_backend
This is where all the server-side code will live. File and direcotry structure under this folder will be largely governed by Django conventions.

### sleuth_crawler
This is where all the crawler code will live. Structure here is largely up to the developers.

## Branching and Pull Requests
The main branch for this repository will be `master`. When a developer starts work on a new issue, the developer will create a new branch with a name in the form `<issue-number>-<dash separated issue title>`. For example, if your issue is number 5, and it's title is "Set up Sleuth Repository", your branch should be called something like `5-repo-setup`. Once the issue branch has been created, the developer will write code and commit it to that branch, pushing commits to the upstream branch as he/she develops. When the developer has finished work on an issue the developer will create a pull request (PR) against `master` on Github and fill out the pull request template with information about the PR. Other contributors will then review the PR, and once it has been approved and all tests are passing on that branch it can be merged into `master`. Developers should ensure that their branch is up to date with `master` (i.e all the code in `master` should also be in your branch) when they create PRs.

Here's an example of a full sprint development cycle.
```Shell
# Make sure you are up to date with master before branching
$ git pull origin master
# Create new branch for issue
$ git checkout -b 10-add-search
# Do some coding, then commit and push your progress
$ git status
$ git add .
$ git commit
# Fill out commit description and push (set upstream if this is your first push for this new branch)
$ git push --set-upstream origin 10-add-search
# Keep coding, commiting, and pushing your changes
```

## Issue Tracking
All issues will be tracked using the ZenHub Chrome extension. During weekly meetings, contributors will generally be asisgned 1-2 issues to work on for the week and should have completed their assigned issues by the following meeting. The life-cycle of an issue should generally be Backlog > Assign issue to developer > In Progress > Up for Review > Approved > Closed.

## Code Style and Best Practice
### Python
Python code should all follow the [PEP8 Style](https://www.python.org/dev/peps/pep-0008/). It is recommended that you use a good text editor like [VSCode](https://code.visualstudio.com/) that will allow you to install plugins to do code linting for you.
### JavaScript
JavaScript should generally follow [ES6 Style](https://github.com/airbnb/javascript). Again, using a strong editor with JS linting will be important here.
### Testing
All code changes must come with unit tests - we want to keep code coverage at or above 70%. PRs without tests will not be approved.
We will be using [Travis CI](https://travis-ci.org/) to automatically build and run tests automatically when we push or issue PRs.


