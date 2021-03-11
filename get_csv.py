from bs4 import BeautifulSoup
from requests import get
import imdb
import pandas as pd


class GetCSV:
    def get_csv(self, tt_code, season_length, string):
        '''
        this method takes in the season-length and the ttcode and requests the
        url from imdb. From here it loops over all of the episode blocks within
        the URL and finds the sn number, the episode num and the imdb rating as
        well as title. In order to avoid an error where tv shows are listed but
        not yet rated. We use the the try feature to see if there is a rating.
        If the episode isn't rated then we break out of the loop. This could
        cause problems on more obscure shows. Next the main loops over all of
        the seasons by using adding the season string at the end of the url.
        Finally the list of lists collected in the web scraper is put into a
        panda file and then exported to a csv. With the word of the string
        being the name ofthe file.
        '''
        string = string.split()[0]
        url = ('https://www.imdb.com/title/tt{code}/episodes'
               + '?season=1').format(code=tt_code)
        data = []
        for sn in range(1, int(season_length) + 1):
            url = get(('https://www.imdb.com/title/tt{code}/episodes'
                      + '?season=').format(code=tt_code) + str(sn))
            website = BeautifulSoup(url.text, 'html.parser')
            episode_blocks = website.find_all('div', class_='info')
            for episodes in episode_blocks:
                season = sn
                episode_num = episodes.meta['content']
                try:
                    imdb_rating = episodes.find('span',
                                                class_='ipl-rating-star'
                                                       + '__rating').text
                except:
                    break
                else:
                    title = episodes.a['title']
                    episode_info = [season, episode_num, imdb_rating, title]
                    data.append(episode_info)
        name = 'tv_show_data_' + string
        name = pd.DataFrame(data, columns=['season', 'episode_num',
                                           'imdb_rating', 'title'])
        name.to_csv('{}.csv'.format(string), index=False)

    def get_season_length(self, tt_string):
        '''
        this uses the imdbPY plug in to find the number of seasons based on the
        tt code found in the former method. From here we look at the
        seasonlength column in the imdbPy data base.
        '''
        ia = imdb.IMDb()
        series = ia.get_movie(tt_string)
        print(series)
        count = series.data['number of seasons']
        return(count)

    def get_ttcode_list(self, string):
        '''
        This method uses the imdbpy package in get a list of potential results
        From the search string. We use this as a double check to make sure
        the user has the correct TV show/
        '''
        ia = imdb.IMDb()
        search = ia.search_movie(string)
        list_id = []
        for i in search:
            list_id.append(i)
        return list_id

    def get_ttcode(self, string, index):
        '''
        Takes in the index and the string term both from user input. We have
        done the index as often there is unexpected result terms from the
        search. We encounterd some strange result, like getting the sorpranos
        when searching family guy. Then we are copy the search method from
        above, but import the term index from user input so we can make sure
        that the right show is being extracted.
        '''
        ia = imdb.IMDb()
        search = ia.search_movie(string)
        id = search[index].movieID
        return id


# def main():
    # string = "family Guy"
    # tt_list = get_ttcode_list(string)
    # print(tt_list)
    # print("What index looks like the show you are looking to graph?")
    # tt_string = get_ttcode('family guy', 1)
    # print(tt_string)
    # season_length = get_season_length(tt_string)
    # print(season_length)
    # get_csv(tt_string, season_length, string)

# if __name__ == '__main__':
    # main()
