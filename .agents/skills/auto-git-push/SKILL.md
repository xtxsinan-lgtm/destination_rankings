---
name: auto-git-push
description: >-
  Automatically stage, commit, and push all workspace changes to the remote Git
  repository after completing any code, data, or documentation task. Always invoke
  and follow this skill at the end of every file-modifying task so changes are
  immediately pushed to GitHub.
---

# Auto Git Commit & Push (`auto-git-push`)

Whenever you complete any task that creates, edits, or updates files in the repository, you **MUST** stage, commit, and push the changes to the remote repository (`origin`) before finishing your response.

## Steps

1. **Verify SEO & Data Integrity (if HTML/JS data changed)**:
   If any ranking dataset (`data*.js`) or HTML page (`*.html`) was modified in `destination_rankings`, run:
   ```bash
   python3 tools/build_seo.py
   ```
2. **Check Git Status**:
   Run `git status -s` to inspect modified and untracked files.
3. **Stage, Commit, and Push**:
   Run the helper script [push.sh](./scripts/push.sh) with a descriptive commit message, or execute directly:
   ```bash
   git add -A && git commit -m "<concise summary of changes>" && git push origin HEAD
   ```
4. **Verify Push**:
   Confirm that `git status -sb` shows the branch is up to date with `origin/main` (or the current remote tracking branch) and report the commit hash in your final response.
