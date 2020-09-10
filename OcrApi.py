# -*- coding: utf-8 -*- 
import os
import sys
import requests
# If you are using a Jupyter notebook, uncomment the following line.
# %matplotlib inline
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image
from io import BytesIO
import io
import logging
import config


def fetchApi(image_name):
    pid = os.getpid()
    logging.basicConfig(filename='./logs/ocr_api.log',level=logging.DEBUG)
    logging.info('=== start ocrApi ===')

    subscription_key = config.subscription_key
    endpoint = "https://optical-character-recognition.cognitiveservices.azure.com/"

    ocr_url = endpoint + "vision/v3.0/ocr"

    params = {'language': 'ja', 'detectOrientation': 'true'}

    
    path = "/home/azureuser/fukuNode/"
    image_path = path + image_name
    # Read the image into a byte array
    image_data = open(image_path, "rb").read()
    # Set Content-Type to octet-stream
    headers = {'Ocp-Apim-Subscription-Key': subscription_key, 'Content-Type': 'application/octet-stream'}
    # put the byte array into your post request
    response = requests.post(ocr_url, headers=headers, params=params, data = image_data)

    response.raise_for_status()

    analysis = response.json()

    # Extract the word bounding boxes and text.
    line_infos = [region["lines"] for region in analysis["regions"]]
    # print("===line_infos=== : ",line_infos)

    word_infos = []
    tmp = "/home/azureuser/fuku/ocrApi/work/text."
    text = tmp + str(pid)
    f = open(text, "w")
    for line in line_infos:
        for word_metadata in line:
            for word_info in word_metadata["words"]:

                # print(word_info["text"])
                f.write(word_info["text"])

    f.close()
    f = open(text, "r")
    tmp = f.read()
    logging.info(tmp)
    with open(text) as f:
        fuku = '福島'
        if fuku in f.read():
            # print(fuku)
            logging.info('Fukishima exist')
            print(True)
            return True
        else:
            print(False)
            logging.info('Fukishima doesn\'t exist')
            return False

if __name__ == "__main__":
    fetchApi(sys.argv[1])
