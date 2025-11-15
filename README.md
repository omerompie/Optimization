# Team Python Project: Git & PyCharm Setup Guide

Welcome to the team! This guide has everything you need to get set up and start coding with us.

Please follow these steps in order, and you'll be set up perfectly in about 10-15 minutes.

> **Note:** This guide includes instructions for both **Windows** and **macOS**. Follow the section that matches your operating system.

---

## Part 1: One-Time Setup (Do This Now)

You only need to do this part once on your computer.

### 1.1: Clean Out Old SSH Keys (Very Important!)

This step prevents the "Permission Denied" error that is very common. We will make sure you only have one, new key.

#### Windows:

1. Open your PowerShell terminal (just from the Start Menu is fine).

2. Run this command to see if you have any old keys:

```powershell
ls C:\Users\<YOUR-USERNAME>\.ssh
```

(Replace `<YOUR-USERNAME>` with your actual username, e.g., `C:\Users\Klaas\.ssh`)

3. If you see old key files named `id_rsa` or `id_rsa.pub`, delete them. This is what causes most problems.

```powershell
# Run these commands if you see the old 'rsa' files
rm C:\Users\<YOUR-USERNAME>\.ssh\id_rsa
rm C:\Users\<YOUR-USERNAME>\.ssh\id_rsa.pub
```

#### macOS:

1. Open your Terminal application (find it in Applications > Utilities, or press `Cmd + Space` and type "Terminal").

2. Run this command to see if you have any old keys:

```bash
ls ~/.ssh
```

3. If you see old key files named `id_rsa` or `id_rsa.pub`, delete them. This is what causes most problems.

```bash
# Run these commands if you see the old 'rsa' files
rm ~/.ssh/id_rsa
rm ~/.ssh/id_rsa.pub
```

### 1.2: Configure Git's "Signature"

Git needs to "sign" every commit you make with your name and email.

#### Windows:

In the same PowerShell terminal, run these two commands. Use your real name and the email you used for your GitHub account.

```powershell
git config --global user.name "Your Name"
```

```powershell
git config --global user.email "youremail@example.com"
```

#### macOS:

In the same Terminal, run these two commands. Use your real name and the email you used for your GitHub account.

```bash
git config --global user.name "Your Name"
```

```bash
git config --global user.email "youremail@example.com"
```

### 1.3: Create Your New SSH Key

This is the secure "password" for your computer to talk to GitHub.

#### Windows:

1. Run this command in your PowerShell terminal. Use your GitHub email.

```powershell
ssh-keygen -t ed25519 -C "youremail@example.com"
```

2. It will ask you where to save the key. Just press **Enter** to accept the default.
3. It will ask you to `Enter passphrase`. Press **Enter** again (leave it empty).
4. It will ask you to `Enter same passphrase again`. Press **Enter** one more time.

You've now created a new, secure key!

#### macOS:

1. Run this command in your Terminal. Use your GitHub email.

```bash
ssh-keygen -t ed25519 -C "youremail@example.com"
```

2. It will ask you where to save the key. Just press **Enter** to accept the default.
3. It will ask you to `Enter passphrase`. Press **Enter** again (leave it empty).
4. It will ask you to `Enter same passphrase again`. Press **Enter** one more time.

You've now created a new, secure key!

### 1.4: Add Your Key to GitHub

Now, we copy the public part of that key to the GitHub website.

#### Windows:

1. Run this command to display your new public key in the terminal.

```powershell
cat C:\Users\<YOUR-USERNAME>\.ssh\id_ed25519.pub
```

(Again, replace `<YOUR-USERNAME>`)

2. It will print a long string starting with `ssh-ed25519...`.

3. Carefully highlight and copy this entire string. (from `ssh-ed25519` all the way to your email at the end).

#### macOS:

1. Run this command to display your new public key in the terminal.

```bash
cat ~/.ssh/id_ed25519.pub
```

2. It will print a long string starting with `ssh-ed25519...`.

3. Carefully highlight and copy this entire string. (from `ssh-ed25519` all the way to your email at the end).

#### Both Platforms:

