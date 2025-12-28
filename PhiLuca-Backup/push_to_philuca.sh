#!/usr/bin/env python3
import os
import subprocess

def run_command(cmd):
    try:
        print(f"Executing: {cmd}")
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

# 1. Initialize Git if not present
if not os.path.exists(".git"):
    run_command("git init")

# 2. Configure Identity (Using your ORCID/Marco info)
run_command('git config --global user.name "the-adjacent-possibilities"')
run_command('git config --global user.email "adjacent.possibilities.dot.com@gmail.com"') # Replace with your actual email

# 3. Add Remote (PhiLuca-Core)
run_command("git remote add origin https://github.com/the-adjacent-possibilities/PhiLuca-Core.git")

# 4. Filter for 'Honest' files (Avoiding massive junk/logs if necessary)
# We add everything for now to ensure your research is safe.
run_command("git add .")

# 5. The First Global Commit
commit_msg = "DSS Phase 1: Initializing Phinary Substrate - Executed 2025-12-09"
run_command(f'git commit -m "{commit_msg}"')

# 6. Push to Main
# Note: You will be prompted for your GitHub Username and PAT (Personal Access Token)
run_command("git branch -M main")
run_command("git push -u origin main")

print("\n--- Manifold Unfolded: Termux Synced to PhiLuca-Core ---")
