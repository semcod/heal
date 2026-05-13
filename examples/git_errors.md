# Git Error Examples

Real-world Git errors and how `heal` helps fix them.

### Error
```bash
$ git merge feature-branch
Auto-merging src/app.js
CONFLICT (content): Merge conflict in src/app.js
Automatic merge failed; fix conflicts and then commit the result.
```

### Using heal
```bash
$ git merge feature-branch 2>&1 | heal
```

### Expected Solution
```
Git encountered conflicts while merging that need manual resolution.

**Solution:**

1. View conflicted files:
   ```bash
   git status
   ```

2. Open the conflicted file and look for conflict markers:
   ```
   <<<<<<< HEAD
   your changes
   =======
   their changes
   >>>>>>> feature-branch
   ```

3. Resolve conflicts manually, then:
   ```bash
   git add src/app.js
   git commit -m "Merge feature-branch, resolved conflicts"
   ```

4. Or abort the merge:
   ```bash
   git merge --abort
   ```

5. Use a merge tool:
   ```bash
   git mergetool
   ```
```

### Error
```bash
$ git push origin main
To github.com:user/repo.git
 ! [rejected]        main -> main (non-fast-forward)
error: failed to push some refs to 'github.com:user/repo.git'
hint: Updates were rejected because the tip of your current branch is behind
```

### Using heal
```bash
$ git push origin main 2>&1 | heal
```

### Expected Solution
```
Your local branch is behind the remote branch. Someone else pushed changes.

**Solution:**

1. **Recommended**: Pull and merge first:
   ```bash
   git pull origin main
   # Resolve any conflicts if they occur
   git push origin main
   ```

2. Pull with rebase (cleaner history):
   ```bash
   git pull --rebase origin main
   git push origin main
   ```

3. Force push (DANGEROUS - only if you're sure):
   ```bash
   git push --force origin main
   # or safer:
   git push --force-with-lease origin main
   ```

4. Check what's different:
   ```bash
   git fetch origin
   git log HEAD..origin/main
   ```
```

### Error
```bash
$ git push origin main
remote: Support for password authentication was removed on August 13, 2021.
remote: Please use a personal access token instead.
fatal: Authentication failed for 'https://github.com/user/repo.git/'
```

### Using heal
```bash
$ git push origin main 2>&1 | heal
```

### Expected Solution
```
GitHub no longer accepts password authentication. You need a Personal Access Token (PAT).

**Solution:**

1. Create a Personal Access Token on GitHub:
   - Go to Settings → Developer settings → Personal access tokens
   - Generate new token with 'repo' scope
   - Copy the token

2. Use the token as password when prompted, or configure it:
   ```bash
   git remote set-url origin https://YOUR_TOKEN@github.com/user/repo.git
   ```

3. **Better**: Use SSH instead:
   ```bash
   # Generate SSH key if you don't have one
   ssh-keygen -t ed25519 -C "your_email@example.com"
   
   # Add to GitHub: Settings → SSH and GPG keys
   cat ~/.ssh/id_ed25519.pub
   
   # Change remote to SSH
   git remote set-url origin git@github.com:user/repo.git
   ```

4. Use Git Credential Manager:
   ```bash
   git config --global credential.helper store
   ```
```

### Error
```bash
$ git checkout abc123
Note: switching to 'abc123'.
You are in 'detached HEAD' state...
```

### Using heal
```bash
$ git status 2>&1 | heal
```

### Expected Solution
```
You're in detached HEAD state - not on any branch.

**Solution:**

1. If you want to keep changes, create a new branch:
   ```bash
   git checkout -b new-branch-name
   ```

2. Return to a branch without keeping changes:
   ```bash
   git checkout main
   ```

3. If you made commits in detached HEAD:
   ```bash
   # Note the commit hash
   git log
   
   # Switch to a branch
   git checkout main
   
   # Cherry-pick your commits
   git cherry-pick <commit-hash>
   ```

4. Or merge the detached HEAD commits:
   ```bash
   git branch temp-branch
   git checkout main
   git merge temp-branch
   ```
```

### Error
```bash
$ git pull origin main
error: Your local changes to the following files would be overwritten by merge:
        src/config.js
Please commit your changes or stash them before you merge.
Aborting
```

### Using heal
```bash
$ git pull origin main 2>&1 | heal
```

### Expected Solution
```
You have uncommitted changes that conflict with incoming changes.

**Solution (choose one):**

1. Stash your changes temporarily:
   ```bash
   git stash
   git pull origin main
   git stash pop
   ```

2. Commit your changes first:
   ```bash
   git add .
   git commit -m "WIP: save current work"
   git pull origin main
   ```

3. Discard your local changes (careful!):
   ```bash
   git checkout -- src/config.js
   git pull origin main
   ```

4. Pull with rebase and autostash:
   ```bash
   git pull --rebase --autostash origin main
   ```
```

### Error
```bash
$ git push origin main
remote: error: GH001: Large files detected. You may want to try Git Large File Storage
remote: error: File large-file.zip is 150.00 MB; this exceeds GitHub's file size limit of 100.00 MB
```

### Using heal
```bash
$ git push origin main 2>&1 | heal
```

### Expected Solution
```
You're trying to push a file larger than GitHub's 100MB limit.

**Solution:**

1. Remove the file from Git history:
   ```bash
   git rm --cached large-file.zip
   git commit --amend -m "Remove large file"
   git push origin main
   ```

2. Use Git LFS for large files:
   ```bash
   # Install Git LFS
   git lfs install
   
   # Track large files
   git lfs track "*.zip"
   git add .gitattributes
   git add large-file.zip
   git commit -m "Add large file with LFS"
   git push origin main
   ```

3. Add to .gitignore if it shouldn't be tracked:
   ```bash
   echo "large-file.zip" >> .gitignore
   git rm --cached large-file.zip
   git commit -m "Remove large file from tracking"
   ```

4. If already in history, use BFG Repo-Cleaner:
   ```bash
   bfg --delete-files large-file.zip
   git reflog expire --expire=now --all
   git gc --prune=now --aggressive
   ```
```

### Error
```bash
$ git rebase main
CONFLICT (content): Merge conflict in src/app.js
error: could not apply abc123... Add new feature
Resolve all conflicts manually, mark them as resolved with
"git add/rm <conflicted_files>", then run "git rebase --continue".
```

### Using heal
```bash
$ git rebase main 2>&1 | heal
```

### Expected Solution
```
Git encountered conflicts during rebase that need manual resolution.

**Solution:**

1. View conflicted files:
   ```bash
   git status
   ```

2. Resolve conflicts in the files, then:
   ```bash
   git add src/app.js
   git rebase --continue
   ```

3. Skip the problematic commit:
   ```bash
   git rebase --skip
   ```

4. Abort the rebase:
   ```bash
   git rebase --abort
   ```

5. Use a merge tool:
   ```bash
   git mergetool
   git rebase --continue
   ```
```

### Error
```bash
$ git checkout -b feature-branch
fatal: A branch named 'feature-branch' already exists.
```

### Using heal
```bash
$ git checkout -b feature-branch 2>&1 | heal
```

### Expected Solution
```
A branch with that name already exists locally.

**Solution:**

1. Switch to the existing branch:
   ```bash
   git checkout feature-branch
   ```

2. Delete the old branch and create new:
   ```bash
   git branch -D feature-branch
   git checkout -b feature-branch
   ```

3. Create a branch with a different name:
   ```bash
   git checkout -b feature-branch-v2
   ```

4. Check all branches:
   ```bash
   git branch -a
   ```
```