4. Go to [github.com]([https://github.com](https://github.com/settings/keys)) and log in.

5. Click your profile picture (top-right) and go to **Settings**.

6. On the left menu, click **SSH and GPG keys**.

7. Click the green **New SSH key** button.

8. Give it a **Title** (e.g., "My PyCharm Laptop").

9. Paste your copied key into the big "Key" box.

10. Click **Add SSH key**.

### 1.5: Start the SSH Service

#### Windows (Admin Step):

This requires Administrator permission.

1. Go to your Start Menu.

2. Type "PowerShell".

3. Right-click on "Windows PowerShell" and select **"Run as administrator"**.

4. Click "Yes" on the security prompt.

5. In the new Administrator terminal (it will say `C:\Windows\system32>`), run these two commands. They ensure the service is running.

```powershell
# This command sets the service to "Manual" so you can start it
Set-Service -Name ssh-agent -StartupType Manual
```

```powershell
# This command starts the service
Start-Service ssh-agent
```

#### macOS:

The SSH agent runs automatically on macOS, so you can skip this step!

### 1.6: Add Your Key to the SSH Agent

Now, let's load your new key into the agent so your computer can use it.

#### Windows:

In the same Administrator terminal, run this command:
(Use the full path to your key)

```powershell
ssh-add C:\Users\<YOUR-USERNAME>\.ssh\id_ed25519
```

You must see the message: `Identity added...`

#### macOS:

In your Terminal, run this command:

```bash
ssh-add ~/.ssh/id_ed25519
```

You must see the message: `Identity added...`

**Note:** On macOS, you may want to add the key to your keychain so it persists across reboots:

```bash
ssh-add --apple-use-keychain ~/.ssh/id_ed25519
```

### 1.7: Test Your Connection!

This is the final test. If this works, you are all set.

#### Windows:

In the same Administrator terminal, run this:

```powershell
ssh -T git@github.com
```

#### macOS:

In your Terminal, run this:

```bash
ssh -T git@github.com
```

#### Both Platforms:

- You might see a warning: `Are you sure you want to continue connecting (yes/no/[fingerprint])?`.
- Type `yes` and press **Enter**.

You should see the welcome message: `Hi <your-username>! You've successfully authenticated...`

**Success!** You can now close the terminal. You are finished with the one-time setup.

---

## Part 2: Getting the Project (Cloning)

Now you'll download the project so PyCharm can see it.

### Create Your Project Folder

#### Windows:

In Windows Explorer, go to your user folder (`C:\Users\<YOUR-USERNAME>`) and create a new folder called `PyCharmProjects`. This is a clean place to keep all your work.

#### macOS:

In Finder, go to your home folder (you can press `Cmd + Shift + H`) and create a new folder called `PyCharmProjects`. This is a clean place to keep all your work.

### Open Terminal in Your Folder

#### Windows:

1. Open the new `PyCharmProjects` folder.
2. In the address bar at the top, type `powershell` and press **Enter**.
3. This will open a normal PowerShell terminal inside that folder.

#### macOS:

1. Open the new `PyCharmProjects` folder in Finder.
2. Right-click (or Control-click) on the folder and select **Services > New Terminal at Folder** (or you can drag the folder icon to the Terminal icon in your Dock).
3. Alternatively, open Terminal and type `cd ~/PyCharmProjects` and press **Enter**.

### Clone the Repo

#### Both Platforms:

1. On our GitHub repo page, click the green **< > Code** button.
2. Click the **SSH** tab.
3. Copy the URL (it looks like `git@github.com:Klaasompie/Optimization.git`).
4. In your terminal, run `git clone` with that URL:

**Windows:**
```powershell
git clone git@github.com:Klaasompie/Optimization.git
```

**macOS:**
```bash
git clone git@github.com:Klaasompie/Optimization.git
```

This will create a new folder `Optimization` containing all our project files.

### Open in PyCharm

#### Windows:

1. Open PyCharm.
2. Click **File > Open**.
3. Navigate to `C:\Users\<YOUR-USERNAME>\PyCharmProjects` and select the `Optimization` folder.
4. Click **OK**. PyCharm will open the project, and it's already connected to Git!

#### macOS:

1. Open PyCharm.
2. Click **File > Open**.
3. Navigate to your home folder > `PyCharmProjects` and select the `Optimization` folder.
4. Click **Open**. PyCharm will open the project, and it's already connected to Git!

---

## Part 3: Our Daily Workflow (How to Make Changes)

**Rule #1: You cannot push to main. You must follow these steps. This protects our project.**

### Step 3.1: ALWAYS Get Updates

Before you start any new work, get the latest code from the main branch.

You can do this in the PyCharm terminal (the "Terminal" tab at the bottom).

```bash
git checkout main
```

```bash
git pull origin main
```

(This ensures you are building on the team's most recent work.)

### Step 3.2: Create Your Own Branch

Now, create a new branch for your feature. Give it a descriptive name.

```bash
git checkout -b "feature/your-task-name"
```

**Example:** `git checkout -b "feature/user-login-page"`

**Example:** `git checkout -b "fix/main-menu-bug"`

### Step 3.3: Do Your Work

This is the fun part. Write your Python code, add files, and save them in PyCharm.

### Step 3.4: Save (Commit) Your Changes

When you've finished your task (or a good piece of it), you need to "commit" your work.

1. Add all your changed files:

```bash
git add .
```

(The `.` means "all files in this folder.")

2. Commit them with a clear message:

```bash
git commit -m "Added login form and button"
```

### Step 3.5: Push Your Branch to GitHub

The first time you push a new branch, you must use this special command:

```bash
git push -u origin "feature/your-task-name"
```

(Replace `feature/your-task-name` with your actual branch name. The `-u` links your local branch to a new branch on GitHub.)

After that one time, any other commits you make on this same branch can be pushed with just:

```bash
git push
```

### Step 3.6: Open a Pull Request (PR)

1. Go to our repo on GitHub.
2. You will see a yellow bar with your branch name. Click the **"Compare & pull request"** button.
3. Give it a title, write a short description of what you did.
4. On the right, click **"Reviewers"** and add one (or all) of us.
5. Click **"Create pull request"**.

We will then review your code, approve it, and merge it into main.

---

## Part 4: Handy Git Commands Reference

### Quick Command List

```bash
# Check status and info
git status                          # See what files you've changed
git branch                          # See what branch you're on (has *)
git log --oneline                   # See recent commits (press 'q' to exit)
git diff filename.py                # See what changed in a file

# Daily workflow
git add .                           # Stage all changes
git commit -m "Your message"        # Commit your changes
git push                            # Push to GitHub
git pull origin main                # Get latest from main

# Branch management
git checkout -b "feature/name"      # Create new branch
git checkout branch-name            # Switch branches
git branch -d branch-name           # Delete local branch (after merged)

# Undo commands (be careful!)
git checkout -- filename.py         # ⚠️ Discard changes in one file
git reset HEAD filename.py          # Unstage a file (undo git add)
git reset --soft HEAD~1             # Undo last commit, keep your changes
git reset --hard HEAD~1             # ⚠️ Undo last commit, DELETE changes
git reset --hard                    # ⚠️ Delete ALL uncommitted changes
```

### Understanding Reset Options

- **`--soft`**: Undo the commit but keep your changes staged (ready to commit again). Use when you want to re-do a commit or fix the commit message.
- **`--hard`**: Undo the commit AND delete all changes permanently. Use when you want to completely start over from the last commit.

### Emergency: "I Made a Mess!"

**You committed to main by accident:**
```bash
git branch feature/my-backup        # Save your work
git reset --hard origin/main        # Reset main to match GitHub
git checkout feature/my-backup      # Switch to your backup branch
```

**You have merge conflicts:**
1. Open the conflicting files in PyCharm
2. Look for sections marked with `<<<<<<<`, `=======`, and `>>>>>>>`
3. Edit the file to keep what you want and remove the conflict markers
4. Save the file, then run:
```bash
git add .
git commit -m "Resolved merge conflicts"
```

**Remember:** Git is very forgiving. Almost anything can be undone. Don't be afraid to experiment on your branch!
