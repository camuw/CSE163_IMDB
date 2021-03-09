from bs4 import BeautifulSoup
from requests import get
from imdb import IMDb
import imdb
import pandas as pd
from get_csv import GetCSV
from graphs import Graphs

user_input = False

def main():
    reader = GetCSV()
    if input("Do you want to input TV shows? Y or N : ") == "Y":
        string1 = input("Enter 1st TV show: ")
        string2 = input("Enter 2nd TV show: ")
    else:
        string1 = "Family Guy"
        string2 = "American Dad"
    tt_string1 = reader.get_ttcode(string1)
    season_length1 = reader.get_season_length(tt_string1)
    data1 = reader.get_csv(tt_string1, season_length1, string1)

    tt_string2 = reader.get_ttcode(string2)
    season_length2 = reader.get_season_length(tt_string2)
    data2 = reader.get_csv(tt_string2, season_length2, string2)

    graphs = Graphs()
    graphs.scatterplot(data1, data2, string1, string2)
    graphs.boxplot(data1, data2, string1, string2)
    graphs.multi(data1,data2,string1,string2)

if __name__ == '__main__':
    main()
