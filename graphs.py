'''
This file contains all of our methods for creating our 3 visualizations.
Every function within this file takes in two datasets and two show names
in order to generate a scatterplot with trend lines, a comparative
boxplot, and a figure with scatterplots of the last 5 seasons of both
shows.
'''
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


class Graphs:
    '''
    This class is reponsible for generating all of the plots used
    for driver.py. From using the input of two datasets and two show
    names, this class has methods to generate a scatterplot with
    trendlines, acomparative boxplot, and a figure with scatterplots
    of the last 5 seasons of both shows.
    '''
    def testing(self, data1, data2, string1, string2):
        '''
        This method is used primarily for testing / comparison
        purposes. This method simply lists the top 5 highest rated
        episodes for each of the two shows, as well as their rating
        and season and episode number.
        '''
        data1['imdb_rating'] = pd.to_numeric(data1['imdb_rating'])
        data2['imdb_rating'] = pd.to_numeric(data2['imdb_rating'])
        print("Top 5 highest rated episodes for each show")
        print(string1 + ":")
        print(data1.nlargest(5, 'imdb_rating'))
        print("\n" + string2 + ":")
        print(data2.nlargest(5, 'imdb_rating'))

    def scatterplot(self, data1, data2, string1, string2):
        '''
        This method generates two scatterplots from two sets of data and
        displays them overlapped on a single figure. The scatterplot
        is comparing the number of seasons vs the imdb ratings for each
        season(each data point is an episode). The plot also contains
        trend lines for both of the shows.
        '''
        # print(data1)
        concat = pd.concat([data1.assign(shows=string1),
                            data2.assign(shows=string2)])
        concat['imdb_rating'] = pd.to_numeric(concat['imdb_rating'])
        sns.lmplot(x='season', y='imdb_rating', data=concat,
                   hue='shows', height=6, aspect=1)
        # plot = sns.joinplot(data=concatenated, x="season"
        # ,y="imdb_rating",hue = "shows")
        # plot.set_yticklabels([0,1,2,3,4,5,6,7,8,9])
        # print(concat)
        # print(concat.columns)
        title = "IMDb ratings of {} vs {}".format(string1.capitalize(),
                                                  string2.capitalize())
        plt.title(title, pad=0.2)
        plt.savefig('scatter.png', bbox_inches='tight')
        plt.show()

    def boxplot(self, data1, data2, string1, string2):
        '''
        This method generates a comparative boxplot based on two sets
        of data. It plots the number of seasons vs the imdb ratings for
        each season(the data itself uses the imdb ratings from every
        episode). We are also plotting any outlier episodes that had
        an unusally high or low imdb rating.
        '''
        concat = pd.concat([data1.assign(shows=string1),
                            data2.assign(shows=string2)])
        concat['imdb_rating'] = pd.to_numeric(concat['imdb_rating'])
        sns.boxplot(x="season", y="imdb_rating", hue="shows",
                    data=concat, palette="Set3")
        title = ("Comparative Boxplots of IMDb "
                 + "ratings of {} vs {}").format(string1.capitalize(),
                                                 string2.capitalize())
        plt.title(title)
        plt.savefig('boxplot.png', bbox_inches='tight')
        plt.show()

    def multi(self, data1, data2, string1, string2):
        '''
        This method generates a figure that contains 5 scatterplots of
        the last 5 seasons from both shows that are passed. If one of
        the shows doesn't have at least 5 seasons, we plot however many
        seasons that show has.
        '''
        concat = pd.concat([data1.assign(shows=string1),
                            data2.assign(shows=string2)])
        concat['imdb_rating'] = pd.to_numeric(concat['imdb_rating'])
        seasons = min(data1['season'].max(), data2['season'].max())
        concat["episode_num"] = pd.to_numeric(concat["episode_num"],
                                              downcast="float")
        num_plots = min(seasons, 5)
        fig, axes = plt.subplots(1, num_plots)
        fig.set_figheight(15)
        fig.set_figwidth(15)
        offest = seasons - 5
        title = ("Comparison of the last 5 seasons"
                 + " ratings of {} v"
                 + "s {}").format(string1.capitalize(),
                                  string2.capitalize(), loc='left')
        fig.suptitle(title, verticalalignment='bottom')
        for i in range(seasons-5, seasons):
            concatenated1 = concat[concat['season'] == i + 1]
            # print(concatenated1)
            sns.scatterplot(ax=axes[i-offest], x='episode_num',
                            y='imdb_rating', data=concatenated1,
                            hue="shows")
            axes[i-offest].set_xlabel('Season '+str(i+1))
            if i-offest == 0:
                axes[i-offest].set_ylabel('IMDB Rating')
            else:
                axes[i-offest].set_ylabel('')
        plt.savefig('multiplot.png', bbox_inches='tight')
        plt.show()
