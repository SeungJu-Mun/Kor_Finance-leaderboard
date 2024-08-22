import streamlit as st
import pandas as pd
import openai
import os
import datetime
import base64
import requests
import json
import re
import glob

# 페이지 설정
title = "🤗 AICOSS 산학연계 해커톤 - 생성형 AI를 활용한 금융 상담 Chat-Bot 개발"
st.set_page_config(
    page_title=title,
    page_icon="🤗",
    layout="wide",
)

# Load the API key from Streamlit secrets
try:
    github_token = st.secrets['GITHUB_TOKEN']
except KeyError:
    st.error("GITHUB_TOKEN 환경 변수가 설정되지 않았습니다. 'Manage app'에서 환경 변수를 설정하세요.")

def upload_to_github(token, repo, path, content):
    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    headers = {
        "Authorization": f"token {token}",
        "Content-Type": "application/json"
    }
    
    # 먼저 파일의 sha 값을 가져오기 위해 GET 요청을 보냅니다.
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        sha = response.json().get('sha')
    else:
        sha = None

    data = {
        "message": "Add inference result",
        "content": base64.b64encode(content.encode()).decode()
    }
    if sha:
        data["sha"] = sha

    # 파일을 업데이트하기 위해 PUT 요청을 보냅니다.
    response = requests.put(url, headers=headers, json=data)
    if response.status_code == 201:
        st.success("평가 완료")
    elif response.status_code == 200:
        st.success("파일이 성공적으로 업데이트되었습니다")
    else:
        st.error(f"평가 실패: {response.status_code} - {response.json().get('message', 'Unknown error')}")
        st.error(response.json())  # 추가적으로 전체 응답 내용을 출력하여 디버깅에 도움

def setup_basic():
    url = 'https://personaai.co.kr/main'
    st.title(title)

   # 추가 서브제목
    st.subheader("🏆 Open-Ko-Finance-LLM-Leaderboard")

    st.markdown(
        "🚀 Open-Ko-Finance-LLM 리더보드는 한국어 금융 분야의 전문적인 지식을 대형 언어 모델로 객관적인 평가를 수행합니다.\n"
    )
    st.markdown( f" 이 리더보드는 [(주)페르소나에이아이](https://personaai.co.kr/main)에서 운영합니다.")

