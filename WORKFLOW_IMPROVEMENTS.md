# Workflow Improvements - Phase 1 & 2

## 구현 완료 기능

### Phase 1: Core Visualization

#### 1. Workflow Dashboard (research-queue.html)
**위치**: Research Queue 페이지의 각 활성 워크플로우 카드

**기능**:
- **Step-by-step Progress Indicator**: 4단계 워크플로우 시각화
  - Team Composition → Draft → Review → Revise
  - 현재 단계 강조 표시 (pulsing animation)
  - 완료된 단계는 체크마크 표시

- **Expert Status Grid**: 각 전문가의 실시간 작업 상태
  - 전문가별 status badge (waiting / active / completed)
  - 개별 progress bar (0-100%)
  - 리뷰 점수 표시 (완료 시)

- **Timeline Indicator**: 시간 추적
  - 경과 시간 (elapsed time)
  - 예상 남은 시간 (estimated remaining)
  - 동적으로 업데이트

**사용법**:
```
http://localhost:8080/web/research-queue.html
```
활성 워크플로우를 보면 자동으로 dashboard가 표시됩니다.

---

#### 2. Live Activity Feed (research-queue.html)
**위치**: Research Queue 페이지 - "View Activity Log" 버튼 클릭

**기능**:
- **실시간 로그 스트림**: 모든 워크플로우 이벤트 기록
  - Info (ℹ): 일반 정보 (시작, 진행 상태)
  - Success (✓): 성공적인 완료
  - Warning (⚠): 경고 메시지
  - Error (✕): 에러 발생

- **필터링**: 로그 레벨별 필터
  - All / Info / Success / Error

- **타임스탬프**: 각 이벤트의 정확한 시간 표시

**API Endpoint**:
```
GET /api/workflow-activity/{project_id}?limit=50
```

**로그 예시**:
```
14:32:15  ✓ Cryptography Expert completed review
          Score: 7.5/10, Comments: 3

14:30:42  ⟳ Economics Expert started review
          Reading draft (2,145 tokens)...

14:28:30  ✓ Initial draft completed
          3,421 tokens generated in 4.2min
```

---

### Phase 2: Enhanced UX

#### 3. Cost & Performance Analytics (create-report.html)
**위치**: Create Report 페이지 - Expert Team Proposal 섹션

**기능**:
- **Time Breakdown**: 단계별 예상 시간
  ```
  Initial Draft         5 min  ████░░░░░░ (28%)
  Review Round 1        6 min  █████░░░░░ (33%)
  Review Round 2        4 min  ███░░░░░░░ (22%)
  Final Revision        3 min  ██░░░░░░░░ (17%)
  ```

- **Cost Estimate**: 토큰 및 비용 추정
  - Input Tokens: ~50,000
  - Output Tokens: ~15,000
  - Model: Claude Opus 4.5
  - **Estimated Cost: $0.75**

- **동적 계산**: 전문가 수, 라운드 수, 모델에 따라 자동 계산

**가격 정보** (2026 기준):
| Model | Input (per 1M tokens) | Output (per 1M tokens) |
|-------|----------------------|------------------------|
| Opus 4.5 | $15 | $75 |
| Sonnet 4 | $3 | $15 |
| Haiku 4 | $0.8 | $4 |

---

#### 4. Interactive Expert Team Editor (create-report.html)
**위치**: Create Report 페이지 - Proposed Expert Team 섹션

**기능**:
- **Drag & Drop Reordering**: 전문가 우선순위 조정
  - 카드를 드래그해서 순서 변경
  - 자동으로 proposal 업데이트

- **Edit Expert Domain**: 전문가 이름/분야 수정
  - Edit 버튼 클릭 → 텍스트 입력

- **Manage Focus Areas**: 세부 전문 분야 관리
  - ❌ 버튼으로 focus area 제거
  - "➕ Add Focus" 버튼으로 추가

- **Add/Remove Experts**:
  - ❌ 버튼으로 전문가 제거
  - "➕ Add Another Expert" 버튼으로 추가

- **실시간 Cost 업데이트**: 팀 구성 변경 시 자동 재계산

**사용 시나리오**:
1. AI가 3명의 전문가 제안
2. 사용자가 4번째 전문가 추가 (Custom)
3. 전문가 순서를 드래그로 변경
4. Focus areas 수정
5. Cost estimate 자동 업데이트 ($0.75 → $1.00)

---

## API 변경사항

### 새로운 Response Models

```python
class ExpertStatus(BaseModel):
    expert_id: str
    expert_name: str
    status: str  # "waiting", "active", "completed"
    progress: int  # 0-100
    message: str
    score: Optional[float] = None

class CostEstimate(BaseModel):
    input_tokens: int
    output_tokens: int
    total_tokens: int
    estimated_cost_usd: float
    model_breakdown: Dict[str, dict]

class ActivityLogEntry(BaseModel):
    timestamp: str
    level: str  # "info", "success", "warning", "error"
    message: str
    details: Optional[dict] = None
```

