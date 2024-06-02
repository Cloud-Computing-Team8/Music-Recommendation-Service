# Music-Recommendation-Service

A music recommendation service using facial expression recognition.

# Chat GPT 코드 사용법

1. 동일한 폴더에 .env 파일을 만든다.
2. 내용에 아래 정보를 추가한다.
   OPEN_API_KEY = {본인이 Open AI 에서 발급받은 API KEY}

3. detected_emotion 변수에는 AWS Rekognition 에서 전달받은 감정 값을 넣는다.
4. title, artist, youtube_lick 변수를 활용하여 Web page를 구성한다.
