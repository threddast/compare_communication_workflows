# DATA

- the file all_repos.csv contains all mined data about 176169 repositories
- the file mailing_list_candidates contains the 614 mailing list repositories selected automatically 
- the file manual_check.csv contains the result of the manual filtering process

# CODE

- query.py was used to query github and get the repositories, it is called like `./query.py 0 2012`
- repo-matching.ipynb contains the code to perform the matching of MA repositories to GH ones

Regarding query.py, the output is a file for each day of each year that was queried. 
The first argument is the token group to use. This allows parallelisation using many tokens.
This approach was used to minimise the effect of API errors returned by GitHub.
all-repos.csv is a collection of all mined files into a single one.
The directory `data` contains an example of mined data for some days of 2012
