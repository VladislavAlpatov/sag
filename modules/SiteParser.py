from bs4 import BeautifulSoup
import requests


class Steam:
    """parse steam profile info"""
    def __init__(self, url: str):
        self.__data = BeautifulSoup(requests.get(url).text, 'html.parser')

        if url[-1] != '/':
            self.url = url + '/'
        else:
            self.url = url

    def __str__(self):
        return 'Steam profile parser by NullifiedVlad'

    def getNick(self):
        return self.__data.find('span', {'class': 'actual_persona_name'}).text

    def getLvl(self):
        return int(self.__data.find('span', {'class': 'friendPlayerLevelNum'}).text)

    def getGameStatus(self):
        return self.__data.find('div', {'class': 'profile_in_game_header'}).text

    def getVacStatus(self):
        if bool(self.__data.find('div', {'class': 'profile_ban'})):
            return self.__data.find('div', {'class': 'profile_ban'}).text[:-7]
        else:
            return 'No VAC on record.'

    def getProfilePicture(self):
        image = self.__data.find('div', {'class': 'playerAvatarAutoSizeInner'})
        url_list = image.findAll('img')

        del image

        if len(url_list) == 2:
            url = str(url_list[1])
            return url[10:-3]
        else:
            url = str(url_list[0])
            return url[10:-3]

    def getTotalGames(self):
        try:

            games_block = self.__data.find('a', {'href': f'{self.url}games/?tab=all'})
            return int(games_block.find('span', {'class': 'profile_count_link_total'}).text)

        except Exception:
            return str('Not stated')

    def getTotalComments(self):
        try:
            comments_block = self.__data.find('a', {'class': 'commentthread_allcommentslink'})
            return comments_block.find('span').text

        except Exception:
            return 'Not stated'

    def getTotalScreenshots(self):
        try:
            screenshot_block = self.__data.find('a', {'href': f'{self.url}screenshots/'})
            return int(screenshot_block.find('span', {'class': 'profile_count_link_total'}).text)
        except Exception:
            return 'Not stated'

    def getTotalFriends(self):
        try:
            friend_block = self.__data.find('a', {'href': f'{self.url}friends/'})
            friends = friend_block.find('span', {'class': 'profile_count_link_total'})

            del friend_block
            return int(friends.text)

        except Exception:
            return 'Not stated'

    def getTotalBages(self):
        try:
            bages_block = self.__data.find('a', {'href': f'{self.url}badges/'})
            return bages_block.find('span', {'class': 'profile_count_link_total'}).text
        except Exception:
            return 'Not stated'


class Tf2stats:
    """
    Get tf2 stats fro this site:
    https://steamcharts.com/app/440#All"""

    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0'}
        self.__data = BeautifulSoup(requests.get("https://steamcharts.com/app/440#All",
                                                 headers=self.headers).text,
                                    'html.parser')

    def getMinutesOnline(self):
        return self.__data.findAll('div', {'class': 'app-stat'})[0].text[1:-10]

    def getDayOnline(self):
        return self.__data.findAll('div', {'class': 'app-stat'})[1].text[1:-15]

    def getAllTimeOnline(self):
        return self.__data.findAll('div', {'class': 'app-stat'})[2].text[1:-16]
