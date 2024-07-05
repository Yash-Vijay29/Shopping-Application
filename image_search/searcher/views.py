from django.shortcuts import render
from .forms import UploadImageForm,TextInputer
from PIL import Image
from .Colors import Dominant_Color
import cv2
import numpy as np
from .Object_Classifier import classify
from .Scraper import scrape_amazon_product,scrape_info
from .Sorter import download_and_sort_products
from .summarizer import summarize_product_info
def homepage(request):
    if request.method == "POST":
        form = UploadImageForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = request.FILES['image']
            image = Image.open(image_file)
            image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            cv2.imwrite("temp/stored_picture.png",image_cv)
            dom_col = Dominant_Color("temp/stored_picture.png")
            text = classify()
            if text == None:
               form = TextInputer
               return render(request,"htmls/DetectionFailed.html")
            products = scrape_amazon_product(text)
            sorted_products = download_and_sort_products(products,dom_col)
            return render(request, 'htmls/products.html', {'products': sorted_products})
    else:
     form = UploadImageForm()
     return render(request, "htmls/homepage.html", {'form': form})
def manualsearch(request):
   if request.method == "POST":
      form = TextInputer(request.POST)
      if form.is_valid():
         text = request.POST.get('text')
         products = scrape_amazon_product(text)
def details(request,product_url):
    product_info = scrape_info(product_url)
    summarized_info = summarize_product_info(product_info)
    
    context = {
        'product_info': summarized_info
    }
    
    return render(request, 'htmls/Description.html', context)
# Create your views here.
