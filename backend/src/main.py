from search import SearchAlgorithm
import os


if __name__ == "__main__":
    while True:
        target_directory = input("Enter target directory: ")
        if os.path.isdir(target_directory):
            break
        else:
            print("Invalid directory")
    
    s = SearchAlgorithm(target_directory)