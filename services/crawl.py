import requests
import logging

class Crawler:
    base_url = 'http://leekwars.com'
    user = {
        'login': '0imNKvn0w6uQ',
        'leek_name': ['23r2SYM1RW9zFg'],
        'password': 'g6wfHdTez3uTw',
        'mail': '0imNKvn0w6uQ@yopmail.com'
    }

    def __init__(self):
        self.connected = False
        self.connection_cookies = None
        self.logger = logging.getLogger('crawler')

    def connect(self, nb_tries=3):
        if nb_tries < 0:
            self.logger.error('Impossible to connect to the website')
            return False

        self.logger.info('Try to connect to the website')
        url = Crawler.base_url + '/index.php?page=login_form'
        params = {
            'login': Crawler.user['login'],
            'pass': Crawler.user['password'],
        }

        try:
            res = requests.post(url, data=params)
        except IOError:
            raise

        if res.ok:
            self.connected = True
            self.connection_cookies = res.cookies
            return True

        self.logger.warning('Error when trying to connect (HTTP %d)' % self.status_code)
        return self.connect(nb_tries - 1)

    def crawl_leek(self, leek_id, reconnect=False):
        if not self.connected or reconnect:
            try:
                self.connect()
            except IOError:
                raise
        if not self.connected:
            raise IOError('Impossible to crawl the leek %s' % leek_id)

        self.logger.info('Try to crawl the leek %s' % leek_id)
        url = Crawler.base_url + '/leek/%s' % leek_id

        try:
            res = requests.get(url, cookies=self.connection_cookies)
        except IOError:
            raise

        if res.ok:
            content = res.content.decode(encoding='utf-8')
            if not 'Poireau introuvable' in content:
                return content
            else:
                raise IOError('Leek %s doesn\' exist' % leek_id)

        self.logger.warning('Error when trying to crawl (HTTP %d)' % res.status_code)
        if not reconnect:
            return self.crawl_leek(leek_id, True)
        raise IOError('Impossible to crawl the leek %s' % leek_id)
