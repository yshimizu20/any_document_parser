from genericpath import isfile
import os
from datetime import datetime
from time import strptime
import csv


def scrape_title():
    """
    scrapes all files in the samples/ directory
    stores all file info in samples/filepaths.csv
    """
    SAMPLE_DIR = "samples/"
    q = [SAMPLE_DIR]
    titles = []

    while q:
        d = q.pop()
        currdir, nextdir, filedirs = next(os.walk("d"))
        for dname in nextdir:
            q.append(d + dname)
        for filename in filedirs:
            filepath = d + filename
            time_mod = datetime.fromtimestamp(os.path.getmtime(filepath))
            time_cre = datetime.fromtimestamp(os.path.getctime(filepath))
            parsed_lst = filepath.split(".")
            if len(parsed_lst) == 1:
                doctype = ""
            else:
                doctype = parsed_lst[-1]
            
            titles.append({
                "filepath": filepath,
                "time_mod": datetime.strftime(time_mod, "%Y-%m-%d"),
                "time_cre": datetime.strftime(time_cre, "%Y-%m-%d"),
                "doctype": doctype,
                "scraped_extracted": "",
                "scraped_plain": ""
            })

        field_names = ["filepath", "time_mod",
                       "time_cre", "doctype", "scraped_extracted", "scraped_raw"]
        with open("samples/filepaths.csv", "w") as f:
            writer = csv.DictWriter(f, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(titles)

    return titles


def update_filepaths(event):
    pass


if __name__ == "__main__":
    for filepath in os.listdir("."):
        if os.path.isfile(filepath):
            time_mod = datetime.fromtimestamp(os.path.getmtime(filepath))
            time_cre = datetime.fromtimestamp(os.path.getctime(filepath))
            print(time_mod, type(time_mod))
            print(datetime.strftime(time_mod, "%Y-%m-%d"))
