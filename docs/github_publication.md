# GitHub publication — commands and safeguards

Git history is initialized locally, but **no remote repository was created or pushed**. Before publishing, confirm the desired GitHub account, verify the repository `automobile-sales-recession-analysis` does not already contain unrelated work, and connect authenticated access. Avoid force pushes.

## Create the remote

Create an **empty public repository** named `automobile-sales-recession-analysis` on GitHub, without auto-generating a README or license (the local project contains them). Check that the intended account owns the repo. From the local repository root:

```bash
git status
git remote -v
git remote add origin https://github.com/YOUR_USERNAME/automobile-sales-recession-analysis.git
git push -u origin main
```

If `origin` already exists, inspect its URL and history before changing it. Never use `git push --force` for an existing remote. The original dataset and any local environment secrets remain ignored by Git. Check the remote file listing and README after push; do not claim publication solely because a command was entered.

## Before presenting the repository as finished

Obtain and inspect the IBM CSV, install dependencies, execute and save the notebook from a clean kernel, run the dashboard in a real browser, generate the two required screenshots, recompute question 3 answers and commit the validated outputs. Follow `docs/validation_report.md` to document actual evidence for each criterion.
