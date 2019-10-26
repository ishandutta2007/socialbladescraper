import scrapy
import pprint as pp


class Top5000Spider(scrapy.Spider):
    name = "top5000"

    def start_requests(self):
        urls = [
            'https://socialblade.com/youtube/top/5000/',
            'https://socialblade.com/youtube/top/5000/mostviewed/',
            'https://socialblade.com/youtube/top/5000/mostsubscribed/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        hrefs = response.css('a::attr(href)').getall()
        hrefs = [h for h in hrefs if '/youtube/c/' in h or '/youtube/channel/' in h or '/youtube/user/' in h]
        page = response.url.split("/")[-2]
        filename = 'top5000-{}.txt'.format(page)
        with open(filename, 'w') as f:
            f.write("\n".join(hrefs).replace("\n\n","\n"))

        self.log('Saved file {}'.format(filename))
