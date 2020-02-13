from discord.ext import commands
import os, io
from google.cloud import vision
import pandas as pd
import random


def image_text_rec(url):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"ServiceAccountToken.json"

    client = vision.ImageAnnotatorClient()

    # FILE_NAME = 'test1.jpg'
    # FOLDER_PATH = r'D:\Documents\Proga\KNU\sem_12\blablabot\images'
    # with io.open(os.path.join(FOLDER_PATH, FILE_NAME), 'rb') as image_file:
    #     content = image_file.read()
    # image = vision.types.Image(content=content)
    # response = client.text_detection(image=image)

    image = vision.types.Image()
    image.source.image_uri = url
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

    return df

bot = commands.Bot(command_prefix = '.')

profile_info = {}

@bot.event
async def on_message(message):
    def is_correct(m):
        return m.author == message.author

    if message.author.id == 677077194870226944: #your bot's id
        return

    if message.content == "hello":
        await message.channel.send("Hello {0.author.mention} ".format(message))

    elif 'talk' in message.content:
        await message.channel.send("Cool! Tell me more about you")

        for info in ['name', 'sex', 'age', 'city']:
            await message.channel.send("What is your " + info + '?')
            ans = await bot.wait_for('message', check=is_correct)
            if 'stop' in ans.content:
                break
            profile_info[info] = list(ans.content.split())[-1]
            await message.channel.send(random.choice(['OK, got it', 'Alrigrt', 'Great!']))
        await message.channel.send('Now I know you!')
        # print(profile_info)


    elif 'about' in message.content:
        cnt = 0
        while True:
            if not cnt:
                await message.channel.send("Cool! What you wanna know about you?")
            else:
                await message.channel.send("Something more?")

            ans = await bot.wait_for('message', check=is_correct)

            about = None
            if 'name' in ans.content:
                about = 'name'
            elif 'age' in ans.content:
                about = 'age'
            elif 'sex' in ans.content:
                about = 'sex'
            elif 'city' in ans.content:
                about = 'city'
            elif 'enough' in ans.content:
                await message.channel.send("Alright then")
                break

            await message.channel.send(profile_info[about])
            cnt += 1

    elif message.attachments:
        await message.channel.send("It's an image! Let me find out what is written there! :)")
        url = message.attachments[0].url
        url = 'https://media.discordapp.net/attachments' + url[38:]
        await message.channel.send(url)
        await message.channel.send("\nWait a bit...")
        text = image_text_rec(url)

        await message.channel.send(' '.join(list(str(text.iat[0, 1]).split('\n'))))


bot.run('your_token')