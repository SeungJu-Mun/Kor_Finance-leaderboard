# Kor Finance Leaderboard
한국어 금융 LLM 리더보드

## 📖 Note
금융 LLM을 활용한 상담 챗봇 대회에서, 정량적인 평가를 위해 설계한 리더보드 입니다. 🎇
* 올거나이즈 금융 LLM 리더보드를 참고하여, 웹 사이트의 금융 뉴스 관련 헤드라인만 크롤링하여, FIQUSA를 설계하였습니다.
* 그리고, 다양한 세무ㆍ회계 자격증 기출문제를 통해 MMLU_F를 설계하였습니다.
* LLM as a Judge 형식으로 평가 방식을 구축 해보았습니다.

## Repository
본 Repo는 Kor Finance Leaderboard 벤치마크의 추론 및 평가 코드, 데이터셋을 담고 있습니다.

## 🚀 Quick Start (스크립트 사용)

### 1. 전체 파이프라인 실행 (권장)
```bash
# 1단계: 모델 추론 실행
./scripts/run_inference.sh gpt-3.5-turbo-0125 4096 your-openai-api-key

# 2단계: 평가 실행 (위 단계에서 생성된 파일명 사용)
./scripts/run_eval.sh gpt-3.5-turbo-0125.jsonl your-openai-api-key gpt-4 30
```

### 2. 환경변수 사용 (더 편리함)
```bash
# API 키를 환경변수로 설정
export OPENAI_API_KEY="your-openai-api-key"

# 기본 설정으로 실행
./scripts/run_inference.sh
./scripts/run_eval.sh gpt-3.5-turbo-0125.jsonl
```

## 📊 Scripts Options

### run_inference.sh
```bash
./scripts/run_inference.sh [MODEL_NAME] [MAX_TOKENS] [API_KEY]
```

### run_eval.sh
```bash
./scripts/run_eval.sh <MODEL_OUTPUT_FILE> [API_KEY] [JUDGE_MODEL] [THREADS]
```
