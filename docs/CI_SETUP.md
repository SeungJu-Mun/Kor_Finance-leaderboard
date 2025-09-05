# 🤖 CI/CD 파이프라인 설정 가이드

본 문서는 한국어 금융 LLM 리더보드의 자동 평가 파이프라인 설정 방법을 안내합니다.

## 📋 개요

CI 파이프라인은 다음과 같은 상황에서 자동으로 실행됩니다:

1. **main 브랜치에 푸시할 때** - `src/dataset/` 또는 `app/` 디렉토리에 변경사항이 있을 경우
2. **Pull Request 생성 시** - 위와 동일한 경로에 변경사항이 있을 경우  
3. **수동 실행** - GitHub Actions에서 직접 트리거

## 🔧 설정 방법

### 1. GitHub Secrets 설정

GitHub 저장소에서 다음 Secret을 설정해야 합니다:

1. 저장소의 **Settings** → **Secrets and variables** → **Actions** 이동
2. **New repository secret** 클릭
3. 다음 Secret 추가:

| Secret 이름 | 설명 | 예시 |
|------------|------|------|
| `OPENAI_API_KEY` | OpenAI API 키 | `sk-...` |

### 2. 워크플로우 파일 확인

`.github/workflows/auto-eval.yml` 파일이 올바르게 설정되어 있는지 확인합니다.

### 3. 권한 설정

GitHub Actions가 제대로 동작하도록 저장소 권한을 확인합니다:

1. **Settings** → **Actions** → **General**
2. **Workflow permissions**에서 "Read and write permissions" 선택
3. "Allow GitHub Actions to create and approve pull requests" 체크

## 🚀 사용 방법

### 자동 실행

1. **데이터셋 변경**: `src/dataset/evaluation_data/` 또는 `src/dataset/finetuning_data/`에 파일을 추가/수정
2. **앱 변경**: `app/` 디렉토리의 파일을 수정
3. **main 브랜치에 푸시** 또는 **Pull Request 생성**

### 수동 실행

1. GitHub 저장소의 **Actions** 탭 이동
2. **🤖 자동 모델 평가 파이프라인** 워크플로우 선택
3. **Run workflow** 클릭
4. 필요시 매개변수 조정:
   - `model_name`: 평가할 모델명 (기본값: gpt-3.5-turbo-0125)
   - `max_tokens`: 최대 토큰 수 (기본값: 4096)
   - `judge_model`: Judge 모델명 (기본값: gpt-4)
   - `threads`: 평가 스레드 수 (기본값: 10)

### 로컬에서 CI 파이프라인 테스트

CI를 GitHub에서 실행하기 전에 로컬에서 전체 파이프라인을 테스트할 수 있습니다:

```bash
# 환경변수 설정
export OPENAI_API_KEY="your-api-key"

# 전체 파이프라인 실행
./scripts/run_ci_pipeline.sh

# 또는 특정 설정으로 실행
./scripts/run_ci_pipeline.sh gpt-3.5-turbo-0125 gpt-4 your-api-key 4096 10
```

## 📊 파이프라인 단계

### 1. 🔍 변경사항 감지
- 변경된 파일 목록 확인
- 평가가 필요한 변경사항인지 판단

### 2. 🚀 모델 추론
- 지정된 모델로 FinBench 데이터셋에 대해 추론 실행
- 결과를 JSONL 파일로 저장
- 추론 결과를 아티팩트로 업로드

### 3. 🔍 모델 평가
- LLM as a Judge를 사용하여 추론 결과 평가
- 다중 스레드로 병렬 처리
- 평가 결과를 아티팩트로 업로드

### 4. 📊 결과 보고서
- 전체 파이프라인 실행 결과 요약
- 카테고리별 점수 계산 및 표시
- Pull Request에 자동 코멘트 작성

## 📁 생성되는 파일들

### GitHub Actions 실행 시
- **Artifacts**: 추론 결과 및 평가 결과 파일
- **Summary**: GitHub Actions 실행 요약 페이지에 결과 표시
- **PR Comments**: Pull Request에 평가 결과 자동 코멘트

### 로컬 실행 시 (`run_ci_pipeline.sh`)
```
ci_logs/
├── inference_YYYYMMDD_HHMMSS.log     # 추론 로그
├── eval_YYYYMMDD_HHMMSS.log          # 평가 로그
└── summary_YYYYMMDD_HHMMSS.md        # 결과 요약
```

## ⚠️ 주의사항

1. **API 비용**: OpenAI API 사용에 따른 비용이 발생할 수 있습니다
2. **실행 시간**: 전체 파이프라인은 10-60분 정도 소요될 수 있습니다
3. **동시 실행**: 여러 워크플로우가 동시에 실행되면 API 제한에 걸릴 수 있습니다
4. **브랜치 보호**: main 브랜치에 보호 규칙을 설정하여 CI 통과 후에만 병합되도록 할 수 있습니다

## 🔧 트러블슈팅

### API 키 오류
```
❌ 오류: OpenAI API 키가 필요합니다.
```
→ GitHub Secrets에 `OPENAI_API_KEY`가 올바르게 설정되었는지 확인

### 파일 경로 오류
```
❌ 오류: 파일을 찾을 수 없습니다
```
→ 스크립트 실행 위치와 파일 경로 확인

### 권한 오류
```
Permission denied
```
→ 스크립트 파일에 실행 권한이 있는지 확인: `chmod +x scripts/*.sh`

## 📈 확장 가능성

1. **다중 모델 평가**: 여러 모델을 동시에 평가하는 매트릭스 빌드
2. **성능 추적**: 시간에 따른 모델 성능 변화 추적
3. **Slack/Discord 알림**: 평가 완료 시 팀 채널에 알림
4. **자동 배포**: 평가 결과가 좋으면 자동으로 프로덕션 환경에 배포
5. **A/B 테스트**: 다른 설정으로 실행하여 성능 비교
