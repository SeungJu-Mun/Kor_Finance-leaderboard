#!/bin/bash

# 한국어 금융 LLM 리더보드 - 모델 추론 실행 스크립트
# Usage: ./scripts/run_inference.sh [MODEL_NAME] [MAX_TOKENS] [API_KEY]

set -e  # 오류 발생 시 스크립트 중단

# 기본값 설정
DEFAULT_MODEL="gpt-3.5-turbo-0125"
DEFAULT_MAX_TOKENS=4096
DEFAULT_API_KEY="${OPENAI_API_KEY}"

# 인수 처리
MODEL_NAME="${1:-$DEFAULT_MODEL}"
MAX_TOKENS="${2:-$DEFAULT_MAX_TOKENS}"
API_KEY="${3:-$DEFAULT_API_KEY}"

# API 키 확인
if [ -z "$API_KEY" ]; then
    echo "❌ 오류: OpenAI API 키가 필요합니다."
    echo "환경변수 OPENAI_API_KEY를 설정하거나 세 번째 인수로 전달해주세요."
    echo "사용법: $0 [model_name] [max_tokens] [api_key]"
    exit 1
fi

echo "🚀 모델 추론을 시작합니다..."
echo "📋 설정:"
echo "  - 모델: $MODEL_NAME"
echo "  - 최대 토큰: $MAX_TOKENS"
echo "  - 출력 파일: ${MODEL_NAME//\//_}.jsonl"
echo ""

# 추론 디렉토리로 이동하여 실행
cd src/inference

echo "⏳ 추론 실행 중..."
export OPENAI_API_KEY="$API_KEY"

# uv가 설치되어 있으면 uv run 사용, 아니면 python 직접 사용
if command -v uv >/dev/null 2>&1; then
    echo "🚀 uv를 사용하여 추론 실행..."
    uv run python generator-openai-test.py \
        --model "$MODEL_NAME" \
        --model_len "$MAX_TOKENS"
else
    echo "🐍 python을 사용하여 추론 실행..."
    python generator-openai-test.py \
        --model "$MODEL_NAME" \
        --model_len "$MAX_TOKENS"
fi

# 결과 파일을 루트 디렉토리로 이동
OUTPUT_FILE="${MODEL_NAME//\//_}.jsonl"
if [ -f "$OUTPUT_FILE" ]; then
    mv "$OUTPUT_FILE" "../../$OUTPUT_FILE"
    echo "✅ 추론 완료! 결과 파일: $OUTPUT_FILE"
    echo "📊 다음 단계: ./scripts/run_eval.sh $OUTPUT_FILE [API_KEY]"
else
    echo "❌ 오류: 출력 파일이 생성되지 않았습니다."
    exit 1
fi
