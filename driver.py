'''
this program is the main method for out program. It takes in the nessisary
inputs and drives the program. It deafults to doing family guy and american Dad
unless otherwise directed.
'''
from get_csv import GetCSV
from graphs import Graphs

user_input = False


def main():
    '''
    In this method we ask the user if the want to enter a show
    if not it defaults family guy and american dad. Due to an error in the imdb
    PY data base, family guy when searched the first output the sorpranos. In
    our testing this error does not happen on most other tv show. To fix these
    we coded in an index feature for each of the data sets. From here we are
    set the respected dataset and graph them 3 differnt ways.
    '''
    reader = GetCSV()
    if input("Do you want to input TV shows? Y or N : ") == "Y":
        string1 = input("Enter 1st TV show: ")
        string2 = input("Enter 2nd TV show: ")
        index1 = 0
        index2 = 0
    else:
        string1 = "Family Guy"
        string2 = "American Dad"
        index1 = 1
        index2 = 0
    tt_string1 = reader.get_ttcode(string1, index1)
    season_length1 = reader.get_season_length(tt_string1)
    print(tt_string1, season_length1)
    data1 = reader.get_csv(tt_string1, season_length1, string1)

    tt_string2 = reader.get_ttcode(string2, index2)
    season_length2 = reader.get_season_length(tt_string2)
    data2 = reader.get_csv(tt_string2, season_length2, string2)

    graphs = Graphs()
    graphs.scatterplot(data1, data2, string1, string2)
    graphs.boxplot(data1, data2, string1, string2)
    graphs.multi(data1, data2, string1, string2)


if __name__ == '__main__':
    main()
