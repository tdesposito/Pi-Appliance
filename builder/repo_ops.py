import datetime
from pathlib import Path
from urllib.parse import urlparse

import boto3

from . import *

def commit_repo(term):
    prep_screen(term, "Commit Updates To Repository")
    if not get_uncommitted():
        return press_any_key(term, f"\n{term.bright_yellow}Nothing To Commit.")

    with term.location():
        echo(f"{term.bright_blue}Commit Message (blank to abort): {term.bright_white}")
        message = input()
    if not message:
        return
    print("\n\n")

    try:
        try_command("git add -A", "Error staging files")
        try_command("git commit -m", "Error committing", params=f"'{message}'")
        try_command(f"git tag {datetime.datetime.now().strftime('APL-%Y%m%d-%H%M')}", "Error tagging commit")
        try_command("git push", "Error pushing to remote")
        try_command("git push --tags", "Error pushing tags")
    except Exception as e:
        press_any_key(f"{term.bright_red}{e}{term.white}")
    else:
        press_any_key(term, f"{term.bright_blue}Done.{term.white}")


def get_uncommitted(get_new=True, get_mod=True):
    uncomm = []
    if get_new:
        uncomm.extend(str(runcmd("git ls-files -o --exclude-standard").stdout, 'utf-8').split("\n"))
    if get_mod:
        uncomm.extend(str(runcmd("git ls-files -m --exclude-standard").stdout, 'utf-8').split("\n"))
    return [e for e in uncomm if e]


def init_repo(term):
    prep_screen(term, "Initialize Repository")

    print(f"\n{term.bright_blue}Remote Repository Name (blank to abort): {term.bright_white}")
    repo = input()
    if not repo:
        return

    if not Path('./.git').is_dir():
        p = runcmd(f"git init")
        if p.returncode:
            return press_any_key(term, f"\n{term.bright_red}Error initializing repo:{term.white}\n{p.stdout}")

    git = boto3.client('codecommit')
    try:
        echo("Creating Repository...")
        rsp = git.create_repository(
            repositoryName=repo,
            repositoryDescription=f'''Code for your Pi-Appliance.'''
        )
        if rsp.get('ResponseMetadata',{}).get('HTTPStatusCode') != 200:
            return press_any_key(term, f"\n{term.bright_red}Error creating remote (bad response).{term.white}")
        echo("Done.\nSaving Secrets...")
        repourl = urlparse(rsp['repositoryMetadata']['cloneUrlHttp'])
        secrets = load_secrets()
        secrets['repo_host'] = repourl.hostname
        secrets['repo_url'] = f"{repourl.hostname}{repourl.path}"
        print("Done.")
        save_secrets(secrets)
    except Exception as e:
        return press_any_key(term, f"\n{term.bright_red}Error creating remote:{term.white}\n{e}\n")

    try:
        try_command(f"git remote add origin codecommit::us-east-1://default@{repo}", "Error adding remote")
        try_command("git add .gitignore", "Error adding for initial commit")
        try_command("git commit -m", "Error creating initial commit", params="'init repository'")
        try_command("git push --set-upstream origin main", "Error setting upstream")
    except Exception as e:
        press_any_key(f"{term.bright_red}{e}{term.white}")
    else:
        press_any_key(term, f"\n{term.bright_green}Repository and Remote initialized.{term.white}")
