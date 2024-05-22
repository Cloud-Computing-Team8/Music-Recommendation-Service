import boto3
import os

# AWS 사용자 자격 증명 설정
aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

if aws_access_key_id is None or aws_secret_access_key is None:
    print("AWS credentials not found in environment variables.")
else:
    print("AWS credentials found.")
    
# AWS 리전 설정
region_name = 'us-west-2'

# Rekognition 클라이언트 생성
rekognition = boto3.client(
    'rekognition',
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=region_name
)

script_dir = os.path.dirname(os.path.abspath(__file__))
image_relative_path = './test_images/sad.jpg'
image_path = os.path.join(script_dir, image_relative_path)

with open(image_path, 'rb') as image_file:
    image_bytes = image_file.read()

# 얼굴 감지 요청
response = rekognition.detect_faces(
    Image={'Bytes': image_bytes},
    Attributes=['ALL']  # 'ALL' 또는 'DEFAULT' 속성
)

# 결과 출력
for face_detail in response['FaceDetails']:
    print(f"Confidence: {face_detail['Confidence']}")
    print(f"Emotions: {face_detail['Emotions']}")
    print(f"Landmarks: {face_detail['Landmarks']}")
    print("--------")
