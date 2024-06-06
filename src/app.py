import os
import boto3
import random
import re
from flask import Flask, request, render_template, redirect, url_for
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from dotenv import load_dotenv

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

load_dotenv()
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
REGION_NAME = 'us-west-2'
OPEN_API_KEY = os.getenv('OPEN_API_KEY')

def get_youtube_video_id(youtube_link):
    video_id_match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11}).*', youtube_link)
    print(video_id_match)
    return video_id_match.group(1) if video_id_match else None

def analyze_emotion(image_path):
    rekognition = boto3.client(
        'rekognition',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=REGION_NAME
    )

    with open(image_path, 'rb') as image_file:
        image_bytes = image_file.read()

    response = rekognition.detect_faces(
        Image={'Bytes': image_bytes},
        Attributes=['ALL']
    )

    detected_emotion = response['FaceDetails'][0]['Emotions'][0]['Type']
    return detected_emotion

def recommend_song_based_on_emotion(detected_emotion):
    emotion_words = {
        "SAD": ["Sad", "Melancholy", "Sorrowful", "Heartbroken", "Tearful", "Mournful", "Depressed", "Grieving", "Dismal", "Forlorn", "Despondent"],
        "CONFUSED": ["Confused", "Perplexed", "Baffled", "Bewildered", "Mystified", "Befuddled", "Flustered", "Disoriented", "Puzzled", "Confounded", "Discombobulated"],
        "DISGUSTED": ["Disgusted", "Revolted", "Repulsed", "Nauseated", "Appalled", "Sickened","Horrified", "Offended", "Grossed-out", "Contemptuous", "Abhorrent"],
        "ANGRY": ["Angry", "Furious", "Irate", "Enraged", "Incensed", "Livid", "Wrathful", "Indignant", "Infuriated", "Fuming", "Outraged"],
        "SURPRISED": ["Surprised", "Astonished", "Amazed", "Stunned", "Shocked", "Startled", "Dumbfounded", "Bewildered", "Flabbergasted", "Speechless", "Gobsmacked"],
        "FEAR": ["Fear", "Terrified", "Frightened", "Petrified", "Horrified", "Alarmed", "Apprehensive", "Uneasy", "Nervous", "Intimidated", "Dreadful"],
        "CALM": ["Calm", "Tranquil", "Serene", "Placid", "Peaceful", "Composed", "Relaxed", "Unperturbed", "Collected", "Unruffled", "Laid-back"],
        "HAPPY": ["Happy", "Joyful", "Elated", "Jubilant", "Cheerful", "Gleeful", "Delighted", "Ecstatic", "Overjoyed", "Content", "Blissful"]
    }

    if detected_emotion in emotion_words:
        detected_emotion = random.choice(emotion_words[detected_emotion])

    model = ChatOpenAI(temperature=1.3, model="gpt-3.5-turbo", api_key=OPEN_API_KEY)

    messages = [
        SystemMessage(content="This API provides inspirational songs based on the requested mood."),
        HumanMessage(content=f"""Please provide an inspirational song that fits my current mood. 
                    You can suggest a song that I can find on YouTube. 
                    Make sure to suggest a different song than what you might have recommended previously. 
                    My current mood is {detected_emotion.lower()}.
                    Please respond in the format: title: ~, artist: ~, YouTube link: ~.""")
    ]

    model_response = model.invoke(messages)
    content = str(model_response)

    title_match = re.search(r'title:\s*["\']?(.*?)[\'"]?(?=,)', content)
    artist_match = re.search(r'artist:\s*(.*?)(?=,)', content)
    youtube_link_match = re.search(r'YouTube link:\s*(https?://[^\s]+)', content)

    title = title_match.group(1).replace("\\", "") if title_match else None
    artist = artist_match.group(1).replace("\\", "") if artist_match else None
    youtube_link = youtube_link_match.group(1) if youtube_link_match else None
    youtube_video_id = get_youtube_video_id(youtube_link) if youtube_link else None

    if (title == None) | (artist == None) | (youtube_link == None):
        if detected_emotion == "Sad": 
            title = "Fight Song"
            artist = "Rachel Platten"
            youtube_link = "https://www.youtube.com/watch?v=xo1VInw-SKc"
        elif detected_emotion == "Confused": 
            title = "The Climb"
            artist = "Miley Cyrus"
            youtube_link = "https://www.youtube.com/watch?v=NG2zyeVRcbs"
        elif detected_emotion == "Disgusted": 
            title = "Roar"
            artist = "Katy Perry"
            youtube_link = "https://www.youtube.com/watch?v=CevxZvSJLk8"
        elif detected_emotion == "Angry": 
            title = "Titanium"
            artist = "David Guetta"
            youtube_link = "https://www.youtube.com/watch?v=JRfuAukYTKg"
        elif detected_emotion == "Surprised": 
            title = "Stronger"
            artist = "Kelly Clarkson"
            youtube_link = "https://www.youtube.com/watch?v=Xn676-fLq7I"
        elif detected_emotion == "Fear": 
            title = "Count on Me"
            artist = "Bruno Mars"
            youtube_link = "https://www.youtube.com/watch?v=6k8cpUkKK4c"
        elif detected_emotion == "Calm": 
            title = "A Thousand Years"
            artist = "Christina Perri"
            youtube_link = "https://www.youtube.com/watch?v=rtOvBOTyX00"
        elif detected_emotion == "Happy":
            title = "Brave"
            artist = "Sara Bareilles"
            youtube_link = "https://www.youtube.com/watch?v=QUQsqBqxoR4"
        youtube_video_id = get_youtube_video_id(youtube_link)
    return title, artist, youtube_link, youtube_video_id

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            detected_emotion = analyze_emotion(file_path)
            title, artist, youtube_link, youtube_video_id = recommend_song_based_on_emotion(detected_emotion)
            return render_template('result.html', emotion=detected_emotion, title=title, artist=artist, youtube_link=youtube_link, youtube_video_id=youtube_video_id)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
