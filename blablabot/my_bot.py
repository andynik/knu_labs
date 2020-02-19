from discord.ext import commands
import os
from google.cloud import vision
import pandas as pd
import random
import dialogflow_v2 as dialogflow
from google.api_core.exceptions import InvalidArgument



def image_text_rec(url):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"VisionAPI_Token.json"

    client = vision.ImageAnnotatorClient()

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


def faq(question):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"DialogflowAPI_Token.json"
    session_client = dialogflow.SessionsClient()

    DIALOGFLOW_PROJECT_ID = 'blablabot-268010'
    DIALOGFLOW_LANGUAGE_CODE = 'en'
    SESSION_ID = 'current-user-id'

    text_to_be_analyzed = question

    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.types.TextInput(text=text_to_be_analyzed, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)

    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
        raise

    print("Query text:", response.query_result.query_text)
    print("Detected intent:", response.query_result.intent.display_name)
    print("Detected intent confidence:", response.query_result.intent_detection_confidence)
    print("Fulfillment text:", response.query_result.fulfillment_text)

    return response.query_result.fulfillment_text

bot = commands.Bot(command_prefix = '.')

profile_info = {}

@bot.event
async def on_message(message):
    def is_correct(m):
        return m.author == message.author

    if message.author.id == 677077194870226944: # your bot's id
        return

    if message.content == "hello":
        await message.channel.send("Hello {0.author.mention} ".format(message))

    elif 'profile' in message.content:
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

    elif 'faq' in message.content:
        cnt = 0
        while True:
            if not cnt:
                await message.channel.send("OK. Ask me something about Google Compute Engine. I will help you!")
            else:
                await message.channel.send("Anything else?")

            ans = await bot.wait_for('message', check=is_correct)
            resp = faq(ans.content)

            if 'enough' in ans.content:
                await message.channel.send("Alright then")
                break
            else:
                await message.channel.send(resp)

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
