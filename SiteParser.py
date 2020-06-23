from bs4 import BeautifulSoup
import requests


class Steam:
    def __init__(self, url):
        self.__data = BeautifulSoup(requests.get(str(url)).text, 'html.parser')
        self.url = str(url)

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
        image = str(image.find('img'))
        return image[10:-3]

    def getTotalGames(self):
        try:
            games_block = self.__data.find('a', {'href': f'{self.url}games/?tab=all'})
            return int(games_block.find('span', {'class': 'profile_count_link_total'}).text)

        except Exception as e:
            return str('Not stated')

    def getTotalComments(self):
        try:
            comments_block = self.__data.find('a', {'class': 'commentthread_allcommentslink'})
            return comments_block.find('span').text

        except Exception as e:
            return str('Not stated')

    def getTotalScreenshots(self):
        try:
            screenshot_block = self.__data.find('a', {'href': f'{self.url}screenshots/'})
            return int(screenshot_block.find('span', {'class': 'profile_count_link_total'}).text)
        except Exception as e:
            return str('Not stated')

    def getTotalFriends(self):
        try:
            friend_block = self.__data.find('a', {'href': f'{self.url}friends/'})
            friends = friend_block.find('span', {'class': 'profile_count_link_total'})

            del friend_block
            return int(friends.text)
        except Exception as e:
            return str('Not stated')

    def getTotalBages(self):
        try:
            bages_block = self.__data.find('a', {'href': f'{self.url}badges/'})
            return bages_block.find('span', {'class': 'profile_count_link_total'}).text
        except Exception as e:
            return str('Not stated')


class CtfBans:
    def __init__(self, url):
        self.__data = BeautifulSoup(requests.get(str(url)).text, 'html.parser')

    def getLastUserName(self):
        table = self.__data.find('div', {'style': 'float:left;'}).text
        return str(table[23:])

    def getLastBanTime(self):
        tbl = self.__data.find('tr', {'class': 'tbl_out'})
        time = tbl.findAll('td', {'height': '16',
                                  'align': 'center',
                                  'class': 'listtable_1'})[1].text
        return str(time)

    def getLastBanLength(self):
        return self.__data.find('td', {'width': '20%',
                                       'height': '16',
                                       'align': 'center'}).text
