import scrapy
import json


class PricespiderSpider(scrapy.Spider):
    name = "pricespider"
    allowed_domains = ["www.rightmove.co.uk"]
    start_urls = ["https://www.rightmove.co.uk/house-prices/southwark-85215.html?soldIn=1"]


    def parse(self, response):
        script_content = response.xpath("//script[contains(text(), 'window.__staticRouterHydrationData')]//text()").get()[37:-1]
        raw_json = script_content.split('JSON.parse("')[1].rsplit('")', 1)[0]
        clean_json = raw_json.replace('\\"', '"').replace('\\n', '')
        data = json.loads(clean_json)

        # Cela a fonctionné, car vous avez correctement suivi la hiérarchie de la structure JSON.
        properties = data['loaderData']['property-search-by-location']['properties']

        if len(properties) == 0:
            return None

        for item_propertie in properties:
            yield{
                'address': item_propertie['address'],
                'type': item_propertie['propertyType'],
                'transactions': item_propertie['transactions'],
                'location': item_propertie['location'],
                'url': item_propertie['detailUrl'],
            }
        
        current_page = int(response.url.split('=')[-1])
        next_page = current_page + 1

        if next_page > 100:
            return None

        next_page_url = f"https://www.rightmove.co.uk/house-prices/southwark-85215.html?soldIn={next_page}"
        
        # Appele recurcive
        yield response.follow(next_page_url, callback=self.parse)

