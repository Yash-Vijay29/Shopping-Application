import cv2
import numpy as np
import os
from .Colors import Dominant_Color, sort_colors_by_distance  # Import your Dominant_Color function and sorting function
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'
}

def download_and_sort_products(products,target):
    sorted_products = []

    dominant_colors_array = []  # Array to store dominant colors in order

    for product in products:
        img_url = product.get('img_url')
        if img_url:
            # Download image and save locally
            try:
                image_name = f"product_{products.index(product)}.png"  # Generate a unique filename
                image_path = f"downloads/{image_name}"  # Path where images will be saved
                response = requests.get(img_url, stream=True, headers=headers)
                if response.status_code == 200:
                    with open(image_path, 'wb') as f:
                        f.write(response.content)

                    # Find dominant color of the image
                    dominant_color = Dominant_Color(image_path)

                    # Add dominant color to array
                    dominant_colors_array.append(dominant_color)

                    # Clean up: Delete the downloaded image
                    os.remove(image_path)

                    # Add dominant color to product dictionary
                    product['dominant_color'] = dominant_color

                    # Append product to sorted list
                    sorted_products.append(product)

                else:
                    print(f"Failed to download image from {img_url}")
                    # Assign 'None' to dominant_color for this product
                    product['dominant_color'] = None
                    dominant_colors_array.append(None)

            except Exception as e:
                print(f"Error processing image: {e}")
                # Assign 'None' to dominant_color for this product
                product['dominant_color'] = None
                dominant_colors_array.append(None)

        else:
            # Assign 'None' to dominant_color for products without img_url
            product['dominant_color'] = None
            dominant_colors_array.append(None)
    
    # Sort dominant colors array by distance
    sorted_dominant_colors = sort_colors_by_distance(target, dominant_colors_array)

    # Rearrange products based on sorted dominant colors
    sorted_products_by_color = []
    for color in sorted_dominant_colors:
        for product in sorted_products:
            if product.get('dominant_color') == color:
                sorted_products_by_color.append(product)
                break

    return sorted_products_by_color

