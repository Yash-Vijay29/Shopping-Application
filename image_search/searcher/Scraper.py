# Import necessary modules
from bs4 import BeautifulSoup
import requests
from .models import Product,Info  # Import your Django model
import random

def get_random_user_agent():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Mozilla/5.0 (Windows; U; Windows NT 6.0; x64; en-US) AppleWebKit/535.28 (KHTML, like Gecko) Chrome/55.0.1022.386 Safari/603.0 Edge/16.97716',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_8) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/52.0.2384.228 Safari/601',
        'Mozilla/5.0 (Windows NT 10.4; Win64; x64; en-US) AppleWebKit/601.6 (KHTML, like Gecko) Chrome/48.0.1003.132 Safari/536',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 7_4_1; en-US) AppleWebKit/537.37 (KHTML, like Gecko) Chrome/51.0.2682.185 Safari/533',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 7_0_9; en-US) AppleWebKit/537.25 (KHTML, like Gecko) Chrome/49.0.1803.279 Safari/602',
        'Mozilla/5.0 (Linux; Linux i680 ; en-US) AppleWebKit/603.18 (KHTML, like Gecko) Chrome/48.0.3070.105 Safari/602',
        # Add more user agents as needed
    ]
    return random.choice(user_agents)

def scrape_amazon_product(text):
    url = f'https://www.amazon.com/s?k={text}'
    headers = {
        'User-Agent': get_random_user_agent(),
        'Accept-Language': 'en-US, en;q=0.5'
    }
    response = requests.get(url, headers=headers)
    print(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    print(response)
    products = []
    results = soup.find_all('div', {'data-component-type': 's-search-result'})

    for result in results:
        try:
            # Extract product name
            name_tag = result.find('span', {'class': 'a-size-base-plus a-color-base a-text-normal'})
            product_name = name_tag.text.strip() if name_tag else None
            print("Product Name:", product_name)

            # Extract product image URL
            img_tag = result.find('img', {'class': 's-image'})
            img_url = img_tag['src'] if img_tag else None
            print("Image URL:", img_url)

            # Extract product page URL
            link_tag = result.find('a', {'class': 'a-link-normal'})
            product_url = 'https://www.amazon.com' + link_tag['href'] if link_tag else None
            print("Product URL:", product_url)

            # Extract product rating
            rating_tag = result.find('span', {'class': 'a-icon-alt'})
            rating = rating_tag.text if rating_tag else None
            print("Rating:", rating)

            # Extract product price
            price_tag = result.find('span', {'class': 'a-price'})
            price = price_tag.find('span', {'class': 'a-offscreen'}).text if price_tag else None
            print("Price:", price)

            # Create or update a Product instance in the database
            product_obj, created = Product.objects.update_or_create(
                product_url=product_url,
                defaults={
                    'name': product_name,
                    'img_url': img_url,
                    'rating': rating,
                    'price': price
                }
            )

            products.append({
                'name': product_name,
                'img_url': img_url,
                'product_url': product_url,
                'rating': rating,
                'price': price,
                'dominant_color': ''
            })

        except Exception as e:
            print(f"Error scraping product: {e}")

    print("Final Products List:", products)
    return products
def scrape_info(link):
    headers = {
        'User-Agent': get_random_user_agent(),
        'Accept-Language': 'en-US, en;q=0.5'
    }
    response = requests.get(link, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the title
    title = soup.find(id='productTitle')
    title = title.get_text(strip=True) if title else 'N/A'
    
    # Extract the price
    price = soup.find('span', {'id': 'priceblock_ourprice'})
    if not price:
        price = soup.find('span', {'id': 'priceblock_dealprice'})
    price = price.get_text(strip=True) if price else 'N/A'

    # Extract the image URL
    image = soup.find(id='imgTagWrapperId').img
    image_url = image['src'] if image else 'N/A'

    # Extract reviews
    reviews = soup.find_all('span', {'data-hook': 'review-body'})
    reviews_content = [review.get_text(strip=True) for review in reviews[:5]]  # Get first 5 reviews

    # Return the information
    information = {
        'name': title,
        'img_url': image_url,
        'reviews': reviews_content,
        'price': price
    }

    # Create or update a Product instance in the database
    info_obj, created = Info.objects.update_or_create(
        name=title,
        defaults={
            'img_url': image_url,
            'price': price,
            'reviews': " | ".join(reviews_content)
        }
    )

    return information