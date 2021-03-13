'''
This file has our main method for our program. It takes in the necessary
inputs and drives the program. It defaults the inputs to be Family Guy
and American Dad unless the user specifies his/her own shows.
'''
from get_csv import GetCSV
from graphs import Graphs

user_input = False


def main():
    '''
    In this method we ask the user if they want to enter a show, and if they
    type 'N' the program defaults to Family Guy and American Dad. Due to an
    error in the IMDb PY data base, whenever Family Guy is searched the first
    output is "The Sorpranos". After testing we found that, this error does not
    happen on most tv shows. To fix this we coded in an index feature for
    each of the data sets. if the user wants to put in their own TV show the are
    prompted to selct theirapportare show from a list. From there we create the
    respective dataset and graph them 3 different ways.
    '''
    reader = GetCSV()
    if input("Do you want to input TV shows? Y or N : ") == "Y":
        string1 = input("Enter 1st TV show: ")
        string2 = input("Enter 2nd TV show: ")
        print()
        list1 = reader.get_ttcode_list(string1)
        print("Top 5 Search Results for ", string1, " :")
        #print(list1)
        for i in range(5):
            print((i+1),". ",list1[i])
        print()
        print('Select which show you prefer by their number.')
        #print('Index goes up by one after every line. Start from the top.')
        index1 = input("Select the index you prefer ")
        index1 = str(int(index1)-1)
        #index1 -= 1
        print('\n')
        list2 = reader.get_ttcode_list(string2)
        #print(list2)
        print()
        print("Top 5 Search Results for ", string2, " :")
        #print(list2)
        for i in range(5):
            print((i+1),". ",list2[i])
        print()
        print('Select the show that you prefer by their number.')
        #print('Index goes up by one after every line. Start from the top.')
        index2 = input("Select the index you prefer: ")
        index2 = str(int(index2)-1)
        #index2 -= 1
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
