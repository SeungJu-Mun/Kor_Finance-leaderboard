#!/bin/bash

# 한국어 금융 LLM 리더보드 - CI 파이프라인 전체 실행 스크립트
# Usage: ./scripts/run_ci_pipeline.sh [MODEL_NAME] [JUDGE_MODEL] [API_KEY]

set -e  # 오류 발생 시 스크립트 중단

# 기본값 설정
DEFAULT_MODEL="gpt-3.5-turbo-0125"
DEFAULT_JUDGE_MODEL="gpt-4"
DEFAULT_MAX_TOKENS=4096
DEFAULT_THREADS=10
DEFAULT_API_KEY="${OPENAI_API_KEY}"

# 인수 처리
MODEL_NAME="${1:-$DEFAULT_MODEL}"
JUDGE_MODEL="${2:-$DEFAULT_JUDGE_MODEL}"
API_KEY="${3:-$DEFAULT_API_KEY}"
MAX_TOKENS="${4:-$DEFAULT_MAX_TOKENS}"
THREADS="${5:-$DEFAULT_THREADS}"

# API 키 확인
if [ -z "$API_KEY" ]; then
    echo "❌ 오류: OpenAI API 키가 필요합니다."
    echo "환경변수 OPENAI_API_KEY를 설정하거나 세 번째 인수로 전달해주세요."
    exit 1
fi

echo "🚀 CI 파이프라인 시작"
echo "=================================================="
echo "설정:"
echo "  - 모델: $MODEL_NAME"
echo "  - Judge 모델: $JUDGE_MODEL"
echo "  - 최대 토큰: $MAX_TOKENS"
echo "  - 스레드 수: $THREADS"
echo "=================================================="
echo ""

# 타임스탬프 생성
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
OUTPUT_FILE="${MODEL_NAME//\//_}.jsonl"
LOG_DIR="ci_logs"
mkdir -p "$LOG_DIR"

# 로그 파일 설정
INFERENCE_LOG="$LOG_DIR/inference_$TIMESTAMP.log"
EVAL_LOG="$LOG_DIR/eval_$TIMESTAMP.log"

echo "📋 1단계: 모델 추론 실행"
echo "로그 파일: $INFERENCE_LOG"

# 추론 실행
if ./scripts/run_inference.sh "$MODEL_NAME" "$MAX_TOKENS" "$API_KEY" 2>&1 | tee "$INFERENCE_LOG"; then
    echo "✅ 추론 완료"
    
    # 결과 파일 검증
    if [ -f "$OUTPUT_FILE" ]; then
        LINES=$(wc -l < "$OUTPUT_FILE")
        echo "📊 생성된 결과: $LINES 줄"
    else
        echo "❌ 오류: 출력 파일이 생성되지 않았습니다: $OUTPUT_FILE"
        exit 1
    fi
else
    echo "❌ 추론 실패"
    exit 1
fi

echo ""
echo "📋 2단계: 모델 평가 실행"
echo "로그 파일: $EVAL_LOG"

# 평가 실행
if ./scripts/run_eval.sh "$OUTPUT_FILE" "$API_KEY" "$JUDGE_MODEL" "$THREADS" 2>&1 | tee "$EVAL_LOG"; then
    echo "✅ 평가 완료"
    
    # Judge 파일 찾기
    JUDGE_FILE=$(ls judge_*.jsonl 2>/dev/null | tail -1)
    if [ -n "$JUDGE_FILE" ]; then
        echo "📄 Judge 결과: $JUDGE_FILE"
    else
        echo "⚠️  경고: Judge 파일을 찾을 수 없습니다"
    fi
else
    echo "❌ 평가 실패"
    exit 1
fi

echo ""
echo "📋 3단계: 결과 요약 생성"

# 결과 요약 파일 생성
SUMMARY_FILE="$LOG_DIR/summary_$TIMESTAMP.md"

cat > "$SUMMARY_FILE" << EOF
# 🏆 한국어 금융 LLM 평가 결과

## 📋 실행 정보
- **실행 시간**: $(date '+%Y-%m-%d %H:%M:%S')
- **모델**: $MODEL_NAME
- **Judge 모델**: $JUDGE_MODEL
- **최대 토큰**: $MAX_TOKENS
- **스레드 수**: $THREADS

## 📊 파일 정보
- **추론 결과**: $OUTPUT_FILE
- **Judge 결과**: ${JUDGE_FILE:-"생성되지 않음"}
- **추론 로그**: $INFERENCE_LOG
- **평가 로그**: $EVAL_LOG

## 📈 평가 점수
EOF

# 점수 계산 결과 추가
if [ -n "$JUDGE_FILE" ] && [ -f "$JUDGE_FILE" ]; then
    echo "\`\`\`" >> "$SUMMARY_FILE"
    cd src/eval
    python score-single.py -p "../../$JUDGE_FILE" >> "../../$SUMMARY_FILE" 2>&1 || echo "점수 계산 중 오류 발생" >> "../../$SUMMARY_FILE"
    cd ../..
    echo "\`\`\`" >> "$SUMMARY_FILE"
else
    echo "평가 점수를 계산할 수 없습니다." >> "$SUMMARY_FILE"
fi

echo "📄 요약 보고서: $SUMMARY_FILE"
echo ""
echo "🎉 CI 파이프라인 완료!"
echo "=================================================="

# 요약 내용을 화면에 출력
cat "$SUMMARY_FILE"
