import scrapy, csv

class BlogSpider(scrapy.Spider):
    name = "blogspider"
    start_urls = ["http://gamek.vn/su-that-kinh-hoang-lieu-co-phai-chinh-doctor-strange-da-tu-nguy-tao-vu-tai-nan-cua-minh-20190212133036234.chn"]

    def __init__(self):
        with open('results.txt', mode="w") as csv_file:
            crawler_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            crawler_writer.writerow(['url', 'title', 'author', 'date'])

    def parse(self, response):
        for title in response.css('h1'):
            single_blog = {
                'url':response.url,
                'title': title.css("::text").get().replace("\r\n", ""),
                'author':response.css("span.author::text").get(),
                'date': response.css("p.mgt15").get().split('|')[1].replace("\r\n", "").replace("</p>","")
                }
            single_blog_for_csv = [
                response.url,
                title.css("::text").get().replace("\r\n", ""),
                response.css("span.author::text").get(),
                response.css("p.mgt15").get().split('|')[1].replace("\r\n", "").replace("</p>","")
            ]
            self.write_to_csv(single_blog_for_csv)
            yield single_blog

        for next_page in response.css('.detailbt>ul>li>a'):
            yield response.follow(next_page, self.parse)
        
    def write_to_csv(self, result):
        with open('results.txt', mode="a") as csv_file:
            crawler_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            crawler_writer.writerow(result)