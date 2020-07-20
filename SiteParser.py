from bs4 import BeautifulSoup
import requests
from config import Bot_info


class Steam:
    def __init__(self, url):
        self.__data = BeautifulSoup(requests.get(str(url)).text, 'html.parser')
        self.url = str(url)

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
            return str(self.__data.find('div', {'class': 'profile_ban'}).text[:-7])
        else:
            return str('No VAC on record.')

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
            return str('Not stated')

    def getTotalScreenshots(self):
        try:
            screenshot_block = self.__data.find('a', {'href': f'{self.url}screenshots/'})
            return int(screenshot_block.find('span', {'class': 'profile_count_link_total'}).text)
        except Exception:
            return str('Not stated')

    def getTotalFriends(self):
        try:
            friend_block = self.__data.find('a', {'href': f'{self.url}friends/'})
            friends = friend_block.find('span', {'class': 'profile_count_link_total'})

            del friend_block
            return int(friends.text)
        except Exception:
            return str('Not stated')

    def getTotalBages(self):
        try:
            bages_block = self.__data.find('a', {'href': f'{self.url}badges/'})
            return bages_block.find('span', {'class': 'profile_count_link_total'}).text
        except Exception:
            return str('Not stated')


class CtfBans:
    def __init__(self, url):
        self.__data = BeautifulSoup(requests.get(url, headers=Bot_info.heads).text, 'html.parser')
        self.__lines = self.__data.findAll('td', {'height': '16',
                                                  'class': 'listtable_1'})
        self.name = self.__lines[4].text.replace('\n', '')
        self.steam_id = self.__lines[6].text[1:-1]
        self.date = self.__lines[12].text
        self.steam_ulr = 'https://steamcommunity.com/profiles/' + self.__lines[10].text.replace('\n', '')
        self.length = self.__lines[14].text[:-1]
        self.reason = self.__lines[18].text


class Covid:
    __url = 'https://www.google.com/search?q=covid+19+statistics&oq=covid+19+s&aqs=chrome.1.69i57j0l7.6379j0j15' \
            '&sourceid=chrome&ie=UTF-8 '
    __data = BeautifulSoup(requests.get(__url, headers=Bot_info.heads).text, 'html.parser')

    def getInfected(self):
        return self.__data.findAll('div', {'jsname': 'fUyIqc'})[37].text

    def getDeath(self):
        return self.__data.findAll('div', {'jsname': 'fUyIqc'})[40].text

    def getHealed(self):
        return self.__data.findAll('div', {'jsname': 'fUyIqc'})[39].text


class Tf2stats:
    """
            Парсит статистику tf2 через сайт:
            https://steamcharts.com/app/440#All
            """
    __url = "https://steamcharts.com/app/440#All"
    __data = BeautifulSoup(requests.get(__url, headers=Bot_info.heads).text, 'html.parser')

    def getMinutesOnline(self):
        return self.__data.findAll('div', {'class': 'app-stat'})[0].text[1:-10]

    def getDayOnline(self):
        return self.__data.findAll('div', {'class': 'app-stat'})[1].text[1:-15]

    def getAllTimeOnline(self):
        return self.__data.findAll('div', {'class': 'app-stat'})[2].text[1:-16]
