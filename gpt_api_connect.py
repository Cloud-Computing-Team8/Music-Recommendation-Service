from langchain.prompts import (
    ChatPromptTemplate, 
    SystemMessagePromptTemplate, 
    HumanMessagePromptTemplate,
)
from langchain.schema import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import re
import os
import random

# 예시로 사용할 감정 값 - 실제 구현시, AWS Rekognition을 통해 얻은 감정 값을 사용
detected_emotion = "HAPPY"
print(f"Detected Emotion: {detected_emotion}")

# 한정된 감정 단어로는 다양한 결과값을 구해낼 수 없음. 연상되는 단어 set을 만들어 random 으로 사용.

# Sad
sad_words = ["Sad", "Melancholy", "Sorrowful", "Heartbroken", "Tearful", "Mournful", "Depressed", "Grieving", "Dismal", "Forlorn", "Despondent"]
# Confused
confused_words = ["Confused", "Perplexed", "Baffled", "Bewildered", "Mystified", "Befuddled", "Flustered", "Disoriented", "Puzzled", "Confounded", "Discombobulated"]
# Disgusted
disgusted_words = ["Disgusted", "Revolted", "Repulsed", "Nauseated", "Appalled", "Sickened","Horrified", "Offended", "Grossed-out", "Contemptuous", "Abhorrent"]
# Angry
angry_words = ["Angry", "Furious", "Irate", "Enraged", "Incensed", "Livid", "Wrathful", "Indignant", "Infuriated", "Fuming", "Outraged"]
# Surprised
surprised_words = ["Surprised", "Astonished", "Amazed", "Stunned", "Shocked", "Startled", "Dumbfounded", "Bewildered", "Flabbergasted", "Speechless", "Gobsmacked"]
# Fear
fear_words = ["Fear", "Terrified", "Frightened", "Petrified", "Horrified", "Alarmed", "Apprehensive", "Uneasy", "Nervous", "Intimidated", "Dreadful"]
# Calm
calm_words = ["Calm", "Tranquil", "Serene", "Placid", "Peaceful", "Composed", "Relaxed", "Unperturbed", "Collected", "Unruffled", "Laid-back"]
# Happy
happy_words = ["Happy", "Joyful", "Elated", "Jubilant", "Cheerful", "Gleeful", "Delighted", "Ecstatic", "Overjoyed", "Content", "Blissful"]

if detected_emotion == "SAD": detected_emotion = random.choice(sad_words)
elif detected_emotion == "CONFUSED": detected_emotion = random.choice(confused_words)
elif detected_emotion == "DISGUSTED": detected_emotion = random.choice(disgusted_words)
elif detected_emotion == "ANGRY": detected_emotion = random.choice(angry_words)
elif detected_emotion == "SURPRISED": detected_emotion = random.choice(surprised_words)
elif detected_emotion == "FEAR": detected_emotion = random.choice(fear_words)
elif detected_emotion == "CALM": detected_emotion = random.choice(calm_words)
elif detected_emotion == "HAPPY": detected_emotion = random.choice(happy_words)

# 인식된 감정에 따라 ChatGPT를 통해 노래 추천

load_dotenv()
OPEN_API_KEY = os.environ.get("OPEN_API_KEY")
# temperature: 0.5 ~ 1.5 사이의 값으로 설정, 너무 높은 값을 넣으면 창조함.
model = ChatOpenAI(temperature=1.3, model="gpt-3.5-turbo", api_key=OPEN_API_KEY)

model_response = ""

messages = [
    SystemMessage(
        content="This API provides inspirational songs based on the requested mood."
    ), 
    HumanMessage(
        content=f"""Please provide an inspirational that fits my current mood. 
                You can suggest a song that I can find on YouTube. 
                Make sure to suggest a different song than what you might have recommended previously. 
                My current mood is {detected_emotion.lower()}.
                Please respond in the format: title: ~, artist: ~, YouTube link: ~."""
    ), 
]

# 모델에 메시지를 보내고 응답을 model_response 변수에 저장
model_response = model.invoke(messages)

# 모델의 응답을 출력
print(model_response)

content = str(model_response)

# 정규식을 사용하여 각 부분 추출
title_match = re.search(r'title:\s*["\']?(.*?)[\'"]?(?=,)', content)
artist_match = re.search(r'artist:\s*(.*?)(?=,)', content)
youtube_link_match = re.search(r'YouTube link:\s*(https?://[^\s]+)', content)

# 변수에 저장 및 이스케이프 문자 제거
title = title_match.group(1).replace("\\", "") if title_match else None
artist = artist_match.group(1).replace("\\", "") if artist_match else None
youtube_link = youtube_link_match.group(1) if youtube_link_match else None

# HAPPY : Brave, Sara Bareilles, https://www.youtube.com/watch?v=QUQsqBqxoR4
# SAD : Fight Song, Rachel Platten, https://www.youtube.com/watch?v=xo1VInw-SKc
# COMFUSED : The Climb, Miley Cyrus, https://www.youtube.com/watch?v=NG2zyeVRcbs
# DISGUSTED : Roar, Katy Perry, https://www.youtube.com/watch?v=CevxZvSJLk8
# ANGRY : Titanium, David Guetta, https://www.youtube.com/watch?v=JRfuAukYTKg
# SURPRISED : Stronger, Kelly Clarkson, https://www.youtube.com/watch?v=Xn676-fLq7I
# FEAR : Count on Me, Bruno Mars, https://www.youtube.com/watch?v=6k8cpUkKK4c
# CALM : A Thousand Years, Christina Perri, https://www.youtube.com/watch?v=rtOvBOTyX00

# 감정에 따라 추천된 노래가 없을 경우, 감정에 따라 미리 정해둔 노래 추천

if (title == None) & (artist == None) & (youtube_link == None) :
    if detected_emotion == "SAD": 
        title = "Fight Song"
        artist = "Rachel Platten"
        youtube_link = "https://www.youtube.com/watch?v=xo1VInw-SKc"
    elif detected_emotion == "CONFUSED": 
        title = "The Climb"
        artist = "Miley Cyrus"
        youtube_link = "https://www.youtube.com/watch?v=NG2zyeVRcbs"
    elif detected_emotion == "DISGUSTED": 
        title = "Roar"
        artist = "Katy Perry"
        youtube_link = "https://www.youtube.com/watch?v=CevxZvSJLk8"
    elif detected_emotion == "ANGRY": 
        title = "Titanium"
        artist = "David Guetta"
        youtube_link = "https://www.youtube.com/watch?v=JRfuAukYTKg"
    elif detected_emotion == "SURPRISED": 
        title = "Stronger"
        artist = "Kelly Clarkson"
        youtube_link = "https://www.youtube.com/watch?v=Xn676-fLq7I"
    elif detected_emotion == "FEAR": 
        title = "Count on Me"
        artist = "Bruno Mars"
        youtube_link = "https://www.youtube.com/watch?v=6k8cpUkKK4c"
    elif detected_emotion == "CALM": 
        title = "A Thousand Years"
        artist = "Christina Perri"
        youtube_link = "https://www.youtube.com/watch?v=rtOvBOTyX00"
    elif detected_emotion == "HAPPY":
        title = "Brave"
        artist = "Sara Bareilles"
        youtube_link = "https://www.youtube.com/watch?v=QUQsqBqxoR4"


# 결과 출력
print(f'Title: {title}')
print(f'Artist: {artist}')
print(f'YouTube Link: {youtube_link}')