# uses k cluster algorithm to find dominant color for reordering the recommended list
import cv2
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt 
from webcolors import hex_to_rgb
import numpy as np
def Dominant_Color(file):
    # Reading the store image, performing conversion from 3D to 2D
    image = cv2.imread(file)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pixels = image.reshape(-1,3)
    kmeans = KMeans(n_clusters=8,random_state=0).fit(pixels)
    dominant_colors = kmeans.cluster_centers_.astype(int)
    # Using WebColors for finding closest color
    color = dominant_colors[0]
    rgb_tuple = tuple(color)
    hex_color = '#{:02x}{:02x}{:02x}'.format(*rgb_tuple)
    return hex_color

def hex_color_distance(hex1, hex2):
    """
    Calculate the Euclidean distance between two colors in RGB space.
    """
    rgb1 = hex_to_rgb(hex1)
    rgb2 = hex_to_rgb(hex2)
    r_diff = (rgb1.red - rgb2.red) ** 2
    g_diff = (rgb1.green - rgb2.green) ** 2
    b_diff = (rgb1.blue - rgb2.blue) ** 2
    distance = (r_diff + g_diff + b_diff) ** 0.5
    return distance

def sort_colors_by_distance(target_color, color_array):
    """
    Sort an array of hex colors based on their distance from a target color.
    """
    distances = [(hex_color_distance(target_color, color), color) for color in color_array]
    sorted_colors = sorted(distances, key=lambda x: x[0])
    sorted_colors_hex = [color[1] for color in sorted_colors]
    return sorted_colors_hex


