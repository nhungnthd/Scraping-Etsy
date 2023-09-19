import json
import scrapy
import pandas as pd

base_url = 'https://www.etsy.com/uk/search?q=best+selling+product&ref=pagination&page={}'

class ETSYScraper(scrapy.Spider):
    name = "ETSYScraper"
    
    # initialize the spider with the first page of the base url
    def __init__(self, name=None, **kwargs):
        super(ETSYScraper, self).__init__(name, **kwargs)
        self.page_number = 1
        self.start_urls = [base_url.format(self.page_number)]
        self.currencySymbol_currency = {
            '$': 'USD',
            '£': 'GBP'
        }
        # list to store extracted product data
        self.product_data = []  
        
    # start request method    
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)

    # parsing logic
    def parse(self, response):
        #  locate the script tag containing ld+json data
        script_text = response.css(
            'script[type="application/ld+json"]::text'
        ).extract_first()

        # check if script text is not none and not empty
        if script_text:
            # parse the json content
            json_data = json.loads(script_text)
            
            # access data from json object
            item_list = json_data.get('itemListElement', [])
            
            for item in item_list:
                product_title = item.get('name')
                product_url = item.get('url')
                product_image = item.get('image')
                product_brand_type = item.get('brand', {}).get('@type')
                product_brand_name = item.get('brand', {}).get('name')
                product_offers_type = item.get('offers', {}).get('@type')
                product_offers_price = item.get('offers', {}).get('price')
                product_offers_priceCurrency = item.get('offers', {}).get('priceCurrency')
                product_rating_value = item.get('aggregateRating', {}).get('ratingValue')
                product_reviewCount = item.get('aggregateRating', {}).get('reviewCount')
                
                # Extract the sale price from the HTML
                sale_price = response.css('p.wt-text-title-01.lc-price span.currency-value::text').extract_first()
                
                sale_price_symbol = response.css('p.wt-text-title-01.lc-price span.currency-symbol::text').extract_first()
                
                # convert price symbol to currency code
                sale_price_currency = self.currencySymbol_currency.get(sale_price_symbol, sale_price_symbol)
                
                # create a dictionary to store extracted data for items
                product_data_dict = {
                    'product_title': product_title,
                    'product_url': product_url,
                    'product_image': product_image,
                    'product_brand_type': product_brand_type,
                    'product_brand_name': product_brand_name,
                    'product_offers_type': product_offers_type,
                    'product_offers_price': product_offers_price,
                    'product_offers_priceCurrency': product_offers_priceCurrency,
                    'product_rating_value': product_rating_value,
                    'product_reviewCount': product_reviewCount,
                    'sale_price': sale_price,
                    'sale_price_currency': sale_price_currency
                }
                
                #  append data for items
                self.product_data.append(product_data_dict)
                
        # follow pagination to the next page 
        self.page_number += 1
        if self.page_number <= 10:
            next_page_url = base_url.format(self.page_number)
            yield scrapy.Request(next_page_url, callback=self.parse)

    def closed(self, reason):
        # save the result to csv 
        df = pd.DataFrame(self.product_data)
        df.to_csv("./etsy_data.csv", index=False)                
