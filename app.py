import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{}'

# Number of pages to scrape (in this case, 20 pages)
num_pages = 20

# Maximum number of rows to scrape (200 in this case)
max_rows = 200

# Create a CSV file and write the header
csv_file = open('scraped_data.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(csv_file)
writer.writerow(['URL', 'Name', 'Price', 'Rating', 'Number of Reviews', 'ASIN'])

# Counter variable for tracking the number of scraped rows
scraped_rows = 0

for page in range(1, num_pages + 1):
    # Make a GET request to the URL of each page
    response = requests.get(url.format(page))
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all product containers on the page
    product_containers = soup.find_all('div', {'data-component-type': 's-search-result'})
    
    # Iterate over each product container
    for container in product_containers:
        # Extract the product URL
        product_url = container.find('a', class_='a-link-normal s-no-outline').get('href')
        product_url = 'https://www.amazon.in' + product_url
        
        # Extract the ASIN from the product URL
        asin = product_url.split('/')[-1].split('?')[0]
        
        
        # Extract the product name
        product_name = container.find('span', class_='a-size-medium a-color-base a-text-normal').text.strip()
        
        # Extract the product price
        product_price = container.find('span', class_='a-offscreen').text
        
        # Extract the rating (if available)
        rating = container.find('span', class_='a-icon-alt')
        if rating:
            rating = rating.text.split()[0]
        else:
            rating = 'N/A'
        
        # Extract the number of reviews (if available)
        num_reviews = container.find('span', {'class': 'a-size-base', 'dir': 'auto'})
        if num_reviews:
            num_reviews = num_reviews.text
        else:
            num_reviews = '0'
        
        # Write the scraped information to the CSV file
        writer.writerow([product_url, product_name, product_price, rating, num_reviews, asin])
        
        # Increment the counter variable
        scraped_rows += 1
        
        # Check if the maximum number of rows has been reached
        if scraped_rows == max_rows:
            break
    
    # Check if the maximum number of rows has been reached
    if scraped_rows == max_rows:
        break

# Close the CSV file
csv_file.close()

# Read the CSV file and display the data
df = pd.read_csv('scraped_data.csv')
print(df)
