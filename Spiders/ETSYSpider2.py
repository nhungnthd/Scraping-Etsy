import json
import scrapy
import pandas as pd

base_url = 'https://www.etsy.com/uk/search?q=best+selling+product&ref=pagination&page={}'

class ETSYScraper2(scrapy.Spider):
    name = "ETSYScraper2"

    # initialize the spider with the first page of the base URL
    def __init__(self, name=None, **kwargs):
        super(ETSYScraper2, self).__init__(name, **kwargs)
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
        # locate the script tag containing ld+json data
        script_text = response.css(
            'script[type="application/ld+json"]::text'
        ).extract_first()

        # check if script text is not None and not empty
        if script_text:
            # parse the JSON content
            json_data = json.loads(script_text)

            # access data from the JSON object
            item_list = json_data.get('itemListElement', [])

            for item in item_list:
                # get product url using for send request to get detail
                product_url = item.get('url')

                # send a request for the product detail page and yield the product URL
                yield scrapy.Request(product_url, callback=self.parse_product_detail)

        self.page_number += 1
        if self.page_number <= 10:
            next_page_url = base_url.format(self.page_number)
            yield scrapy.Request(next_page_url, callback=self.parse)

    # parse product detail
    def parse_product_detail(self, response):
        script_text_product_detail = response.css(
            'script[type="application/ld+json"]::text'
        ).extract_first()

        # check if script text is not None and not empty
        if script_text_product_detail:
            # parse the JSON content
            json_data = json.loads(script_text_product_detail)

            # extract product details from the JSON data
            product_data = {
                'product_url': json_data.get('url', ''),
                'product_name': json_data.get('name', ''),
                'product_sku': json_data.get('sku', ''),
                # 'product_description': json_data.get('description', ''),
                'product_images': [image.get('contentURL', '') for image in json_data.get('image', [])],
                'product_category': json_data.get('category', ''),
                'product_brand': json_data.get('brand', {}).get('name', ''),
                'product_rating': json_data.get('aggregateRating', {}).get('ratingValue', ''),
                'product_review_count': json_data.get('aggregateRating', {}).get('reviewCount', ''),
                'product_price': json_data.get('offers', {}).get('price', ''),
                'product_price_currency': json_data.get('offers', {}).get('priceCurrency', ''),
            }

            # extract reviews
            reviews = []
            for review in json_data.get('review', []):
                review_info = {
                    'review_rating': review.get('reviewRating', {}).get('ratingValue', ''),
                    'review_date_published': review.get('datePublished', ''),
                    'review_body': review.get('reviewBody', ''),
                    'review_author': review.get('author', {}).get('name', ''),
                }
                reviews.append(review_info)

            product_data['product_reviews'] = reviews

            # append the product data to the product_data list
            self.product_data.append(product_data)

    def closed(self, reason):
        df = pd.DataFrame(self.product_data)
        df.to_csv("./etsy_data_product_details.csv", index=False)
