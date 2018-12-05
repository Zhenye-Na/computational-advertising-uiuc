"""
HW4: Ads analysis.

@author: Zhenye Na
"""

import os
import json
import requests

from PIL import Image
from io import BytesIO

# read json file to python dictionary
json_file = open('../ads.json')
json_str = json_file.read()
json_data = json.loads(json_str)
ads = json_data["ads"]

# filter out ads containing keyword logo in their url
selected_ads = []
for visited_page_url, ad_urls in ads.items():
    # list of ads str
    if isinstance(ad_urls, list):
        for ad_url in ad_urls:
            if ad_url.find("logo") == -1:
                selected_ads.append(ad_url)
    # ads strs
    elif isinstance(ad_urls, str):
        if ad_url.find("logo") == -1:
            selected_ads.append(ad_url)

if not os.path.isdir('../imgs'):
    os.mkdir('../imgs')

# download images
for idx, url in enumerate(selected_ads):
    response = requests.get(url, stream=True)
    try:
        image = Image.open(BytesIO(response.content))
        width, height = image.size
        if width > 1 and height > 1:
            # images.append(image)
            image.save("{}th_ad.png".format(idx))
    except:
        continue