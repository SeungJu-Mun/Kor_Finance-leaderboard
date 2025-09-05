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

### run_ci_pipeline.sh (전체 파이프라인)
```bash
./scripts/run_ci_pipeline.sh [MODEL_NAME] [JUDGE_MODEL] [API_KEY] [MAX_TOKENS] [THREADS]
```

## 🤖 자동화된 CI/CD 파이프라인

이 프로젝트는 GitHub Actions를 통한 **완전 자동화된 평가 파이프라인**을 지원합니다!

### ✨ 자동 실행 조건
- `src/dataset/` 디렉토리에 새로운 데이터가 추가될 때
- `app/` 디렉토리의 앱 코드가 수정될 때  
- Pull Request가 생성될 때
- 수동으로 워크플로우를 실행할 때

### 🚀 CI 파이프라인 동작
1. **🔍 변경사항 감지** - 어떤 파일이 변경되었는지 자동 감지
2. **🚀 모델 추론** - 새로운 데이터에 대해 자동으로 모델 추론 실행
3. **🔍 모델 평가** - LLM as a Judge를 통한 자동 평가
4. **📊 결과 보고** - GitHub에 평가 결과 자동 업로드 및 PR 코멘트

### 📋 CI 설정 방법
1. GitHub 저장소 Settings에서 `OPENAI_API_KEY` Secret 추가
2. 데이터를 main 브랜치에 푸시하면 자동으로 파이프라인 실행! 

👀 **자세한 설정 방법**: [CI 설정 가이드](docs/CI_SETUP.md) 참조
