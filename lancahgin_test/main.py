from langchain.chat_models import ChatOpenAI
import time
import concurrent
import json
# import os

# os.environ['OPENAI_API_KEY'] = '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'
# llm = ChatOpenAI(temperature=0,               # 창의성 (0.0 ~ 2.0) 
#                  max_tokens=100,             # 최대 토큰수
#                  model_name='gpt-3.5-turbo',  # 모델명
#                 )
# question = '허리통증 증상과 관련되서 말해봐'

# print(f'[답변]: {llm.predict(question)}')
# from langchain.prompts import PromptTemplate

# api_key = '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'
# my_template = """아래의 질문에 대해 한 줄로 간결하고 친절하게 답변하세요.
# 질문: {question}"""
# chat_model = ChatOpenAI(openai_api_key=api_key)
# prompt = PromptTemplate.from_template(my_template)
# prompt.format(question="코막힘에 대해서 설명해봐")
# print(chat_model.predict(prompt.format(question="감기 증상에 대해서 설명해봐")))


from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain
from langchain.schema import BaseOutputParser

api_key = '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'

class CommaSeparatedListOutputParser(BaseOutputParser):
    """LLM 아웃풋에 있는 ','를 분리해서 리턴하는 파서."""
    def parse(self, text: str):
        return text.split('.\n')

template = """
나는 지금 환자와 대화중이고 환자의 증상에 대해서 상담중이야 
환자의 증상에 대해서 설명해줘. 이외의 말은 하지마.
질문:"""

system_message_prompt = SystemMessagePromptTemplate.from_template(template)
human_template = "{text}"
human_message_prompt = HumanMessagePromptTemplate.from_template(human_template)

chat_prompt = ChatPromptTemplate.from_messages([system_message_prompt, human_message_prompt])

chain = LLMChain(
    llm=ChatOpenAI(openai_api_key = api_key),
    prompt=chat_prompt,
    output_parser=CommaSeparatedListOutputParser()
)

sym_data_dict = dict()
def make_sentence(keyword):
    start_time = time.time()
    result = chain.run(f"환자의 {keyword}증상에 대해 말해보세요 환자의 말투로 한문장씩 총 20개의 문장으로 말해줘")
    print(result, type(result))
    sym_data_dict[keyword] = result
    finish_time = time.time()
    print("end_time: ", finish_time - start_time)


