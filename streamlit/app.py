import streamlit as st
import pandas as pd
import openai
import subprocess
import os, json, re, time
from datetime import datetime
from threading import Lock
from typing import Dict, Union


body = '''<font size=3>\n
FIQASA : 금융 도메인 뉴스 헤드라인의 감성을 예측하여 시장 동향을 파악하는 벤치마크 입니다.\n
MMLU_F : 금융 관련 도메인을 정확하게 이해하고 있는지, 객관식 형태로 평가하는 벤치마크 입니다.\n
MATHQA : 리스크 관리, 옵션 가격 모델링 등 금융 분야에서 사용되는 수리적 문제를 잘 해결하는지 평가하는 벤치마크 입니다.
'''
def main():
    # 기본 CSS 설정
    add_selector = st.sidebar.selectbox('메뉴 선택', ('추론','리더보드'))

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write(' ')

    with col2:
        st.image('전남대학교.svg',width=150, use_column_width='auto')

    with col3:
        st.write(' ')
    st.markdown(
        """
        <style>
        .title {
            color: white;
            text-align: center;
            font-size: 2.0em;
        }
        .subtitle {
            color: white;
            text-align: center;
            font-size: 1.2em;
        }
        .content {
            color: white;
            text-align: center;
            font-size: 1em;
        }
        .spacer {
            margin: 20px 0;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    # 기타 Streamlit 요소 구성
    if add_selector == '추론':
        st.header('🏆 한국 금융 LLM-Leaderboard')
        st.caption(body, unsafe_allow_html=True)
        st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)
        leader = st.form('leader board')    
        leader.subheader('📋 인퍼런스 결과 생성')

        # 텍스트 입력 상자
        
        selected_option = leader.text_input("모델 이름을 입력하시오.", placeholder='여기에 입력해주세요',help='모델명 예시 ft:gpt-모델명:personal:파인튜닝 모델명')
        title = leader.text_input(label='OpenAPI Key를 입력하시오', max_chars=100, type='password',placeholder='여기에 입력해주세요',help='sk-xxxxxxxxxxxxxx')

        client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY", title))

        if leader.form_submit_button('훈련 데이터 평가 시작'):
            df_questions = pd.read_json('FinBench_train.jsonl', lines=True)
            single_turn_outputs = []
            for question in df_questions['questions']:
                    messages = [
                        {"role": "system", "content": 'You are an AI assistant. You will be given a task. You must generate a detailed and long answer.'},
                        {"role": "user", "content": str(question)}]
                    response = client.chat.completions.create(
                    model=selected_option,
                    messages=messages,
                    max_tokens=4096)
                    single_turn_outputs.append(response.choices[0].message.content)

            df_output = pd.DataFrame({
            'id': df_questions['id'],
            'category': df_questions['category'],
            'questions': df_questions['questions'],
            'outputs': list(zip(single_turn_outputs)),
            'references': df_questions['references']
        })

            json_output = df_output.to_json(orient='records', lines=True, force_ascii=False)
            st.download_button(label="Download JSON Output",
                               data=json_output,
                               file_name=f"{selected_option.replace('/', '_')}.jsonl",
                               mime='text/json')
    elif add_selector == '리더보드':
        st.subheader('📋 Judge 모델로 평가')
        uploaded_file = st.file_uploader('추론 생성 결과 Jsonl 파일을 선택해주세요', accept_multiple_files=False)
        if uploaded_file is not None:
            df_model_output = pd.read_json(uploaded_file, lines=True)
            df_judge_template = pd.read_json('judge_template-single.jsonl', lines=True)
            client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY","api-key"))
            results = []
                
            for index, row in df_model_output.iterrows():
                prompt = f"**질문**\n{row['questions']}\n\n**모델 답변**\n{row['outputs']}"

                if row['references']:
                    prompt += f"\n\n**Ground Truth**\n{row['references']}"

                prompt += "\n\n[[대화 종료. 평가 시작.]]"

                try:
                    response = client.chat.completions.create(
                        model='gpt-4o',
                        temperature=0,
                        n=1,
                        messages=[
                            {"role": "system", "content": df_judge_template.iloc[0]['system_prompt']},
                            {"role": "user", "content": prompt}
                        ]
                    )

                    content = response.choices[0].message.content
                    judge_message_match = re.search(r"평가:(.*?)점수:", content, re.DOTALL)
                    judge_message = judge_message_match.group(1).strip() if judge_message_match else "No judge message found"
                    judge_score_match = re.search(r"점수:\s*(\d+(\.\d+)?)", content)
                    
                    if judge_score_match:
                        judge_score = float(judge_score_match.group(1))
                    else:
                        raise ValueError("No score found in response")

                    results.append({
                        'id': row['id'],
                        'category' : row['id'],
                        'judge_score': judge_score
                    })
                except Exception as e:
                    st.error(f"An error occurred: {e}")

            results_df = pd.DataFrame(results)
            st.write(results_df)
         
if __name__ == "__main__":
    main()
