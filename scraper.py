import csv
import requests
from bs4 import BeautifulSoup


def scrape_page(soup, quotes):
    # Find all quote elements
    quote_elements = soup.find_all('div', class_='quote')

    for quote_element in quote_elements:
        # Extracting the text of the quote
        text = quote_element.find(
            'span',
            class_='text'
        ).text

        # Extracting the author of the quote
        author = quote_element.find(
            'small',
            class_='author'
        ).text

        # Extracting the tag <a> HTML elements related to the quote
        tag_elements = quote_element.find(
            'div',
            class_='tags'
        ).find_all('a', class_='tag')

        # Storing the list of tag strings in a list
        tags = []
        for tag_element in tag_elements:
            tags.append(tag_element.text)

        # Appending a dictionary containing the quote data
        quotes.append(
            {
                'text': text,
                'author': author,
                'tags': ', '.join(tags)  # Merging the tags into a "A, B, ..., Z" string
            }
        )


# The URL of the home page of the target website
base_url = 'https://quotes.toscrape.com'

# Defining the User-Agent header to use in the GET request below
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}

# Retrieving the target web page
page = requests.get(base_url, headers=headers)

# Parsing the target web page with Beautiful Soup
soup = BeautifulSoup(page.text, 'html.parser')

# Initializing the variable that will contain the list of all quote data
quotes = []

# Scraping the home page
scrape_page(soup, quotes)

# Getting the "Next →" HTML element
next_li_element = soup.find('li', class_='next')

# If there is a next page to scrape
while next_li_element is not None:
    next_page_relative_url = next_li_element.find('a', href=True)['href']

    # Getting the new page
    page = requests.get(base_url + next_page_relative_url, headers=headers)

    # Parsing the new page
    soup = BeautifulSoup(page.text, 'html.parser')

    # Scraping the new page
    scrape_page(soup, quotes)

    # Looking for the "Next →" HTML element in the new page
    next_li_element = soup.find('li', class_='next')

# Open the "quotes.csv" file and create it if not present
with open('quotes.csv', 'w', encoding='utf-8', newline='') as csv_file:
    # Initializing the writer object to insert data into the CSV file
    writer = csv.writer(csv_file)

    # Writing the header of the CSV file
    writer.writerow(['Text', 'Author', 'Tags'])

    # Writing each row of the CSV
    for quote in quotes:
        writer.writerow(quote.values())

print("Quotes have been scraped and saved to 'quotes.csv'.")
