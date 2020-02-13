# Google Vision API sample (no need to use it with my_bot.py)

import os, io
from google.cloud import vision
import pandas as pd

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"ServiceAccountToken.json"

client = vision.ImageAnnotatorClient()

# FILE_NAME = 'test2.jpg'
# FOLDER_PATH = r'D:\Documents\Proga\KNU\sem_12\blablabot\images'
#
# with io.open(os.path.join(FOLDER_PATH, FILE_NAME), 'rb') as image_file:
#     content = image_file.read()
#
# image = vision.types.Image(content=content)
# response = client.text_detection(image=image)
# texts = response.text_annotations


image = vision.types.Image()
image.source.image_uri = "https://media.discordapp.net/attachments/677076812286656514/677209361747279917/test1.jpg"
response = client.text_detection(image=image)
texts = response.text_annotations


df = pd.DataFrame(columns=['locale', 'description'])
for text in texts:
    df = df.append(
        dict(
            locale=text.locale,
            description=text.description
        ),
        ignore_index=True
    )

print(df)
