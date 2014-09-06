from workflow.crawling import crawl_all
from tqdm import tqdm
import mongoengine
import logging
import time
import random

logging.basicConfig(level=logging.DEBUG,
        format='[%(levelname)s][%(name)s][%(asctime)s] %(message)s')

def slow_generator(gen):
    for e in gen:
        yield e
        time.sleep((10 * random.random() + 0.50))

if __name__ == '__main__':
    mongoengine.connect('leekdb')
    ids = list(range(19000))
    random.shuffle(ids)
    crawl_all(slow_generator(tqdm(ids)))
