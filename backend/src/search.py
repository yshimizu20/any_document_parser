import sys
import os


class SearchAlgorithm:
    def __init__(self, kw_str, restrictions={}):
        """
        input
        kw_str: str
        restrictions: dict
            startDate, endDate: str
            publishedBy: str
            accessLevel: int (who has access)
            documentType: list (pdf, png, docx etc.)
        """
        self.kw_str = kw_str.lower() # used for raw search
        self.kw_lst = self.kw_str.split() # used for fast search
        self.kw_must_include = [] # index of must_include words
        self.restrictions = restrictions # dict of restrictions e.g. time, published_by

        parsed_lst = self.kw_str.split('"')
        for i in range(1, len(parsed_lst), 2):
            self.kw_must_include.append(parsed_lst[i])

    def search(self):
        result_title = self.search_title()
        result_fast = self.search_fast()
        result_raw = self.search_raw()

    def search_title(self):
        SAMPLE_DIR = "samples/"
        q = [SAMPLE_DIR]
        results = []

        while q:
            d = q.pop()
            currdir, nextdir, filedirs = next(os.walk("d"))
            for dname in nextdir:
                q.append(d + dname)
            for filename in filedirs:
                for kw in self.kw_lst:
                    if kw in ''.join(filename.split('.')[:-1]):
                        score += 1
                results.append((d + filename, score,))

    def search_fast(self):
        pass

    def search_raw(self):
        results = []

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
                results.append(((score_must, score,), filepath,))

        return results # not sorted


if __name__ == "__main__":
    st = "\"Line\" NDA Shimizu"
    print(st.split('"'))

    s = SearchAlgorithm(st)
    s.search()