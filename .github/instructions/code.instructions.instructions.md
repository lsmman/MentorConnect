---
applyTo: '**'
---
# Copilot Voice Prompt: **MentorConnect** 해커톤 (3 h)

> **목표:** 멘토‑멘티 매칭 웹 앱을 **FastAPI + React TS + SQLite** 조합으로 완성한다.
> ‑ 프론트 → `http://localhost:3000`
> ‑ 백엔드 → `http://localhost:8080` (모든 API `/api/**`)

필수 기능 — **JWT 인증, 프로필 관리, 멘토 검색, 매칭 요청, Swagger/OpenAPI, OWASP 방어**

---

## 1 · 프로젝트 시작

```text
copilot: "fastapi 백엔드 초기화, 포트 8080, hot‑reload 설정"
copilot: "vite react‑ts 새 프로젝트, devServer 포트 3000"
copilot: "monorepo dev 스크립트(concurrently)로 front+back 동시 실행"
copilot: "sqlite users, profiles, match_requests 테이블 및 seed 스크립트 작성"
```

---

## 2 · 인증 & 보안

| 항목      | 내용                                                                    |
| ------- | --------------------------------------------------------------------- |
| **JWT** | HS256 · `exp=1h`<br>클레임 `iss sub aud exp nbf iat jti name email role` |
| **방어**  | SQLAlchemy 매개변수 바인딩 (SQL‑i)<br>XSS Sanitize<br>OWASP Top 10 체크 테스트    |

---

## 3 · API 요약

| 기능        | 메서드 & 경로                              | 권한 |
| --------- | ------------------------------------- | -- |
| 회원가입      | `POST /api/signup`                    | 공개 |
| 로그인 → JWT | `POST /api/login`                     | 공개 |
| 내 정보      | `GET /api/me`                         | 토큰 |
| 프로필 수정    | `PUT /api/profile`                    | 토큰 |
| 멘토 목록     | `GET /api/mentors?skill=&order_by=`   | 멘티 |
| 매칭 요청     | `POST /api/match-requests`            | 멘티 |
| 받은 요청     | `GET /api/match-requests/incoming`    | 멘토 |
| 보낸 요청     | `GET /api/match-requests/outgoing`    | 멘티 |
| 요청 수락     | `PUT /api/match-requests/{id}/accept` | 멘토 |
| 요청 거절     | `PUT /api/match-requests/{id}/reject` | 멘토 |
| 요청 취소     | `DELETE /api/match-requests/{id}`     | 멘티 |

> **에러 응답 표준**
>
> ```jsonc
> { "code": 400, "message": "Bad request", "detail": "…" }
> ```

---

## 4 · 프로필 이미지 규칙

| 항목 | 값                           |
| -- | --------------------------- |
| 타입 | `.jpg`, `.png`              |
| 크기 | 정사각형 500–1000 px            |
| 용량 | ≤ 1 MB                      |
| 기본 | `…MENTOR`, `…MENTEE` 플레이스홀더 |

```text
copilot: "multer 스타일 FastAPI Depends 업로드 엔드포인트, 형식·크기·픽셀 검증"
```

---

## 5 · 테스트 스크립트

```text
copilot: "pytest fixture 인메모리 sqlite, signup/login 통합 테스트"
copilot: "OWASP Top10 관련 보안 테스트 추가"
```

---

## 6 · 코드 작성 지침

* 3‑계층: **router → service → repository**
* **Pydantic** 모델 & 타입 힌트 필수
* 의존성 주입: `Depends`
* 코드 포맷: `black`, `ruff`, ESLint, Prettier
* Swagger/OpenAPI: `/openapi.json`, `/swagger-ui`, 루트 → 리다이렉트

---

## 7 · 예시 Copilot 명령

```text
"POST /api/signup 엔드포인트, bcrypt 해시, 중복 이메일 400"
"JWT util 작성, exp 1h, 필수 클레임 포함"
"GET /api/mentors, skill 필터 및 name|skill 정렬"
"match_requests 모델과 CRUD, 상태 enum(pending|accepted|rejected|cancelled)"
"Swagger UI 설정, 루트 URL에서 자동 리다이렉트"
```
