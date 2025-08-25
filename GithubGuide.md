# 🚀 How to Contribute to This Project

Welcome to the team! To keep our codebase clean, stable, and easy to manage, we follow a simple workflow based on feature branches and Pull Requests (PRs).

> **The Golden Rule:** Never push changes directly to the `main` branch. All code must be reviewed and merged via a Pull Request.

---

## 📝 The Workflow: Step-by-Step

Follow these steps every time you want to add a new feature, fix a bug, or make any changes to the code.

### 1. 🔄 Start Fresh: Sync Your Local `main`

Before starting any new work, make sure your local `main` branch is perfectly in sync with the latest version of the project on GitHub.

```bash
# Switch to your local main branch
git checkout main

# Pull the latest changes from the GitHub repository
git pull origin main
```
### 2. 🌿 Create Your Feature BranchCreate a new branch for the specific task you're working on. Give it a descriptive name, using prefixes like feature/, bugfix/, or docs/.# Create a new branch and switch to it immediately
```bash
# Example: git checkout -b feature/user-login
git checkout -b <branch-name>
```
### 3. 💻 Do the Work & Commit Your ChangesNow you can write your code! As you make progress, commit your changes in small, logical chunks. Write clear and concise commit messages that explain what you did.# Stage your changes (add all modified files in the project)
```bash
git add .
# Commit them with a clear, descriptive message
# Example: git commit -m "feat: Add user login form component"
git commit -m "type: A short description of your changes"
```
### 4. ⬆️ Push Your Branch to GitHubWhen you're ready for your code to be reviewed (or you just want to back it up), push your new branch to the remote repository on GitHub.# Push your new branch to the remote repository named 'origin'
```bash
git push origin <branch-name>
```
### 5. 📬 Open a Pull Request (PR), Go to the repository page on GitHub. 
```bash
You should see a yellow banner with your branch name and a button that says "Compare & pull request". Click it. Give your Pull Request a clear title.Write a brief description of the changes you made and why.Assign team members as reviewers.Click "Create pull request".
```
### 6. 💬 Collaborate and ReviseYour teammates will review your code and may request changes. If you need to make updates:Make the required code changes locally in your branch.Commit and push the changes just like you did in steps 3 and 4.
```bash
The Pull Request will automatically update with your new commits.# Make your edits, then...
git add .
git commit -m "fix: Update styling based on reviewer feedback"
git push origin <branch-name>
```
### 7. ✅ After the MergeOnce your PR is approved, a project lead will merge it into the main branch. Your work is now part of the main codebase! You can then safely delete your local branch.# Switch back to the main branch
```bash
git checkout main
```
### Delete the feature branch from your local machine
```bash
git branch -d <branch-name>
```
