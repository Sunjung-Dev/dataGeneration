import requests
import json
from configparser import ConfigParser

config = ConfigParser()
config.read('/Users/kimsunjung/Desktop/dev/dataGeneration/config.ini')
config.sections()
REST_API_KEY = config['key']['rest_api_key']
KAKAO_URL = config['url']['kakao_kogpt_url']

def kogpt_api(prompt, max_tokens = 1, temperature = 1.0, top_p = 1.0, n = 1):
    r = requests.post(
        KAKAO_URL,
        json = {
            'prompt': prompt,
            'max_tokens': max_tokens,
            'temperature': temperature,
            'top_p': top_p,
            'n': n
        },
        headers = {
            'Authorization': 'KakaoAK ' + REST_API_KEY,
            'Content-Type': 'application/json'
        }
    )
    response = json.loads(r.content)
    return response

def call_kogpt(keyword):
    prompt = '정보: ' + keyword + '''정보를 바탕으로 질문에 답하세요.
    Q: 어디가 아파서 오셨나요?
    A: '''
    response = kogpt_api(prompt, max_tokens=20, temperature=0.3, top_p=0.85)
    print(response)


call_kogpt('목감기')