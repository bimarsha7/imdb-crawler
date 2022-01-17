import scrapy
from  imdb_crawler.items import ImdbCrawlerItem

def get_imdb_urls(csv_data='imdb_urls.csv'):
    import pandas as pd
    df = pd.read_csv(csv_data, delimiter=',')
    return list(df['imdb_url'])[1000:2000]

class ImdbSpider(scrapy.Spider):
    name = "imdb"
    allowed_domains = ["www.imdb.com"]
    # start_urls = [
    #     "http://www.imdb.com/title/tt1392190/",
    #     "http://www.imdb.com/title/tt0845448",
    #     "https://www.imdb.com/title/tt0303602/",
    #     "https://www.imdb.com/title/tt0322259/"
    # ]
    start_urls = get_imdb_urls()

    def parse(self, response):
        item = ImdbCrawlerItem()
        current_url = response.request.url
        title_res_xpath = response.xpath('//h1[@data-testid="hero-title-block__title"]/text()').extract()
        title_metadata_res_xpath = response.xpath('//ul[@data-testid="hero-title-block__metadata"]/li/span/text()').extract()
        top_cast_res_xpath = response.xpath('//a[@data-testid="title-cast-item__actor"]/text()').extract()[:8]
        director_res_xpath = response.xpath('//a[@class="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"]/text()').extract_first()
        genre_res_xpath    = response.xpath('//li[@data-testid="storyline-genres"]/div/ul/li/a/text()').extract()
        tagline_res_xpath  = response.xpath('//li[@data-testid="storyline-taglines"]/div/div/ul/li/span/text()').extract_first()
        plot_keywords_xpath = response.xpath('//div[@data-testid="storyline-plot-keywords"]/a/span/text()').extract()[:5]

        item['imdbId']   = current_url.split('/')[-2]
        item['title']    = title_res_xpath
        item['title_metadata'] = title_metadata_res_xpath
        item['top_cast'] = top_cast_res_xpath
        item['director'] = director_res_xpath
        item['genre']    = genre_res_xpath
        item['taglines'] = tagline_res_xpath
        item['plot_keywords'] = plot_keywords_xpath

        plot_summary_text = response.xpath('//ul[@data-testid="storyline-plot-links"]/li[1]/a/text()').extract()
        
        if ''.join(plot_summary_text) == 'Plot summary':
            plot_summary_href  = response.xpath('//ul[@data-testid="storyline-plot-links"]/li[1]/a/@href').extract()
            url = ''.join(plot_summary_href).split('/')
            url = ''.join(url[3:])

            if plot_summary_href:
                yield scrapy.Request(
                    response.urljoin(url),
                    callback=self.parse_plot_summary,
                    meta = {'item': item}
                )
        else: 
            yield item

    def parse_plot_summary(self, response):
        plot_summary_xpath = response.xpath('//ul[@id="plot-summaries-content"]/li/p/text()').extract_first()
        item = response.meta['item']
        item['plot'] = plot_summary_xpath
        yield item
