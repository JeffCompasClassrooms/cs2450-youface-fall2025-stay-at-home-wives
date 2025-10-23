#Git How-To CheatSheet

Best practices uses a **branch → pull request → review → merge** workflow.  
Don't directly to `main`. Follow these steps to keep everything clean and conflict-free.

## 1. Clone the repo
Do this once:

```bash
git clone https://github.com/<username>/reponame.git
cd reponame
```

## 2. Create a branch for your work
Always branch off `main`:

```bash
git checkout main
git pull origin main
git checkout -b feature/my-change
```

## 3. Make changes & commit
```bash
# edit files...
git add -A       # This adds all changes in the working directory to the staging area
git commit -m "Describe your change here"
```

## 4. Push your branch to GitHub
```bash
git push -u origin feature/my-change
```

## 5. Open a Pull Request (PR)
- On GitHub, go to the repo.  
- You should see a yellow banner: **“Compare & pull request”** → click it.  
  Or: **Pull requests → New pull request** → base = `main`, compare = your branch.  
- Fill in:
  - **Title**: short, imperative summary  
  - **Description**: what/why you changed  
- Assign reviewers.  
- Click **Create pull request**.

## 6. Review a PR
- Go to **Pull requests** → open the PR.  
- Click **Files changed** to see the diff.  
- Add line comments and submit a **Review**.  
- Choose one:
  - Approve  
  - Request changes  
  - Comment

## 7. Update your PR after feedback
Make edits locally, then push again:

```bash
git add -A
git commit -m "Address review feedback"
git push
```

## 8. Merge the PR
When approved and checks pass:
- Click the green **Merge** button.  
- Use **Squash and merge** (for a clean history).  
- Delete the feature branch when prompted (safe after your commit is live in `main`).

## 9. Keep your local main up to date
```bash
git checkout main
git pull origin main
```

## 10. Sync your feature branch
If `main` has moved ahead:

```bash
git checkout feature/my-change
git merge main   # or: git rebase main
```

## Summary
- Branch off `main`  
- Commit & push to your branch  
- Open a Pull Request  
- Teammates review & approve  
- Merge with squash → delete branch  
- Keep `main` fresh locally  
