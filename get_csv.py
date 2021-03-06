from bs4 import BeautifulSoup
from requests import get
from imdb import IMDb
import imdb
import pandas as pd

def get_csv(tt_code, season_length, string):
    string = string.split()[0]
    url = 'https://www.imdb.com/title/tt{code}/episodes?season=1'.format(code= tt_code)
    data = []
    for sn in range(1, int(season_length) + 1):
        url = get('https://www.imdb.com/title/tt{code}/episodes?season='.format(code= tt_code) + str(sn))
        print(url)
        website = BeautifulSoup(url.text, 'html.parser')
        episode_blocks = website.find_all('div', class_= 'info')
        for episodes in episode_blocks:
            season = sn
            episode_num = episodes.meta['content']
            try:
                imdb_rating = episodes.find('span', class_='ipl-rating-star__rating').text
            except:
                break
            else:
                title = episodes.a['title']
                episode_info = [season, episode_num, imdb_rating, title]
                data.append(episode_info)
    print(data)
    name = 'tv_show_data_' + string
    name = pd.DataFrame(data, columns = ['season', 'episode_num', 'imdb_rating', 'title'])
    name.to_csv('{}.csv'.format(string),index=False)


def get_season_length(tt_string):
    ia = imdb.IMDb()
    series = ia.get_movie(tt_string)
    count = series.data['number of seasons']
    return(count)

def get_ttcode(string):
    import imdb
    ia = imdb.IMDb()
    search = ia.search_movie(string)
    id = search[0].movieID
    return id


def main():
    string = "game of thrones"
    tt_string = get_ttcode(string)
    season_length = get_season_length(tt_string)
    print(season_length, tt_string, string)
    get_csv(tt_string, season_length, string)

if __name__ == '__main__':
    main()