if __name__ == "__main__":
    keyword = ['간성뇌증', '강박증', '건망증', '고산병', '광대뼈 위치 이상', '기민상태', '기억장애', '깨어나면 기억하지 못함', '납작한 코, 축 쳐진 귀', '낮 시간대의 졸음', '낮은 지능', '낮은 학업 성취', '내분비계이상', '놀란표정', '놀람반사의 약화', '뇌부종', '뇌수종', '뇌압상승증상', '뇌염증상', '뇌출혈', '달모양의 둥근 얼굴', '두부 외상', '두통', '두피 건조', '두피 열상', '만성 부비동염', '머리모양 변형', '모발 탈색', '모발이 가늘어짐', '모발이 거침', '무균성 뇌막염', '무의식', '박동성 통증', '방향감각 상실', '볼, 눈주위 움푹 꺼짐', '볼이 처짐', '비웃는 듯한 표정', '삐뚤어진 눈, 코, 입', '수막자극증상', '실인증', '실행증', '안면 변형', '안면마비', '안면부 출혈', '안면통', '안면홍조', '어지러움', '언어장애', '얼굴 중심선이 안맞음', '얼굴 한쪽의 반점', '얼굴모양변화', '얼굴부종', '얼굴에 땀이 남', '얼굴에 털이 자람', '얼굴의 나비모양 홍반', '얼굴이 밋밋함', '얼굴이 화끈거림', '얼굴형태의 이상', '운동 실어증', '원형, 타원형의 탈모', '의식 변화', '의식 저하', '이마가 넓어짐', '이마의 주름', '이중턱', '인지장애', '졸림', '지남력 장애', '짓누르는 느낌 ', '치매', '코 옆과 입꼬리 주름', '콧등이 넓어짐', '턱끝이 커보임', '턱의 통증', '편두통', '하악전돌', '학습장애', '혼돈', '혼수', '갑상선 비대', '갑상선이 단단해짐', '경부 강직', '경부 림프절병증', '경부 운동 제한', '경정맥 확장', '고음에서의 분열', '남성스러운 목소리', '덩어리가 만져짐', '목 뒷부분의 지방축적', '목 주변 부종', '목소리 변화', '목의 이물감', '목의 통증', '사경', '삼키기 곤란 ', '성대 이상', '성대마비', '성대부종', '음성피로', '이물감', '이중음성', '이하선비대', '인후염', '잦은 상기도 감염', '지속적인 애성', '코가 목뒤로 넘어감', '편도선 비대', '후두부종', '후두신경 마비', '후두염', '가래', '가슴 답답', '가슴 두근거림', '가슴 통증', '객혈', '거품이 섞인 가래', '검은색 가래', '겨드랑이 악취 ', '과호흡', '기침', '늑막삼출', '락스를 마셨어요', '무호흡', '반복되는 폐렴', '부정맥', '불규칙호흡', '빈맥', '빈호흡', '사래걸림', '새가슴', '서맥', '서호흡', '수면 무호흡', '숨막히는 느낌', '심근손상', '심방 부정맥', '심부전', '심실 부정맥', '심실세동', '심염', '심음 감소', '심인성 쇼크', '심잡음', '심정지', '염산, 황산을 마셨어요', '운동 시 호흡곤란', '울혈성 심부전', '잦은 딸꾹질', '저심박출량', '질식', '천명음', '천식', '청진시 휘파람 소리', '폐기능저하', '폐동맥 고혈압', '폐부종', '폐색전', '폐출혈', '함몰가슴', '헛기침', '호기의 증가', '호흡곤란', '호흡기감염', '화농성 객담', '흉곽 팽윤', '흉부압박감', '흉쇄 유돌근의 몽우리', '흉수', '가슴 쓰림', '간기능 저하', '간부전', '간비대', '공복감', '구토', '급성 신부전', '농신증', '담도감염', '담석', '덩어리가 만져짐', '만성 신부전', '명치 부위 통증', '무통증', '문맥성고혈압', '배꼽의 고름 및 피', '배꼽이 솟음', '복벽이 움푹 들어감', '복부 불편감', '복부 압박 증상', '복부 통증', '복부경련', '복부비만', '복부의 박동감', '복부팽만감', '복수', '분출성 구토', '비장비대', '산통', '소화불량', '손가락으로 밀면 들어감', '식후 불쾌감', '십이지장궤양', '아랫배가 뭉침', '악취', '안정 시 탈장 사라짐', '압통', '야뇨증', '양수의 감소', '옆구리 통증', '오심', '우하복부 통증', '위궤양', '위산의 역류', '위염', '위의 연동운동이 보임', '위장관 출혈', '위장관의 허혈', '임신 2, 3기의 오심', '임신 오조증', '잔변감', '장마비', '장폐색', '초록색 구토', '탈장', '탈장 돌출', '탈장 부위의 통증', '토혈', '트림', '포만감', '헛배', '흡수장애', '관절통', '굽은 등', '뼈의 기형', '요통', '자세이상', '척추 측만', '척추 후만', '척추와 허리 디스크', '괄약근 기능 이상', '달걀 위에 앉아있는 느낌', '대변에 벌레 관찰됨', '배변습관의 변화', '배변장애', '변비', '변실금', '설사', '악취가 나는 설사', '엉덩이 비대칭 주름', '엉덩이 통증', '점액변', '지방변', '치핵의 탈출', '항문 통증', '항문주위 염증', '항문출혈', '허리, 둔부 중심형 비만', '혈변', '회색변', '흑색변', '가늘어지는 팔다리', '관절 운동성 감소', '관절의 경직', '관절통', '다발성 관절염', '동정맥루 잡음 약화', '말초부종', '말초의 허혈', '무감각', '무맥', '반신마비', '방사통', '뼈의 변형', '사지 마비', '사지 변형', '사지 부종', '사지의 창백한 현상', '상지 마비', '손상 부위 출혈', '손상부위 촉각 소실', '압통', '어깨 움직임의 제한', '어깨 잡음', '어깨근육 약화', '어깨의 통증', '옷 액와 부분 변색', '저림', '파열부위 오목해짐', '팔의 길이가 달라짐', '팔의 통증', '편마비', '편측 사지의 감각소실', 'O자 다리', 'X자 다리', '가늘어지는 팔다리', '관절 불안정증', '관절 운동성 감소', '관절염', '관절의 경직', '관절잡음', '관절통', '다리 외상', '다리 통증', '다리가 잘 안 벌어짐', '다리변형', '다리의 길이가 틀림', '다발성 관절염', '말초부종', '말초의 허혈', '무감각', '무릎 부위 부종', '무릎 부위 통증', '무맥', '반신마비', '방사통', '보행이상', '비강,목,폐 건조', '뻣뻣함', '뼈의 기형', '뼈의 변형', '사지 마비', '사지 변형', '사지 부종', '사지의 창백한 현상', '손상 부위 출혈', '손상부위 촉각 소실', '압통', '양무릎사이 벌어짐', '양반다리로 앉기힘듬', '오리걸음', '저림', '정맥혈전', '좁은 보폭의 걸음걸이', '종아리 근육의 비대', '파열부위 오목해짐', '파열음', '파행', '편마비', '편측 사지의 감각소실', '하지 마비', '하지부종', '하지의 근력약화', '해파리에 쏘였어요']
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(make_sentence, keyword)
    file_path = '/Users/kimsunjung/Desktop/dev/dataGeneration/lancahgin_test/testData.json'
    with open(file_path, 'w') as outfile:
        outfile.write(str(sym_data_dict))
