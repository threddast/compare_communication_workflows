#!/usr/bin/env python3


# for pipermail archives
import requests
import datetime
from dateutil.rrule import rrule, MONTHLY
import os
from unidecode import unidecode
from tqdm import tqdm


def get_quarter_archive(url, start, end, filename):
    """
    Download the pipermail archive from the given url for the given years.
    """
    if os.path.exists(filename):
        print(f"Skipping {filename} as it already exists.")
        return
    start_date = datetime.datetime.strptime(start, "%Y-%m")
    end_date = datetime.datetime.strptime(end, "%Y-%m")
    years_between = rrule(MONTHLY, dtstart=start_date, until=end_date)
    quarters = ["q1", "q2", "q3", "q4"]
    total_quarters = []
    for year in years_between:
        for quarter in quarters:
            this_quarter = year.strftime("%Y") + quarter + ".txt"
            if this_quarter not in total_quarters:
                total_quarters.append(this_quarter)
    print(total_quarters)

    progress_bar = tqdm(total=len(total_quarters))

    for quarter in total_quarters:
        # print(f"{formatted_month}: {filename}")
        response = requests.get(url + quarter)
        if response.status_code == 200:
            content = unidecode(response.content.decode("latin-1"))
            with open(filename, "ab") as f:
                f.write(content.encode("ascii", "replace"))
        progress_bar.update(1)
    progress_bar.close()


def get_archive(url, start, end, filename, type="pipermail"):
    """
    Download the pipermail archive from the given url for the given years.
    """
    if os.path.exists(filename):
        print(f"Skipping {filename} as it already exists.")
        return
    start_date = datetime.datetime.strptime(start, "%Y-%m")
    end_date = datetime.datetime.strptime(end, "%Y-%m")

    months_between = rrule(MONTHLY, dtstart=start_date, until=end_date)
    total_months = len(list(months_between))
    progress_bar = tqdm(total=total_months)

    for month in months_between:
        if type == "pipermail":
            formatted_month = month.strftime("%Y-%B") + ".txt"
        elif type == "gnu":
            formatted_month = month.strftime("%Y-%m")
        # print(f"{formatted_month}: {filename}")
        response = requests.get(url + formatted_month)
        if response.status_code == 200:
            content = unidecode(response.content.decode("latin-1"))
            with open(filename, "ab") as f:
                f.write(content.encode("ascii", "replace"))
        progress_bar.update(1)
    progress_bar.close()

print("Downloading mailing list archives...")

print("password-store")
get_archive(
    "https://lists.zx2c4.com/pipermail/password-store/",
    "2012-08",
    "2023-07",
    "password-store.mbox",
)
print("buildroot")
get_archive(
    "https://lists.buildroot.org/pipermail/buildroot/",
    "2006-07",
    "2023-07",
    "buildroot.mbox",
)
print("gnupg-devel")
get_archive(
    "https://lists.gnupg.org/pipermail/gnupg-devel/",
    "1997-01",
    "2023-07",
    "gnupg-devel.mbox",
)
print("gnupg-users")
get_archive(
    "https://lists.gnupg.org/pipermail/gnupg-users/",
    "1999-02",
    "2023-07",
    "gnupg-users.mbox",
)

print("nginx-standard")
get_archive(
    "https://mailman.nginx.org/pipermail/nginx/",
    "2005-02",
    "2023-07",
    "nginx-standard.mbox",
)
print("nginx-devel")
get_archive(
    "https://mailman.nginx.org/pipermail/nginx-devel/",
    "2009-10",
    "2023-07",
    "nginx-devel.mbox",
)
print("busybox")
get_archive(
    "http://lists.busybox.net/pipermail/busybox/",
    "2000-06",
    "2023-07",
    "busybox.mbox",
)

get_quarter_archive(
    "http://lists.schmorp.de/pipermail/rxvt-unicode/",
    "2004-01",
    "2023-07",
    "rxvt-unicode.mbox",
)
get_archive(
    "https://lists.gnu.org/archive/mbox/lwip-devel/",
    "2003-07",
    "2023-07",
    "lwip-devel.mbox",
    type="gnu",
)
get_archive(
    "https://lists.gnu.org/archive/mbox/lwip-users/",
    "2002-12",
    "2023-07",
    "lwip-users.mbox",
    type="gnu",
)
