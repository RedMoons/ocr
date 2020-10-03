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
    endpoint = config.endpoint
    ocr_url = endpoint + "vision/v3.0/ocr"

    params = {'language': 'ja', 'detectOrientation': 'true'}

    path = "/home/azureuser/fukuNode/"
    image_path = path + image_name
    image_data = open(image_path, "rb").read()
    logging.info(image_path)

    headers = {'Ocp-Apim-Subscription-Key': subscription_key, 'Content-Type': 'application/octet-stream'}
    response = requests.post(ocr_url, headers=headers, params=params, data = image_data)
    # logging.info(response.text)
    response.raise_for_status()
    analysis = response.json()
    # Extract the word bounding boxes and text.
    line_infos = [region["lines"] for region in analysis["regions"]]
    # print("===line_infos=== : ",line_infos)
    logging.info('creating text')
    word_infos = []
    tmp = "/home/azureuser/fukuNode/work/"
    text = tmp + str(pid)
    logging.info(text)
    f = open(text, "w")
    for line in line_infos:
        for word_metadata in line:
            for word_info in word_metadata["words"]:

                # logging.info(word_info["text"])
                f.write(word_info["text"])

    f.close()
    # f = open(text, "r")
    # tmp = f.read()
    logging.info('checking text')
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
