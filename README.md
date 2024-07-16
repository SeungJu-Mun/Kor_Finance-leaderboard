# Kor Finance Leaderboard
한국어 금융 LLM 리더보드
## Note

pr 적극 환영합니다.
벤치마크 결과 Self-Report도 받습니다. issue나 pr 부탁드립니다. 💕
* 권장 사항: PR 이전에 `make format && make check` 를 통해 코드 포맷팅을 확인해주세요. (black, isort, ruff 의존성 설치 필요)

## Repository
본 Repo는 Kor Finance Leaderboard 벤치마크의 추론 및 평가 코드, 데이터셋을 담고 있습니다.

## Evaluation Example
Chat gpt 활용, model_len 4096

### 1. 인퍼런스 결과 생성
```bash
python generator-openai-train.py
```

### 2. Judge 모델로 평가

#### OpenAI

```bash
python judgement-single.py -o gpt-3.5-turbo-0125.jsonl -k open-api key -t 30
```
### 3. 결과 확인

```bash
python score-single.py -p 평가결과.jsonl
```

### Streamlit
<p align="left" width="150%">
<img src="assert/Streamlit_화면예시.png" alt="NLP Logo" style="width: 50%;">
</p>
