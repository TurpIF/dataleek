from workflow.scraping import scrap_all
from models.leek_crawl import LeekCrawl
from tqdm import tqdm
import mongoengine
import logging

logging.basicConfig(level=logging.DEBUG,
        format='[%(levelname)s][%(name)s][%(asctime)s] %(message)s')

if __name__ == '__main__':
    mongoengine.connect('leekdb')
    scrap_all(tqdm(LeekCrawl.objects))
