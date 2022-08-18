import MeCab
from pathlib import Path
import numpy as np
import pandas as pd


# Paths
dictionary_path = "backend/src/samples/dictionary.txt"
document_metadata_path = "backend/src/samples/extracted.csv"
document_metadata_columns = ["tokens", "doc_name"]

class Text_Extractor():
    """
    Converts sentence to vector and searches.
    """    
    def __init__(self):
        """
        Constructor to load tagger and dictionary.
        """
        self.tagger = MeCab.Tagger("-Owakati")
        self.dictionary_file = open(dictionary_path, "a+")
        self.dictionary = self.dictionary_file.read().splitlines()
        self.db_columns = document_metadata_columns
        
        if not Path(document_metadata_path).is_file():
            self.document_db = pd.DataFrame(columns=document_metadata_columns)
        else:
            self.document_db = pd.read_csv(document_metadata_path)
        
    def document_tokenizer(self,
                           document,
                           document_name):
        """
        Tokenizes document and constructs vector representation, and saves to 
        database of documents.
        For indexing purposes.
        
        Current implementation is naive.
        INPUTS:     document (String)
        OUTPUTS:    
        """
        self.tagger.parse() 
        node = self.tagger.parseToNode(sentence)
        tokens = []
        while node:
            pos = node.feature.split(",")[0]
            if pos in ["名詞", "動詞", "形容詞"]:
                word = node.surface
                tokens.append(word)
            node = node.next
        
        token_vector = [0] * len(self.dictionary)
        updated_dictionary = False
        
        for token in tokens:
            if token not in self.dictionary:
                self.dictionary.append(token)
                token_vector.append(1)
            else:
                token_vector[self.dictionary.index(token)] += 1
        
        # Make sure new dictionary is saved
        self.dictionary_file.write(self.dictionary)
        
        # Add document token metadata 
        entry = pd.DataFrame({self.db_columns[0]: np.array(token_vector),
                              self.db_columns[1] : document_name})

        self.document_db = pd.concat([self.document_db, 
                                      entry], 
                                     ignore_index = True, 
                                     axis = 0)
        
        # If dictionary size changes, append zeros to other documents
        #! Very time consuming with current code
        if updated_dictionary:
            for index, row in self.document_db.iterrows():
                if len(row[self.db_columns[0]]) != len(self.dictionary):
                    self.document_db.at[index, self.db_columns[0]].extend([0] * (len(self.dictionary) - len(row[self.db_columns[0]])))
                    
        # Save documents to database
        self.document_db.to_csv(document_metadata_path, 
                                index=False)

    def query_tokenizer(self, 
                        sentence):
        """
        Tokenizes sentence and constructs vector representation. 
        For searching purposes.
        
        Current implementation is naive.
        INPUTS:     sentence (String)
        OUTPUTS:    token_vector (List of int)
        """
        tokens = tagger.parse(sentence).split()
        token_vector = [0] * len(self.dictionary)
        
        for token in tokens:
            if token in self.dictionary:
                token_vector[self.dictionary.index(token)] += 1
        
        return np.array(token_vector)
    
if __name__ == "__main__":
    model = Text_Extractor()
    print(model.db_columns)