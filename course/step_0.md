# Step Zero

## Getting Started

We’re starting this course assuming you already know some programming basics in Python. You should be able to write a “Hello World” app, run it, on top of understanding if/else statements, loops, and functions.

We also assume you have Git installed. (If you’re unsure, check by running `git --version` in your terminal).

I am also writing this course on a device running Ubuntu, so the commands are intended to run on a Linux or Unix (Mac) environment. For Windows users, I recommend using Windows Subsystem for Linux

## Creating a Project Folder

Create a dedicated folder for your project, then switch into it:

''' bash
mkdir python-course
cd python-course
'''

## Verifying Python Is Installed

Make sure you have Python 3.9 or higher. You can check by running:

```bash
python3 --version
```

## Setting Up A Virtual Environment

In this course, we will be using virtual environments. This helps keep a separate space for our project where the version of python that is running and the program's dependencies.

This also helps ensure that installed packages don’t interfere with other projects or the system:

Later in the course we will add and start tracking a `requirements.txt` file. This will also enable portability and let us reproduce the project on a difference machine.

To break down the command, `-m` is telling the `python3` command that we want to the use the `venv` module. The second `venv` is what will be used to name the virtual environment.

My practice is to keep it simple and name it venv.

```bash
python3 -m venv venv
```

### Activating The Virtual Environment

We activate it by running the following command. This creates a copy of the python interpreter and any packages you install that is local to the project.

```bash
source venv/bin/activate
```

We can verify that the virtual environment is active becaues our terminal will prepend the name of the environment in parenthesis. In my local environment, it shows up as `(venv)`

### Verifying You Are Using The Right Python

We can verify which python your terminal session is currently using by running the following command:

```bash
which python
```

If we are using the Python interpreter in the venv, we should the following output:

```bash
/path/to/your/workspace/python-course/venv/bin/python
```

It is the `python-course/venv/bin/python` that we are looking for

### Updating Pip

Pip is the built-in package manager for Python. Pip is what lets us access the servers that host Python's various packages. We can ensure that we are on the latest version by running

```bash
python -m pip install --upgrade pip
```

### Exiting A Virtual Environment

We can exit the virtual environment by either closing the terminal or running the following command:

```bash
deactivate
```

## Setting Up A Git Repo

We will be using git to track changes and each step of this course, first we're going to initialize it in the project.

```bash
git init
```

You now have two options:

1. Copy the `.gitignore`, this is the file that will tell git which files to not track, for example temporary files like our local configuration files or virtual environment.

2. Or if you want to make your own, you can start by running the following command:

```bash
touch .gitignore
```

And add the following the newly created file to ignore the venv, along with the config files for VS Code or Pycharm if you are using either

```gitignore
# Virtual environment
venv/

# Pycharm files
.idea/

# VS Code files
.vscode/
```

We can now add it to our staged changes with the following command:

```bash
git add .gitignore
```

This adds it to the set of current changes that we want to add to our ledger.

## Hello World

`main.py`

```python
print("Hello, World!")
```

Verify it runs:

```bash
python main.py
```

If you see “Hello, World!” on your screen, you’re ready to start building out the project!

## Track It With Git

Before we move onto Step 1, let's `commit` this to `git`.

First we need to add add the new file we made.

```bash
git add main.py
```

Now let's verify we have two files staged to commit.

```bash
git status
```

We should see two files staged, `main.py` and `.gitignore`.

Now let's `commit` it, this means we are adding to the ledger of changes in the project that `git` is keeping track of

```bash
git commit -m "step 0: setting up for a python course"
```

Each commit needs to have a message, in the command we do this by adding a `-m` followed by text in quotes. Ideally this describes the changes you are
adding.

## Save It In The Cloud

I already got to step 5 before remembering to add this. But let's also go through the process of setting setting up a cloud backup for our git repo.

The benefit to using git over storing all of our code in a cloud storage service like onedrive, dropbox, google drive, etc. is that we get granualar change tracking to our code, in additional to being able to create multiple branches of that have different copies of our code. Branching is less relevant to the context of this course.

We are going to be using Github, it's currently the most popular hosted git provider, but if you don't want to use them, you can modify the instructions for alternative like Gitlab, Gitea, or Bitbucket.

If you don't have one already, make an account at [github.com](https://github.com/).

Then we want to open a terminal and follow these instructions

Next, we want to click on our profile icon in the top right corner, and click on *settings*. In the settings menu, we want to click *SSH and GPG keys* under *Access* panel. Here's a [shortcut](https://github.com/settings/keys) if you can't find it.

Now it's on you, Github provides detailed steps for both making an ssh key locally, [steps](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)

Afterwards you can run `cat ~/.ssh/id_ed25519.pub` in the terminal to have it print out your key.

Copy the value, and add it to, go back the the [SSH and GPG keys](https://github.com/settings/keys), and add your key. Remember we are using `ssh` not `gpg`. Keep the key type as is, "Authentication key"

Now make a [new repository](https://github.com/new), I am being lazy and naming mine "python-course", and click "Create repository".

I am assuming you've already initialized git locally and made a commit (if not repeat Step 0).

So now let's get what we have one our computers over to the cloud.

First, run  `git remote add origin git@github.com:<your user name>/<your repo name>.git`

This tells your local git where on the internet to upload (push) your files to.

Next run `git push -u origin main`

This will take what we have commited locally, and push it to the cloud.
