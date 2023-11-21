import sys 
import json
import requests
import multiprocessing
from configparser import ConfigParser
from crawling import crawling

config = ConfigParser()
config.read('/Users/kimsunjung/Desktop/dev/dataGeneration/config.ini')
config.sections()
REST_API_KEY = config['key']['rest_api_key']
KAKAO_URL = config['url']['kakao_kogpt_url']
TRAIN_DATA_DICT = dict()

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
    if keyword in TRAIN_DATA_DICT.keys():
        print(keyword)
        TRAIN_DATA_DICT[keyword].append(response['generations'][0]['text'].split("\n")[0])
    else: 
        TRAIN_DATA_DICT[keyword] = list(response['generations'][0]['text'].split("\n")[0])
    return response['generations'][0]['text'].split("\n")[0]

def run_by_batch():
    # 총 239, 400번 호출 
    # 프로세스 4개로 병렬처리 -> 47, 880번
    sys.setrecursionlimit(239400)
    sym_lists = crawling()
    print("++++++++crawling done++++++++")
    with multiprocessing.Pool(4) as process:
       result = process.map(call_kogpt, sym_lists)
       print(list(result))  
    return TRAIN_DATA_DICT

if __name__ == "__main__":
    # run_by_batch()
    print(call_kogpt('복통'))



# def get_keyword():
#     return crawling()

# print(call_kogpt('후두염'))
# {'id': 'dd98fdcc-9901-4cd1-9397-9c915c33d46f', 
# 'generations': [{'text': ' 목이 아프고, 목소리가 안나와요.\n\n                ', 'tokens': 20}], 'usage': {'prompt_tokens': 29, 'generated_tokens': 20, 'total_tokens': 49}}