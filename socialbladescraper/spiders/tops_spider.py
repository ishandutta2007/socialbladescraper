import scrapy
import pprint as pp


class TopsSpider(scrapy.Spider):
    name = "tops"

    def start_requests(self):
        urls = [
            "https://socialblade.com/youtube/top/5000",
            "https://socialblade.com/youtube/top/5000/mostviewed",
            "https://socialblade.com/youtube/top/5000/mostsubscribed",
            "https://socialblade.com/instagram/top/500",
            "https://socialblade.com/instagram/top/500/followers",
            "https://socialblade.com/instagram/top/500/following",
            "https://socialblade.com/instagram/top/500/media",
            "https://socialblade.com/instagram/top/500/engagement-rate",
            "https://socialblade.com/twitter/top/100/tweets",
            "https://socialblade.com/twitter/top/100/engagements",
            "https://socialblade.com/twitter/top/100/following",
            "https://socialblade.com/twitter/top/100/followers",
            "https://socialblade.com/facebook/top/500",
            "https://socialblade.com/facebook/top/500/likes",
            "https://socialblade.com/dailymotion",
            "https://socialblade.com/mixer/top/500/most-followers",
            "https://socialblade.com/mixer/top/500/most-viewed",
            "https://socialblade.com/mixer/top/500/highest-level",
            "https://socialblade.com/mixer/top/500/highest-sparks",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        hrefs = response.css("a::attr(href)").getall()
        platform = response.url.split("/")[3]
        hrefs = [
            h
            for h in hrefs
            if "/{}/c/".format(platform) in h
            or "/{}/channel/".format(platform) in h
            or "/{}/user/".format(platform) in h
            or "/{}/page/".format(platform) in h
        ]
        filename = "output/{}.txt".format("_".join(filter(None, response.url.split("/")[3:])))
        with open(filename, "w") as f:
            f.write("\n".join(hrefs).replace("\n\n", "\n"))

        self.log("Saved file {}".format(filename))
