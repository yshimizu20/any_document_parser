import sys
import os
import csv
from datetime import datetime
# from multiprocessing import Pool, Process, Pipe
import bisect


class SearchAlgorithm:
    def __init__(self, kw_str, restrictions={}):
        """
        input
        kw_str: str
        restrictions: dict
            createStartDate, createEndDate: str
            modifyStartDate, modifyEndDate: str
            publishedBy: str
            accessLevel: int (who has access)
            documentType: list (pdf, png, docx etc.)
        """
        self.kw_str = kw_str.lower()  # used for raw search
        self.kw_lst = self.kw_str.replace(
            '"', "").split()  # used for fast search
        self.kw_must_include = []  # index of must_include words
        self.restrictions = restrictions  # dict of restrictions e.g. time, published_by
        self.files = self.filter_files()

        parsed_lst = self.kw_str.split('"')
        for i in range(1, len(parsed_lst), 2):
            self.kw_must_include.append(parsed_lst[i])

    def filter_files(self):
        FILENAME = "samples/filepaths.csv"

        with open(FILENAME, "r") as f:
            files = [line for line in csv.DictReader(f)]

        if "documentType" in self.restrictions:
            files = [file for file in files if file.endswith(
                '.' + self.restrictions["documentType"])]

        if "createStartDate" in self.restrictions:
            dt = datetime.strptime(
                self.restrictions["createStartDate"], "%Y-%m-%d")
            files = [file for file in files if datetime.strptime(
                file["date_cre"], "%Y-%m-%d") >= dt]

        if "createEndDate" in self.restrictions:
            dt = datetime.strptime(
                self.restrictions["createEndDate"], "%Y-%m-%d")
            files = [file for file in files if datetime.strptime(
                file["date_cre"], "%Y-%m-%d") <= dt]

        if "modifyStartDate" in self.restrictions:
            dt = datetime.strptime(
                self.restrictions["modifyStartDate"], "%Y-%m-%d")
            files = [file for file in files if datetime.strptime(
                file["date_mod"], "%Y-%m-%d") >= dt]

        if "modifyEndDate" in self.restrictions:
            dt = datetime.strptime(
                self.restrictions["modifyEndDate"], "%Y-%m-%d")
            files = [file for file in files if datetime.strptime(
                file["date_mod"], "%Y-%m-%d") <= dt]

        return files

    def get_top_search_results(self, results, display_num = 10):
        """
        returns top dispaly_num scores of the results

        input
        results: list of tuples (filepath, score)
        display_start: int
        display_num: int
        """
        
        res = []
        n_res = 0
        min_res = -1

        for result in results:
            if result[1]:
                if n_res == display_num:
                    if result[1] < min_res:
                        continue
                    else:
                        bisect.insort(res, result, key=lambda x: x[1])
                        res.pop()
                        min_res = res[-1][1]
                else:
                    bisect.insort(res, result, key=lambda x: x[1])
                    n_res += 1
                    min_res = res[-1][1]

        return res


    def search(self):
        result_title = self.search_title()
        result_vectors = self.search_vectors()
        result_raw = self.search_raw()

        return result_title, result_vectors, result_raw

    def search_title(self):
        results = []
        count = 0

        for file in self.files:
            score = 0
            for kw in self.kw_lst:
                if kw in file["filepath"]:
                    score += 1
            if score:
                results.append([file["filepath"], score, count])
                count += 1
        
        return results # not sorted

    def search_vectors(self):
        pass

    def search_raw(self):
        results = []
        count = 0

        EXTRACTED_DIR = "samples/extracted/"
        for filepath in os.listdir(EXTRACTED_DIR):
            score_must, score = 0, 0
            with open(EXTRACTED_DIR + filepath, 'r') as f:
                contents = ''.join(f.readlines()).lower()
                print(contents)
            for kw in self.kw_must_include:
                if kw in contents:
                    score_must += 1
            for kw in self.kw_lst:
                if kw in contents:
                    score += 1
            if score_must or score:
                results.append([filepath, (score_must, score,), count])
                count += 1

        return results  # not sorted


if __name__ == "__main__":
    st = "\"Line\" NDA Shimizu"
    print(st.split('"'))

    s = SearchAlgorithm(st)
    s.search_title()