### 업데이트된 Endpoints

#### GET /api/workflow-status/{project_id}
**추가된 필드**:
```json
{
  "expert_status": [
    {
      "expert_id": "expert-1",
      "expert_name": "Cryptography Expert",
      "status": "active",
      "progress": 67,
      "message": "Reviewing manuscript...",
      "score": null
    }
  ],
  "cost_estimate": {
    "input_tokens": 50000,
    "output_tokens": 15000,
    "total_tokens": 65000,
    "estimated_cost_usd": 0.75,
    "model_breakdown": { ... }
  },
  "elapsed_time_seconds": 720,
  "estimated_time_remaining_seconds": 360
}
```

#### GET /api/workflow-activity/{project_id}
**새로운 endpoint** - Activity log 조회
```json
{
  "activity": [
    {
      "timestamp": "2026-02-05T14:32:15.123Z",
      "level": "success",
      "message": "Cryptography Expert completed review",
      "details": {
        "score": 7.5,
        "comments": 3
      }
    }
  ]
}
```

#### POST /api/propose-team
**추가된 response 필드**:
```json
{
  "cost_estimate": {
    "input_tokens": 50000,
    "output_tokens": 15000,
    "estimated_cost_usd": 0.75
  }
}
```

---

## 테스트 방법

### 1. API 서버 시작
```bash
cd /home/jazz/git/ai-backed-research
./venv/bin/python api_server.py
```

### 2. 웹 서버 시작
```bash
cd web
python -m http.server 8080
```

### 3. 전체 플로우 테스트

**Step 1: 새 리서치 생성**
```
http://localhost:8080/web/create-report.html
```
1. Research type 선택 (Survey / Research)
2. Topic 입력: "Zero-Knowledge Rollups Security"
3. Expert customization (optional)
4. "Propose Expert Team" 클릭

**Step 2: Interactive Editor 테스트**
1. 제안된 전문가 팀 확인
2. Drag & drop으로 순서 변경
3. Focus area 추가/제거
4. Cost estimate 변화 확인
5. "Configure Workflow" 클릭

**Step 3: Workflow 모니터링**
```
http://localhost:8080/web/research-queue.html
```
1. Dashboard에서 4단계 진행 상황 확인
2. Expert status grid에서 각 전문가 상태 확인
3. Timeline indicator로 시간 추적
4. "View Activity Log" 클릭
5. 실시간 로그 확인 및 필터링

**Step 4: 결과 확인**
1. 완료 후 "Read Article" 클릭
2. "View Reviews" 클릭하여 리뷰 데이터 확인

---

## 구현 세부사항

### CSS 스타일링
- IBM Carbon Design System 유지
- 0px border-radius (직각 디자인)
- 8px grid system
- Consistent spacing (spacing-01 ~ spacing-07)

### 애니메이션
- Step indicator pulse (2s infinite)
- Progress bar transitions (0.3s ease)
- Hover effects (70ms transition)
- Drag & drop visual feedback

### 반응형 디자인
- Mobile: 단일 컬럼 레이아웃
- Tablet: 2-3 컬럼 grid
- Desktop: Full grid layout

---

## 다음 단계 (Phase 3 - Optional)

### Research History & Comparison
- 과거 리서치 검색
- Topic similarity matching (벡터 임베딩)
- Side-by-side comparison view
- Performance trend charts
- Template 저장 및 재사용

**예상 작업**:
- 데이터베이스 추가 (SQLite or PostgreSQL)
- 임베딩 모델 통합 (OpenAI embeddings)
- 새로운 페이지: `history.html`
- Comparison view API endpoint

---

## 알려진 제한사항

1. **Activity Log**: 메모리 저장 (서버 재시작 시 삭제)
   - 해결: 파일 또는 DB 저장으로 변경

2. **Cost Estimate**: 실제 토큰 수와 차이 있음
   - 해결: Orchestrator에서 실제 토큰 카운트 전달

3. **Real-time Updates**: Polling (3초마다)
   - 해결: WebSocket 또는 Server-Sent Events 도입

4. **Expert Status**: Orchestrator 통합 필요
   - 해결: WorkflowOrchestrator에서 expert status 업데이트 callback 추가

---

## 성능 최적화

- Activity log limit: 50 entries (default)
- Polling interval: 3 seconds
- Dashboard lazy loading
- CSS animations with GPU acceleration
- Debounced cost calculations

---

## 문의

기능 개선 제안이나 버그 리포트:
- GitHub Issues
- 또는 직접 수정 요청
