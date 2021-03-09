from bs4 import BeautifulSoup
from requests import get
from imdb import IMDb
import imdb
import pandas as pd
from get_csv import GetCSV
import seaborn as sns
import matplotlib.pyplot as plt




class Graphs:
    def __init__(self):
        self._name = None

    def scatterplot(self, data1, data2, string1, string2):
        concatenated = pd.concat([data1.assign(shows=string1), data2.assign(shows=string2)])
        concatenated['imdb_rating'] = pd.to_numeric(concatenated['imdb_rating'])
        plot = sns.lmplot(x='season', y='imdb_rating', data=concatenated, hue='shows', height = 6, aspect = 1)
        #plot = sns.joinplot(data=concatenated,x="season",y="imdb_rating",hue = "shows")
        #plot.set_yticklabels([0,1,2,3,4,5,6,7,8,9])
        print(concatenated)
        print(concatenated.columns)
        title = "IMDb ratings of {} vs {}".format(string1.capitalize(), string2.capitalize())
        plt.title(title, pad = 0.2)
        plt.savefig('scatter.png', bbox_inches = 'tight')
        plt.show()

    def multi(self, data1, data2, string1, string2):
        concatenated = pd.concat([data1.assign(shows=string1), data2.assign(shows=string2)])
        concatenated['imdb_rating'] = pd.to_numeric(concatenated['imdb_rating'])
        seasons = min(data1['season'].max(),data2['season'].max())
        concatenated["episode_num"] = pd.to_numeric(concatenated["episode_num"], downcast="float")
        fig, axes = plt.subplots(1,seasons)
        for i in range(seasons):
            concatenated1 = concatenated[concatenated['season']==i+1]    
            plot = sns.scatterplot(ax = axes[i], x='episode_num', y='imdb_rating', data = concatenated1,hue="shows")
            axes[i].set_xlabel('Season ' + str(i+1) + " episodes")
            axes[i].set_ylabel('IMDB Rating')
        print(concatenated.columns)

        plt.savefig('scatter2.png', bbox_inches = 'tight')
        plt.show()
