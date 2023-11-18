#!/usr/bin/env python3

from github import Github
import pandas as pd
import datetime
import calendar
import random
import time
import sys

tokens = [

    [
        # your token here
    ],

]

token_group = sys.argv[1]
tokens = tokens[int(token_group)]
githubs = []
for tok in tokens:
    githubs.append(Github(tok))

for g in githubs:
    core_rate_limit = g.get_rate_limit().core
    print(core_rate_limit)

year = sys.argv[2]
if len(sys.argv) > 3:
    startdate = sys.argv[3]
else:
    startdate = year + "-1-1"
if len(sys.argv) > 4:
    enddate = sys.argv[4]
else:
    enddate = year + "-12-31"

if len(sys.argv) > 5:
    token_num = int(sys.argv[5])
else:
    token_num = random.randint(0, len(githubs) - 1)



dates = pd.to_datetime(pd.date_range(start=startdate, end=enddate, freq="D"))
g = githubs[token_num]
for day in dates:

    reposarr = []
    query = "stars:>199 fork:true created:" + day.strftime("%Y-%m-%d")

    repos = g.search_repositories(query=query)
    error = True
    while error:
        try:
            now = datetime.datetime.utcnow()
            print(now)
            print(g.get_rate_limit())
            print(query)
            i = 1
            for repo in repos:
                repodata = []
                repodata.append(repo.full_name)
                repodata.append(repo.description)
                repodata.append(repo.fork)
                repodata.append(repo.forks_count)
                repodata.append(repo.homepage)
                repodata.append(repo.id)
                repodata.append(repo.language)
                repodata.append(repo.mirror_url)
                repodata.append(repo.network_count)
                repodata.append(repo.open_issues_count)
                repodata.append(repo.pushed_at)
                repodata.append(repo.source)
                repodata.append(repo.stargazers_count)
                repodata.append(repo.subscribers_count)
                repodata.append(repo.topics)
                repodata.append(repo.watchers_count)

                try:
                    repodata.append(repo.get_commits().totalCount)
                except Exception as e:
                    print(str(e))  # this error is there for empty repos
                    continue
                repodata.append(repo.get_issues(state="all").totalCount)
                try:
                    repodata.append(repo.get_contributors(anon="true").totalCount)
                except Exception as e:
                    print(str(e))
                    repodata.append(-42)

                repodata.append(str(repo.get_languages()))

                reposarr.append(repodata)
                print(str(i), end=" ", flush=True)
                i = i + 1
            print()
            error = False
        except Exception as e:
            print(str(e))
            error = True
            if g.get_rate_limit().core.remaining < 10:
                time_reset = datetime.datetime.strptime(
                    str(g.get_rate_limit().core.reset), "%Y-%m-%d %H:%M:%S"
                )
                print("\nWill reset at: " + str(time_reset))
                now = datetime.datetime.utcnow()
                print("Sleeping now for " + str(time_reset - now))
                time_ctr = 1
                while now < time_reset:
                    print(str(time_ctr), end=" ", flush=True)
                    time_ctr += 1
                    time.sleep(60)
                    now = datetime.datetime.utcnow()
                print("\nResuming at " + str(now))
                reposarr = []

    with open("data/" + year + "/" + day.strftime("%Y-%m-%d"), "w") as f:
        for repo in reposarr:
            f.write(str(repo))
            f.write("\n")
    f.closed
