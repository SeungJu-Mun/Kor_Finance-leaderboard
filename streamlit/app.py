import streamlit as st
import pandas as pd
import openai
import os
import datetime
import base64
import requests

title = "🏆 Open-Ko-Finance-LLM-Leaderboard"
st.set_page_config(
    page_title=title,
    page_icon="🏆",
    layout="wide",
)
api_key = st.secrets['TOKEN']
st.write(api_key)

def upload_to_github(token, repo, path, content):
    url = f"https://api.github.com/repos/{repo}/contents/{path}"
    headers = {
        "Authorization": f"token {token}",
        "Content-Type": "application/json"
    }
    data = {
        "message": "Add inference result",
        "content": base64.b64encode(content.encode()).decode()
    }
    response = requests.put(url, headers=headers, json=data)
    if response.status_code == 201:
        st.success("추론 완료")
    else:
        st.error(f"추론 실패")

def setup_basic():
    url = 'https://personaai.co.kr/main'
    st.title(title)

    st.markdown(
        "🚀 Open-Ko-Finance-LLM 리더보드는 한국어 금융 분야의 전문적인 지식을 대형 언어 모델로 객관적인 평가를 수행합니다.\n"
    )
    st.markdown( f" 이 리더보드는 [PersonaAI](https://personaai.co.kr/main)와 [전남대학교](https://aicoss.kr/www/)가 공동 주최하며, [PersonaAI](https://personaai.co.kr/main)에서 운영합니다.")

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
        st.markdown('<h3>대회 개요</h3>', unsafe_allow_html=True)
        st.markdown('최근 인공지능(AI) 기술의 발전은 다양한 산업 분야에 걸쳐 혁신적인 변화를 가져오고 있습니다.')
        st.markdown('특히, 생성형 AI 기술의 도입은 자연어 처리(NLP)와 관련된 애플리케이션 개발에 큰 영향을 미치고 있는데,')
        st.markdown('금융 상담 서비스 분야에서도 AI를 활용한 자동화된 상담 시스템은 비용 절감과 서비스 효율성 향상을 목표로 활발히 연구되고 있습니다.')
        st.markdown('이러한 배경 속에서 이번 전남대 해커톤 금융 LLM 리더보드를 통해 금융 상담 분야에서 사용자에게 좀 더 높은 정확도와 신뢰성 있는 정보를 전달하기 위해 이번 대회를 개최하게 되었습니다.')
        st.write('')
        st.markdown('<h5>평가 방식</h5>', unsafe_allow_html=True)
        st.markdown('📈 우리는 [LogicKor](https://github.com/instructkr/LogicKor) 다분야 사고력 추론 벤치마크를 활용하여 금융 도메인에 LLM 모델을 테스트하는 통합 프레임워크를 통해 모델을 평가합니다. ')
        st.markdown('한국어로 번역한 데이터 세트와 한국어 웹 코퍼스를 수집하여, 3가지 작업(FIQUSA, MMLU_F, MATHQA)를 구축하여 새로운 데이터 세트를 처음부터 준비했습니다.')
        st.markdown('LLM 시대에 걸맞은 평가를 제공하기 위해 해당 벤치마크를 채택하였고, 최종 점수는 각 평가 데이터 세트에서 얻은 평균 점수로 변환됩니다.')
        st.markdown('평가는 ChatGPT API를 사용합니다.')
        st.write('')
        st.markdown('<h5>평가 기준 설명</h5>', unsafe_allow_html=True)
        st.markdown('1️⃣ FIQUSA : 금융 도메인 뉴스 헤드라인의 감성을 예측하여 시장 동향을 파악하는 벤치마크 입니다.')
        st.markdown('2️⃣ MMLU_F : 금융 관련 도메인을 정확하게 이해하고 있는지, 객관식 형태로 평가하는 벤치마크 입니다.')
        st.markdown('3️⃣ MATHQA : 리스크 관리, 옵션 가격 모델링 등 금융 분야에서 사용되는 수리적 문제를 잘 해결하는지 평가하는 벤치마크 입니다.')
        st.write('')
        st.markdown('<h5>대회 관련 문의사항</h5>', unsafe_allow_html=True)
        st.markdown('평가 예시 데이터셋과 Chatgpt 사용 관련 문의 사항이 있으시면 anstmdwn45@personaai.co.kr로 연락주세요 🤩')
        st.markdown('Made with ❤️ by the awesome open-source community from all over 🌍')
        st.write('')
        st.write('')
        st.write('')

    with tab2:
        code = '''
        import openai
        import os

        client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY", "API_KEY 입력"))

        # 학습 데이터 업로드
        def data_loader(train_file):
            with open(train_file, 'rb') as train_ft:
                training_response = client.files.create(file = train_ft, purpose='fine-tune')
            train_file_id = training_response.id
        
        # 미세조정 수행
        def gpt_finetuning():
            response = client.fine_tuning.jobs.create(
                training_file=training_file_id,
                model="모델명", # gpt-4-o-mini, gpt-3.5-turbo
                suffix="Finance_팀이름")
        '''
        st.markdown('<h3>Evaluation Queue for the 🚀 Open Ko-LLM Leaderboard</h3>', unsafe_allow_html=True)
        st.markdown('1️⃣ ChatGPT를 활용하여 미세 조정을 수행하는 방법')
        st.code(code, language='python')
        st.markdown('2️⃣ 만약에 모델을 업로드 하였는데, 오류가 발생한다면 다음 사항을 고려해보세요')
        st.markdown('⚠️ Fine Tuning을 한 모델 계정의 API를 입력해야 합니다. 그러지 않을경우 제대로 된 평가를 진행할 수 없습니다.❗')
        st.markdown('⚠️ OpenAPI Key를 확인해보세요. 종종 API Key를 잘못 입력한 경우가 있습니다. 🤣')
        st.markdown('')
        st.markdown('3️⃣ 모델 평가 방법은 아래 메뉴얼 대로 하시면 됩니다.')
        st.markdown('• Expander 1을 클릭하여 파인튜닝을 수행한 모델이름과 OpenAI API Key를 입력하면 됩니다.')
        st.markdown('• Expander 2를 클릭하여 팀 이름과 모델 타입을 설정하는데, 팀 이름은 최종 모델 평가 과정에서 필요한 사항이니 반드시 입력해주세요 ❗')
        st.markdown('• 추론을 수행하는데 대체로 10분 이상 소요 됩니다 😊 그 시간동안 간단하게 팀원과 협력하여 웹 페이지를 구성해보세요 ')
        st.markdown('• 추론이 끝나면 아래 다운로드 버튼을 클릭하여, 저장된 Jsonl 파일을 아래 이메일로 보내주시면, 리더보드에 결과가 반영이 됩니다.')
        st.markdown('모델 제출 이메일 : anstmdwn45@personaai.co.kr')
        
        with st.form(key='inference_form_1'):  # 고유한 키 부여
            st.subheader('📋 인퍼런스 결과 생성')

            # 텍스트 입력 상자
            col1, col2 = st.columns([0.54, 0.46])
            
            with col1:
                with st.expander('Expander 1'):
                    selected_option = st.text_input(
                        "모델 이름을 입력하세요.", 
                        placeholder='여기에 입력해주세요',
                        help='모델명 예시 ft:gpt-모델명:personal:파인튜닝 모델명'
                    )
                    api_key = st.text_input(
                        label='OpenAPI Key를 입력하세요.', 
                        max_chars=100, 
                        type='password',
                        placeholder='여기에 입력해주세요',
                        help='sk-xxxxxxxxxxxxxx'
                    )
                    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY", api_key))

            with col2:
                with st.expander('Expander 2'):
                    selected_option_name = st.text_input(
                        "소속 팀이름을 입력하세요.", 
                        placeholder='여기에 입력해주세요'
                    )
                    selected_option_type = st.selectbox(
                        "모델 타입을 입력하세요.",
                        ("🟢 gpt-3.5-turbo", "⭕ gpt-4-o-mini")
                    )


            if st.form_submit_button('추론 시작하기!'):
                with st.spinner():
                    df_questions = pd.read_json('FinBench_train.jsonl', lines=True)
                    single_turn_outputs = []
                    for question in df_questions['questions']:
                        messages = [
                            {"role": "system", "content": 'You are an AI assistant. You will be given a task. You must generate a detailed and long answer.'},
                            {"role": "user", "content": str(question)}
                        ]
                        response = client.chat.completions.create(
                            model=selected_option,
                            messages=messages,
                            max_tokens=4096
                        )
                        single_turn_outputs.append(response.choices[0].message.content)

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
                    upload_to_github(api_key, "CPM-AI/Kor_Finance-leaderboard", f"./data/{st.session_state['selected_option_name'].replace('/', '_')}.json", json_output)

        if 'json_output' in st.session_state:
            st.download_button(
                label='추론 결과 다운로드 하기',
                data=st.session_state['json_output'],
                file_name=f"{st.session_state['selected_option_name'].replace('/', '_')}.jsonl",
                mime='text/json'
            )
        
        

    with tab3:
        st.markdown('<h5> 👩‍✈️ 전남대 금융 LLM 리더보드 평가 규칙</h5>', unsafe_allow_html=True)
        st.markdown('1️⃣ 점수 산출은 Public과 Private 점수의 평균으로 산출합니다.')
        st.markdown('2️⃣ 원활한 서비스 개발을 위해서 Public 모델 제출은 하루 최대 3번까지 가능합니다.')
        st.markdown('3️⃣ Private 점수의 경우, 대회 종료 5시간 전에 최종 미세조정 모델을 제출한 결과로 산정합니다.')
        st.markdown('4️⃣ Model 평가는 gpt-4o를 기준으로 평가를 수행합니다.')

        # DataFrame 생성
        st.markdown('')
        st.subheader('LLM 모델 벤치마크')
        since = "2024-07-26 15:24"
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        df = pd.DataFrame({
            '팀 이름': ['Personaai','Persona_sLLM','전남대1','전남대2','전남대3'], 
            'FIQUSA': [8.2,8.4,6.7,6.6,7.5],
            'MMLU_F': [8.4,6.2,5.5,7.1,6.7], 
            'MATHQA': [8.3,6.5,8.2,8.1,8.8], 
            'Accuracy': [8.3,6.9,5.6,6.7,6.9],
            '모델 제출일시': [now,since,now,now,now]
        }).sort_values('Accuracy', ascending=False).reset_index(drop=True)
        st.dataframe(df, use_container_width=True)

def main():
    setup_basic()
    setup_about()
    
if __name__ == "__main__":
    main()
