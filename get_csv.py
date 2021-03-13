'''
This file takes in the search terms and finds the correct url for the search
terms using the get_ttcode() method. From here the scraper requests the URL
for each of the seasons. The program will then parse through the html file
and finds the necessary values. From here those values are exported to a
csv with the title of the first string within the seach term.
'''
from bs4 import BeautifulSoup
from requests import get
import imdb
import pandas as pd


class GetCSV:
    '''
    This class is responsible for getting all of the info for the file names.
    The program takes in a string and then retrieves the imdb TT code based
    on the index. From here it finds the season length through imdbpy. Then
    using these values, the program loops through the html for the respective
    seasons. It exports them to csv using the first word in the search term.
    '''
    def get_csv(self, tt_code, season_length, string):
        '''
        This method takes in the season-length and the ttcode in order to
        request the url from imdb. From here it loops over all of the episode
        blocks within the URL and finds the season, the episode number, the
        imdb rating, and title. In order to avoid an error where tv shows
        are listed but not yet rated, we use the the try feature to see if there
        is a rating. If the episode isn't rated then we break out of the loop,
        however this could cause problems on more obscure shows. Next the main
        loops over all of the seasons by adding the season string at the end of
        the url. Finally the list of lists collected in the web scraper is put
        into a panda file and then exported to a csv(with the word of the string
        being the name of the file).
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
        return name

    def get_season_length(self, tt_string):
        '''
        This method uses the imdbPY plug in to find the number of seasons based
        on the tt code found in the former method. From here we look at the
        season-length column in the imdbPy data base.
        '''
        ia = imdb.IMDb()
        series = ia.get_movie(tt_string)
        #print(series)
        count = series.data['number of seasons']
        return(count)

    def get_ttcode_list(self, string):
        '''
        This method uses the imdbpy package and gets a list of potential results
        from the search string. We use this as a double check to make sure the
        user has the correct TV show.
        '''
        ia = imdb.IMDb()
        search = ia.search_movie(string)
        list_id = []
        for i in search:
            list_id.append(i)
        return list_id

    def get_ttcode(self, string, index):
        '''
        This method takes in the index and the string term both from user
        input. We have done this since the default index can give us unexpected
        result terms from the search. We encountered some strange result, for
        example we kept getting "The Sorpranos" when searching Family Guy. This
        method then calls the search movie method from IMDB package but we
        import the term index from user input so we can make sure that the right
        show is being extracted.
        '''
        ia = imdb.IMDb()
        search = ia.search_movie(string)
        id = search[int(index)].movieID
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
