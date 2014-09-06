from models.leek_crawl import LeekCrawl
from models.leek import Leek
from services.scrap import scrap_leek_crawl
import logging

logger = logging.getLogger('scraping')

def process_scrap(leek_crawl):
    try:
        info = scrap_leek_crawl(leek_crawl.crawl)
    except Except as e:
        logger.exception(e)
    else:
        info['leek_id'] = leek_crawl.leek_id
        Leek(**info).save()

def scrap_all(leek_crawls):
    for leek_crawl in leek_crawls:
        process_scrap(leek_crawl)
