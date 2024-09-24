import scrapy

class PlutoSpider(scrapy.Spider):
    name = 'pluto_spider'
    start_urls = ['https://pluto.tv/on-demand/']

    def parse(self, response):
        for item in response.css('.itemContainer-0-2-262'):
            title = item.css('img::attr(alt)').get()
            link = item.css('a::attr(href)').get()

            if title and link:
                yield {
                    'title': title,
                    'link': response.urljoin(link),
                }
        next_page_url = response.css('.paginateRightButton-0-2-260::attr(href)').get()
        if next_page_url:
            yield response.follow(next_page_url, self.parse)

    def parse_livetv(self, response):
    
        for channel in response.css('.channelListItem-0-2-259.channel'):
            channel_name = channel.css('a .channel-0-2-266::attr(aria-label)').get()
            channel_link = channel.css('a::attr(href)').get()

            if channel_name and channel_link:
                yield {
                    'channel_name': channel_name,
                    'channel_link': response.urljoin(channel_link),
                }

        next_page_url = response.css('.paginateRightButton-0-2-260::attr(href)').get()
        if next_page_url:
            yield response.follow(next_page_url, self.parse_livetv)

    def start_requests(self):
        yield scrapy.Request('https://pluto.tv/latam/live-tv/', self.parse_livetv)