def setup_about():
    css = '''
    <style>
        .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size:1.5rem;
    </style>
    <style>
    .stButton button {
        font-size: 20px;
        padding: 10px 783px;
        background : linear-gradient(to right, #F2F3F4, #F5F6F7)
        
    }
    .stButton button:hover {
        background: linear-gradient(to right, #DEE1E3, #F2F3F4);
    }
    </style>
    '''

    st.markdown(css, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📖 About", "🚀Submit here!", "🏅 LLM BenchMark"])
    with tab1:
        st.markdown('<h3>주제 개요</h3>', unsafe_allow_html=True)
        st.markdown('최근 인공지능(AI) 기술의 발전은 다양한 산업 분야에 걸쳐 혁신적인 변화를 가져오고 있습니다.')
        st.markdown('특히, 생성형 AI 기술의 도입은 자연어 처리(NLP)와 관련된 애플리케이션 개발에 큰 영향을 미치고 있는데,')
        st.markdown('금융 상담 서비스 분야에서도 AI를 활용한 자동화된 상담 시스템은 비용 절감과 서비스 효율성 향상을 목표로 활발히 연구되고 있습니다.')
        st.markdown('이러한 배경 속에서 생성형 AI를 활용한 금융 상담 Chat-Bot 개발을 통해 대규모 언어 모델(LLM) 최적화와 금융 서비스의 사용자 경험을 개선하는 것을 목적으로 합니다.')
        st.write('')
        st.markdown('<h5>평가 방식</h5>', unsafe_allow_html=True)
        st.markdown('📈 우리는 [LogicKor](https://github.com/instructkr/LogicKor) 다분야 사고력 추론 벤치마크를 활용하여 금융 도메인에 LLM 모델을 테스트하는 통합 프레임워크를 통해 모델을 평가합니다. ')
        st.markdown('한국어로 번역한 데이터 세트와 한국어 웹 코퍼스를 수집하여, 3가지 작업(FIQUSA, MMLU_F, MATHQA)를 구축하여 새로운 데이터 세트를 처음부터 준비했습니다.')
        st.markdown('LLM 시대에 걸맞은 평가를 제공하기 위해 해당 벤치마크를 채택하였고, 최종 점수는 각 평가 데이터 세트에서 얻은 평균 점수로 변환됩니다.')
        st.write('')
        st.markdown('<h5>평가 기준 설명</h5>', unsafe_allow_html=True)
        st.markdown('1️⃣ FIQUSA : 금융 도메인 뉴스 헤드라인의 감성을 예측하여 시장 동향을 파악하는 벤치마크 입니다.')
        st.markdown('2️⃣ MMLU_F : 금융 관련 도메인을 정확하게 이해하고 있는지, 객관식 형태로 평가하는 벤치마크 입니다.')
        st.markdown('3️⃣ MATHQA : 리스크 관리, 옵션 가격 모델링 등 금융 분야에서 사용되는 수리적 문제를 잘 해결하는지 평가하는 벤치마크 입니다.')
        st.write('')
        st.markdown('<h5>관련 문의사항</h5>', unsafe_allow_html=True)
        st.markdown('평가 예시 데이터셋과 Chatgpt 사용 관련 문의 사항이 있으시면 anstmdwn45@personaai.co.kr로 연락주세요 🤩')
        st.markdown('Made with ❤️ by the awesome open-source community from all over 🌍')
        st.write('')
        st.write('')
        st.write('')

    with tab2:
        code2 = '''
# 1. 필요한 라이브러리 업로드
import openai

# 2. 환경변수 설정 (gpt-api key 설정)
client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "API_KEY 입력"))

# 3. 모델 추론수행
messages = [
    {"role": "system", "content": 'You are an AI assistant. You will be given a task. You must generate a detailed and long answer.'},
    {"role": "user", "content": str(question)}
    ]

response = client.chat.completions.create(
    model=selected_option,
    messages=messages,
    max_tokens=4096) # 최대 4k 

result = response.choices[0].message.content

'''
        code = '''
# 1. 필요 개발환경 설치 (Colab, Jupyter)
!pip install openai

# 2. 필요한 라이브러리 업로드
import openai
import os

# 3. 환경변수 설정 (gpt-api key 설정)
openai.api_key = os.environ.get("OPENAI_API_KEY", "API_KEY 입력")

# 4. openai playground 학습 데이터 업로드
def data_loader(train_file):
    with open(train_file, 'rb') as train_ft:
        training_response = openai.File.create(file=train_ft, purpose='fine-tune')
        return training_response['id']

# 5. gpt-3.5-turbo 미세조정
def gpt_finetuning(training_file_id):
    response = openai.FineTuningJob.create(
        training_file=training_file_id,
        model="gpt-3.5-turbo",  # 여기서 사용할 모델명을 정확히 지정하세요
        suffix="Finance_팀이름",
        hyperparameters={
            "n_epochs": 3,  # 데이터 반복 횟수 / 주로 3~5로 설정
            "batch_size": 3,  # 한 번의 학습에 처리할 데이터 수
            "learning_rate_multiplier": 0.3  # 모델의 학습률: 경사하강법을 통해 모델이 손실함수를 최소화할 수 있는 방향을 설정
        })
    return response

# 예시 사용법
train_file = '데이터셋 경로'
training_file_id = data_loader(train_file)
finetuning_response = gpt_finetuning(training_file_id)

print(finetuning_response)
        '''
        data = [{"messages": [{"role": "system", "content": "당신은 유능한 AI 어시스턴트 입니다. 사용자의 질문에 대해 친절하게 답변해주세요."}, {"role": "user", "content": "다음 금융 헤드라인의 정서는 무엇인가요? 긍정, 부정, 중립 중 어느 쪽인가요?\n텍스트:미래에셋, '프리미엄 커버드콜 월배당 ETF' 5종 개인 누적 순매수 1조 넘어\n정답:"}, {"role": "assistant", "content": "헤드라인의 정서는 긍정입니다"}]}]
        st.markdown('<h3>Evaluation Queue for the 🚀 Open Ko-LLM Leaderboard</h3>', unsafe_allow_html=True)
        st.markdown('1️⃣ 금융 도메인 샘플 데이터 다운로드')
        with open('./fine-tuning dataset/finetune_training.jsonl', 'r') as f:
             file_contents = f.read()
        st.download_button(
        	label = '데이터 다운로드 받기',
        	data = file_contents,
        	file_name ='sample.jsonl',
        	mime ='application/json')
        st.markdown('2️⃣ ChatGPT를 활용하여 미세 조정을 수행하는 방법')
        st.code(code, language='python')
        st.markdown('3️⃣ 만약에 데이터 및 모델을 업로드 하였는데, 오류가 발생한다면 다음 사항을 고려해보세요')
        st.markdown('⚠️ gpt model을 파인튜닝 하기위해서는 위에서 정의한 Chat-Completion 데이터 형식을 유지해야합니다.❗')
        st.code(data,language='json')
        st.markdown('⚠️ Fine Tuning을 한 모델 계정의 API를 입력해야 합니다. 그러지 않을경우 제대로 된 평가를 진행할 수 없습니다.❗')
        st.markdown('⚠️ OpenAPI Key를 확인해보세요. 종종 API Key를 잘못 입력한 경우가 있습니다. 🤣')
        st.markdown('')
        st.markdown('4️⃣ 모델 평가 방법은 아래 메뉴얼 대로 하시면 됩니다.')
        st.markdown('• 입력 1을 클릭하여 파인튜닝을 수행한 모델이름과 OpenAI API Key를 입력하면 됩니다.')
        st.markdown('• 입력 2를 클릭하여 팀 이름과 모델 타입을 설정하는데, 팀 이름은 최종 모델 평가 과정에서 필요한 사항이니 반드시 입력해주세요 ❗')
        st.markdown('• 평가를 수행하는데 대체로 10분 이상 소요 됩니다 😊 그 시간동안 모델을 활용하여 서비스를 구성해보세요 ')
        #st.markdown('• 추론이 끝나면 아래 다운로드 버튼을 클릭하여, 파인튜닝 된 ChatGpt 모델의 출력결과를 확인할 수 있습니다.')
        st.markdown('5️⃣ 미세조정된 ChatGPT를 활용하여 추론을 수행하는 방법')
        st.code(code2, language='python')
        st.markdown('')

        
        with st.form(key='inference_form_1'):  # 고유한 키 부여
            st.subheader('📋 인퍼런스 결과 생성')

            # 텍스트 입력 상자
            col1, col2 = st.columns([0.54, 0.46])
            
            with col1:
                with st.expander('입력 1'):
                    selected_option = st.text_input(
                        "모델 이름을 입력하세요.", 
                        placeholder='여기에 입력해주세요',
                        help='모델명 예시 ft:gpt-모델명:personal:파인튜닝 모델명'
                    )
                    api_key = st.text_input(
                        label='OpenAPI Key를 입력하세요.', 
                        max_chars=200, 
                        type='password',
                        placeholder='여기에 입력해주세요',
                        help='sk-xxxxxxxxxxxxxx'
                    )
                    
                    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY", api_key))

            with col2:
                with st.expander('입력 2'):
                    selected_option_name = st.text_input(
                        "소속 팀이름을 입력하세요.", 
                        placeholder='반드시 팀이름-제출시간으로 입력해주세요 ex)페르소나-1130',
                        help = 'ex) 전남대-15'
                    )
                    selected_option_type = st.text_input(
                        "모델 타입",
                        ("🟢 gpt-3.5-turbo")
                    )


            # 폼 제출 버튼
            submit_button = st.form_submit_button('모델 제출하기!')    

            if submit_button:
                # if not selected_option.startswith("ft:gpt-3.5-turbo"):
                if "gpt-3.5-turbo" not in selected_option:
                    st.error("모델명을 다시 한번 확인해주세요. gpt-3.5-turbo 모델만 사용가능 합니다")
                else:
                    with st.spinner():
                        client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY", api_key)) 
                        df_questions = pd.read_json('./streamlit/FinBench.jsonl', lines=True)
                        single_turn_outputs = []
                        for question in df_questions['questions']:
                            messages = [
                                {"role": "system", "content": 'You are an AI assistant. You will be given a task. You must generate a detailed and long answer.'},
                                {"role": "user", "content": str(question)}]
                            response = client.chat.completions.create(
                                model=selected_option,
                                messages=messages,
                                max_tokens=4096
                            )
                            single_turn_outputs.append([response.choices[0].message.content])

                        df_output = pd.DataFrame({
                            'id': df_questions['id'],
                            'category': df_questions['category'],
                            'questions': df_questions['questions'],
                            'outputs': single_turn_outputs,
                            'references': df_questions['references']
                        })

                        json_output = df_output.to_json(orient='records', lines=True, force_ascii=False)
                        st.session_state['json_output'] = json_output
                        st.session_state['selected_option_name'] = selected_option_name
                        upload_to_github(github_token, "NUMCHCOMCH/Kor_Finance-leaderboard", f"./data/{st.session_state['selected_option_name'].replace('/', '_')}.jsonl", json_output)

        #if 'json_output' in st.session_state:
        #    st.download_button(
        #        label='추론 결과 다운로드 하기',
        #        data=st.session_state['json_output'],
        #        file_name=f"{st.session_state['selected_option_name'].replace('/', '_')}.jsonl",
        #        mime='text/json'
        #    )
         
    with tab3:
        st.markdown('<h5> 👩‍✈️ 금융 LLM 리더보드 평가 규칙</h5>', unsafe_allow_html=True)
        st.markdown('1️⃣ 점수 산출은 3가지 지표(MMLU_F, FIQUSA, MATHQA) 점수의 평균으로 산출합니다.')
        st.markdown('2️⃣ MMLU_F와 MATHQA의 경우 금융 도메인 지식과 복잡한 추론이 필요하므로 가산점이 있습니다.😘')
        st.markdown('3️⃣ 원활한 서비스 개발을 위해서 모델 제출은 하루 최대 2번까지 가능합니다. 단❗마지막날은 원활한 진행을 위해 1번만 가능합니다. ')

        # DataFrame 생성
        st.markdown('')
        st.subheader('모델 추론 결과')
        
        # 카테고리별 점수 집계를 위한 딕셔너리
        category_scores = {}

        # 전체 싱글 점수와 멀티 점수의 리스트
        total_single_scores = []

        file_path1 = './streamlit/Baseline_model.jsonl'
        file_path2 = './streamlit/finetuning_model.jsonl'
        file_path3 = './streamlit/AI라이프-2100.jsonl'
        file_path4 = './streamlit/AI라이프-2200.jsonl'
        file_path5 = './streamlit/이루매-2100.jsonl'
        file_path6 = './streamlit/이루매-2200.jsonl'
        file_path7 = './streamlit/펠리컨적사고-2200.jsonl'
        # file_path8 = './streamlit/AI라이프-2200.jsonl'
        file_path8 = './streamlit/이루매-0900.jsonl'
        file_path9 = './streamlit/펠리컨적사고-0900.jsonl'
        file_path10 = './streamlit/이루매-1000.jsonl'
        file_path11 = './streamlit/AI라이프-0900.jsonl'
        file_path12 = './streamlit/AI라이프-1100.jsonl'
        file_path13 = './streamlit/펠리컨적사고-1100.jsonl'




        def extract_team_and_number(filename):
            # 파일 확장자 제거
            base_name = os.path.splitext(filename)[0]

            # '-'를 기준으로 팀 이름과 제출 번호 분리
            parts = base_name.split('-')
            if len(parts) > 1:
                team_name = parts[0]
                submission_number = parts[1]  # '1930' 추출
                if re.match(r'^\d{4}$', submission_number):  # 정확히 4자리 숫자인지 확인
                    formatted_time = f"{submission_number[:2]}:{submission_number[2:]}"  # '19:30' 형식으로 변경
                    return team_name, formatted_time
                else:
                    return team_name, "00:00"  # 숫자 형식이 맞지 않을 경우 "00:00"으로 반환
            else:
                # '-'가 없는 경우 "00:00"으로 오류 처리
                return parts[0], "00:00"



        # 지정된 패턴에 맞는 모든 파일을 찾아서 처리
        def process_file_to_dataframe(file_path):
            category_scores = {} 
            with open(file_path, 'r', encoding='utf-8-sig') as file:  # 'utf-8-sig'로 인코딩 변경
                for line in file:
                    item = json.loads(line)
                    category = item['category']
                    single_score = item['query_single']['judge_score']
        
                    if category not in category_scores:
                        category_scores[category] = []
                
                    category_scores[category].append(single_score)

            # 카테고리별 평균 점수를 계산하여 데이터프레임 생성
            avg_scores = {category: (sum(scores) / len(scores)) if scores else 0 for category, scores in category_scores.items()}

            # MMLU_F와 MATHQA에 가중치 적용
            if 'MMLU_F' in avg_scores:
                avg_scores['MMLU_F'] *= 1.1
            if 'MATHQA' in avg_scores:
                avg_scores['MATHQA'] *= 1.1
    
            # 데이터프레임 생성
            df = pd.DataFrame([avg_scores])
            
            # 파일 이름에서 팀 이름과 모델 제출 번호 추출
            team_name, submission_number = extract_team_and_number(os.path.basename(file_path))
            df['팀이름'] = team_name
            df['모델 제출일시'] = submission_number
            df['AVG_Score'] = ((df['MMLU_F'] + df['FIQUSA'] + df['MATHQA'])/3).round(3)

            return df
        
        # 소수점 한 자리로 설정
        pd.options.display.float_format = "{:.1f}".format
        df1 = process_file_to_dataframe(file_path1)
        df2 = process_file_to_dataframe(file_path2)
        df3 = process_file_to_dataframe(file_path3)
        df4 = process_file_to_dataframe(file_path4)
        df5 = process_file_to_dataframe(file_path5)
        df6 = process_file_to_dataframe(file_path6)
        df7 = process_file_to_dataframe(file_path7)
        df8 = process_file_to_dataframe(file_path8)
        df9 = process_file_to_dataframe(file_path9)
        df10 = process_file_to_dataframe(file_path10)
        df11 = process_file_to_dataframe(file_path11)
        df12 = process_file_to_dataframe(file_path12)
        df13 = process_file_to_dataframe(file_path13)
        # df8 = process_file_to_dataframe(file_path4)

        df = pd.concat([df3,df4,df5,df6,df7]).sort_values('AVG_Score',ascending=False).reset_index(drop=True)
        yesterday =  datetime.datetime.now() - datetime.timedelta(days=1)
        df['모델 제출일시'] = yesterday.strftime("%Y.%m.%d") + ' ' + df['모델 제출일시']
        #df['모델 제출일시'] = datetime.datetime.now().strftime("%Y.%m.%d") + ' ' + df['모델 제출일시']
        df = df[['팀이름','MMLU_F','FIQUSA','MATHQA','AVG_Score','모델 제출일시']]
        data = pd.concat([df8,df9,df10,df11,df12,df13]).sort_values('AVG_Score',ascending=False).reset_index(drop=True)
        data['모델 제출일시'] = datetime.datetime.now().strftime("%Y.%m.%d") + ' ' + data['모델 제출일시']
        data = data[['팀이름','MMLU_F','FIQUSA','MATHQA','AVG_Score','모델 제출일시']]
        df = pd.concat([df,data]).sort_values('AVG_Score',ascending=False).reset_index(drop=True)
        df.index = df.index + 1
        df.index.name = '순위'
        st.dataframe(df,use_container_width=True)

def main():
    setup_basic()
    setup_about()
    
if __name__ == "__main__":
    main()
