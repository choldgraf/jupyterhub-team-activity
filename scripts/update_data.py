import pandas as pd
from watchtower import comments_, issues_, commits_, reviews_
from tqdm import tqdm
import os
import numpy as np
from datetime import timedelta
import argparse

auth = 'GITHUB_API_TOKEN'
auth = os.environ[auth]

########################################################
# Helper functions to iteratively update
def find_last_date(dates):
    last_date = np.max(dates)
    # Two day overlap
    from_date = last_date - timedelta(days=2)
    return from_date

def update_from_latest(org, repo, kind, from_date="2016-01-01"):
    if kind == "comments":
        # Current data we've got
        current_comments = comments_.load_comments(org, repo)
        # Find last day of data
        if current_comments is not None:
            from_date = find_last_date(current_comments['created_at'])
        # Update since that day
        comments_.update_comments(org, repo, auth=auth, since=from_date)

    elif kind == "issues":
        current_issues = issues_.load_issues(org, repo)
        # Find last day of data
        if current_issues is not None:
            from_date = find_last_date(current_issues['created_at'])
        issues_.update_issues(org, repo, auth=auth, since=from_date)

    elif kind == "commits":
        current_commits = commits_.load_commits(org, repo)
        # Find last day of data
        if current_commits is not None:
            from_date = find_last_date(current_commits['date'])
        # Auth is different for commits
        commits_.update_commits(org, repo, auth=auth, since=from_date)
    print("Updated {}/{}: {} after date {}".format(org, repo, kind, from_date))

########################################################
# Update the data

START_DATE ="2016-01-01"

parser = argparse.ArgumentParser(description='Update data for a repository.')
parser.add_argument('org')
parser.add_argument('repo')
parser.add_argument('--date', default=None)

args = parser.parse_args()

start_date = args.date if args.date is not None else "2016-01-01"
for kind in ['comments', 'issues', 'commits']:
    update_from_latest(args.org, args.repo, kind, from_date=start_date)