Contributing to inet
inet is an open source software package, and we welcome community contributions. You can find the source code and test code for inet in the inet git repository on GitHub. This document covers what you should do to contribute to inet.

Submissions

Bug fixes, new features and documentation updates will all be considered for merging into the codebase, but when considering submitting a new feature you should begin by posting an issue to the inet issue tracker.

If you are filing a bug report, please include:

The exact command or function call that you issue to create the bug.
Any supporting data required to recreate the bug (please keep these to the minimum necessary to recreate the issue).
Submitting code to inet

inet uses GitHub's Pull Request mechanism for accepting submissions. To submit code, use the following steps:

Begin by creating an issue describing your proposed change. This should include a description of your proposed change (is it a new feature, a bug fix, etc.), and note in the issue description that you want to work on it.

Fork the inet repository on the GitHub website to your GitHub account.

Clone your forked repository to the system where you'll be developing with git clone.

Ensure that you have the latest version of all files (especially important if you cloned a long time ago, but you'll need to do this before submitting changes regardless). You should do this by adding inet as a remote repository and then pulling from that repository. You'll only need to run the git remote step one time:

git checkout master
git remote add upstream https://github.com/nestauk/inet.git
git pull upstream master
Create a new feature branch that you will make your changes in with:

git checkout -b feature-name-of-feature develop
Install the required libraries:

pip install -r requirements.txt
Confirm that all the tests pass before you make any changes:

py.test tests/
Make your changes, add them (with git add), and commit them (with git commit). Don't forget to update and/or add associated tests as necessary. You should make incremental commits, rather than one massive commit at the end. Write descriptive commit messages to accompany each commit.

When you think you're ready to submit your code, again ensure that you have the latest version of all files in case some changed while you were working on your edits. You can do this by merging develop into your topic branch:

git checkout feature-name-of-feature
git pull upstream develop
Run py.test tests/ --cov inet --cov-report term-missing to ensure that your changes did not cause anything unexpected to break and that your tests cover 100% of any relevant code you have added.

Once the tests pass and coverage is at 100%, you should merge your changes into your local develop branch using the --no-ff flag to ensure commit objects are always created:

git checkout develop
git merge --no-ff feature-name-of-feature
The feature branch can then be deleted before pushing the repo to your remote forked repo:

git branch -d myfeature
git push origin develop
Issue a pull request on the GitHub website to request that we merge your branch's changes into inet's develop branch. If changes are requested don't issue a new pull request. You should make changes on your topic branch, and commit and push them to GitHub. Your pull request will update automatically.

Coding Guidelines

inet adheres to the PEP 8 python coding guidelines for code and documentation standards. Before submitting any code to inet, you should read these carefully and apply the guidelines in your code.

Testing Guidelines

All code that is added to inet must be unit tested, and the unit test code must be submitted in the same pull request as the library code that you are submitting. code that is not unit tested will not be merged.

Getting help with git
If you're new to git, you'll probably find gitref.org helpful.

Thanks to QIIME Project from who's CONTRIBUTING.md these instructions were developed.
