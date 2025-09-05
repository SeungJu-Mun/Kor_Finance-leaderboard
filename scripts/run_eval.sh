#!/bin/bash

# 한국어 금융 LLM 리더보드 - 모델 평가 실행 스크립트
# Usage: ./scripts/run_eval.sh [MODEL_OUTPUT_FILE] [API_KEY] [JUDGE_MODEL] [THREADS]

set -e  # 오류 발생 시 스크립트 중단

# 기본값 설정
DEFAULT_JUDGE_MODEL="gpt-4"
DEFAULT_THREADS=10
DEFAULT_API_KEY="${OPENAI_API_KEY}"

# 인수 처리
MODEL_OUTPUT="${1}"
API_KEY="${2:-$DEFAULT_API_KEY}"
JUDGE_MODEL="${3:-$DEFAULT_JUDGE_MODEL}"
THREADS="${4:-$DEFAULT_THREADS}"

# 필수 인수 확인
if [ -z "$MODEL_OUTPUT" ]; then
    echo "❌ 오류: 모델 출력 파일이 필요합니다."
    echo "사용법: $0 <model_output_file> [api_key] [judge_model] [threads]"
    echo "예시: $0 gpt-3.5-turbo-0125.jsonl"
    exit 1
fi

# 파일 존재 확인
if [ ! -f "$MODEL_OUTPUT" ]; then
    echo "❌ 오류: 파일을 찾을 수 없습니다: $MODEL_OUTPUT"
    exit 1
fi

# API 키 확인
if [ -z "$API_KEY" ]; then
    echo "❌ 오류: OpenAI API 키가 필요합니다."
    echo "환경변수 OPENAI_API_KEY를 설정하거나 두 번째 인수로 전달해주세요."
    exit 1
fi

echo "🔍 모델 평가를 시작합니다..."
echo "📋 설정:"
echo "  - 입력 파일: $MODEL_OUTPUT"
echo "  - Judge 모델: $JUDGE_MODEL"
echo "  - 스레드 수: $THREADS"
echo ""

# 평가 디렉토리로 이동하여 실행
cd src/eval

echo "⏳ Judge 모델로 평가 중..."

# uv가 설치되어 있으면 uv run 사용, 아니면 python 직접 사용
if command -v uv >/dev/null 2>&1; then
    echo "🚀 uv를 사용하여 평가 실행..."
    uv run python judgement-single.py \
        -o "../../$MODEL_OUTPUT" \
        -k "$API_KEY" \
        -j "$JUDGE_MODEL" \
        -t "$THREADS"
else
    echo "🐍 python을 사용하여 평가 실행..."
    python judgement-single.py \
        -o "../../$MODEL_OUTPUT" \
        -k "$API_KEY" \
        -j "$JUDGE_MODEL" \
        -t "$THREADS"
fi

# 생성된 judge 파일 찾기
JUDGE_FILE=$(ls judge_*.jsonl 2>/dev/null | tail -1)

if [ -z "$JUDGE_FILE" ]; then
    echo "❌ 오류: Judge 결과 파일이 생성되지 않았습니다."
    exit 1
fi

echo "📊 평가 완료! Judge 파일: $JUDGE_FILE"
echo ""

echo "🧮 점수 계산 중..."

# uv가 설치되어 있으면 uv run 사용, 아니면 python 직접 사용
if command -v uv >/dev/null 2>&1; then
    uv run python score-single.py -p "$JUDGE_FILE"
else
    python score-single.py -p "$JUDGE_FILE"
fi

# Judge 파일을 루트 디렉토리로 이동
mv "$JUDGE_FILE" "../../$JUDGE_FILE"

echo ""
echo "✅ 평가 완료!"
echo "📄 Judge 결과 파일: $JUDGE_FILE"
echo "🔍 상세 결과는 위의 점수 출력을 확인해주세요."
