import glob
import regex as re
import pandas as pd

list_of_txts = []

for file in glob.glob("Attraction Pictures/*"):
    if file.endswith('.txt'):
        print(file)
        file = re.search("(?<=Attraction Pictures/)(.*)(?=.txt)",file).group()
        list_of_txts.append(file)

series_of_texts = pd.Series(list_of_txts)
series_of_texts.to_csv('listOfUndownloadedImages.csv')