# Scraping-Etsy

Scraping-Etsy is a versatile web scraping project built using [Scrapy](https://docs.scrapy.org/en/latest/), a robust web scraping and web crawling framework for Python. The project is specifically designed to extract valuable data from the popular e-commerce platform [Etsy](https://www.etsy.com/uk/search?q=best+selling+product). With this tool, you can collect comprehensive information about top-selling products on Etsy, including product details, pricing, ratings, and customer reviews.

## Overview

Etsy is renowned for its wide array of unique and handcrafted products. This project aims to empower users to gather essential data on the top-selling products available on Etsy. The collected data can serve multiple purposes, such as market analysis, competitor research, trend identification, and more. By harnessing web scraping techniques, you can unlock valuable insights from the Etsy marketplace.

## Features

- **Web Scraping:** Scraping top-selling product data from Etsy's website.
- **Data Extraction:** Retrieval of product details, prices, descriptions, images, ratings, and reviews.
- **Data Export:** Convenient export of scraped data to CSV files for in-depth analysis.
- **Customizable Spiders:** Adaptable and extensible Scrapy spiders for diverse data extraction needs.
- **ETSYScraper:** Used for extracting general product information from Etsy's search landing page.
- **ETSYScraper2:** Designed for extracting product data from individual product URLs, including reviews.

## Prerequisites

Before you can start using Scraping-Etsy, ensure that you have the following dependencies installed:

- **Python:** Python version 3.6 or higher.
- **Scrapy:** Install Scrapy using `pip install scrapy`.

## Usage

### Running ETSYScraper

To initiate the web scraping process and collect general product information, use the following command:

```bash
scrapy crawl ETSYScraper
