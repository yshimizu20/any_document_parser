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
    SAMPLE_DIR = "samples"
    q = [SAMPLE_DIR]
    titles = []

    while q:
        d = q.pop()
        currdir, nextdir, filedirs = next(os.walk(d))
        for dname in nextdir:
            q.append(d + '/' + dname)
        for filename in filedirs:
            filepath = d + '/' + filename
            date_mod = datetime.fromtimestamp(os.path.getmtime(filepath))
            date_cre = datetime.fromtimestamp(os.path.getctime(filepath))
            parsed_lst = filepath.split(".")
            if len(parsed_lst) == 1:
                doctype = ""
            else:
                doctype = parsed_lst[-1]
            
            titles.append({
                "filepath": filepath,
                "date_mod": datetime.strftime(date_mod, "%Y-%m-%d"),
                "date_cre": datetime.strftime(date_cre, "%Y-%m-%d"),
                "doctype": doctype,
                "scraped_extracted": "",
                "scraped_plain": ""
            })
        print(titles)

        field_names = ["filepath", "date_mod",
                       "date_cre", "doctype", "scraped_extracted", "scraped_plain"]
        with open("samples/filepaths.csv", "w+") as f:
            writer = csv.DictWriter(f, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(titles)

    return titles


def update_filepaths(event):
    pass


if __name__ == "__main__":
    scrape_title()
