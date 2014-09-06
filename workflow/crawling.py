from models.leek_crawl import LeekCrawl
from services.crawl import Crawler

def process_crawl(crawler, leek_id):
    try:
        leek = LeekCrawl.objects.get(leek_id=leek_id)
    except LeekCrawl.DoesNotExist:
        pass
    else:
        return

    try:
        crawl = crawler.crawl_leek(leek_id)
    except IOError:
        return
    leek = LeekCrawl(leek_id=leek_id, crawl=crawl).save()

def crawl_all(leek_ids):
    crawler = Crawler()
    for leek_id in leek_ids:
        process_crawl(crawler, str(leek_id))
