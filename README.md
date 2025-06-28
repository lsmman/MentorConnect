# MentorConnect

# 멘토-멘티 매칭 앱 개발 요구사항

## 앱 개요

이 앱은 **멘토와 멘티를 서로 매칭하는 시스템**입니다. 멘토는 자신의 기술 스택과 소개를 등록하고, 멘티는 원하는 멘토에게 매칭 요청을 보낼 수 있습니다. 멘토는 매칭 요청을 수락하거나 거절할 수 있으며, 한 명의 멘토는 동시에 한 명의 멘티와만 매칭할 수 있습니다.

## 앱 개발 공통 요구사항

- 제한시간: 3시간
- 사용 도구: VS Code + GitHub Copilot 보이스 코딩
- 기술 스택: 웹 앱
- 사용 언어: Python, JavaScript, Java, .NET 중 선택
- 데이터베이스: 자유 선택 (단, 로컬에서 돌아갈 수 있어야 함)

## 기능 요구사항

### 1. 회원가입 및 로그인

- 사용자는 이메일, 비밀번호, 역할(멘토 또는 멘티)을 입력해 회원가입할 수 있어야 합니다.
- 회원가입한 사용자는 로그인할 수 있어야 합니다.
- 로그인 후에는 JWT 형식의 인증토큰을 발급 받습니다. 이 인증 토큰을 이용해 백엔드 API와 통신해야 합니다.

### 2. 사용자 프로필

- 사용자는 로그인 후 자신의 프로필을 등록하거나 수정할 수 있어야 합니다.
  - 멘토: 이름, 소개글, 프로필 이미지, 기술 스택
  - 멘티: 이름, 소개글, 프로필 이미지
- 로그인한 사용자는 자신의 정보를 조회할 수 있어야 합니다.
- 프로필 이미지는 수정하지 않은 경우 기본 이미지를 보여줘야 합니다.
- 프로필 이미지는 로컬 컴퓨터의 이미지 파일을 업로드해서 수정할 수 있습니다.

### 3. 멘토 목록 조회

- 멘티는 멘토의 리스트를 볼 수 있어야 합니다.
- 검색 필터(예: 기술 스택으로 필터링)를 통해 특정 기술 스택을 가진 멘토만 검색할 수 있어야 합니다.
- 멘토 이름 또는 기술 스택으로 멘토 리스트를 정렬할 수 있어야 합니다.

### 4. 매칭 요청 기능

- 멘티는 원하는 멘토에게 매칭 요청을 보낼 수 있어야 합니다.
- 한 멘토에게 한 번만 요청할 수 있으며, 멘토가 수락하거나 거절하기 전까지 다른 멘토에게 중복 요청은 불가능합니다.
- 요청에는 간단한 메시지를 포함할 수 있습니다.

### 5. 요청 수락/거절

- 멘토는 받은 매칭 요청 목록을 볼 수 있어야 하며, 요청을 **수락** 또는 **거절**할 수 있어야 합니다.
- 멘토는 **한 명의 멘티 요청만 수락**할 수 있으며, 수락한 후에는 해당 요청을 취소하거나 삭제하기 전까지 다른 요청을 수락할 수 없습니다.
- 수락하거나 거절한 요청은 상태값을 변경할 수 있어야 합니다.

### 6. 요청 목록 조회

- 멘티는 자신이 보낸 매칭 요청과 그 상태(대기중, 수락, 거절)를 확인할 수 있어야 합니다.
- 멘티는 본인이 보낸 매칭 요청을 **삭제(취소)**할 수 있어야 합니다.

## 기술 요구사항

### 1. 앱 공통 요구사항

앱을 실행시키면 아래와 같은 URL로 접속할 수 있어야 합니다.

- 프론트엔드 앱 URL: http://localhost:3000
- 백엔드 앱 URL: http://localhost:8080
- 백엔드 API 엔드포인트 URL: http://localhost:8080/api

### 2. OpenAPI 설계 우선 원칙

- [API 명세](./mentor-mentee-api-spec.md)에 정의한 대로 작성한 [OpenAPI 문서](./openapi.yaml)를 제공합니다.
- 제공하는 OpenAPI 문서를 바탕으로 프론트엔드 UI 앱과 백엔드 API 앱을 구현해야 합니다.

### 3. JWT 클레임

- [RFC 7519](https://datatracker.ietf.org/doc/html/rfc7519#section-4.1)에서 정의한 `iss`, `sub`, `aud`, `exp`, `nbf`, `iat`, `jti` 클레임을 형식에 맞게 모두 추가해야 합니다.
- `name`, `email`, `role` 클레임을 반드시 포함해야 합니다. 이 때 `role` 클레임의 값은 `mentor` 또는 `mentee`입니다.
- `exp` 클레임은 발급 시각 기준 1시간의 유효기간을 갖습니다.

### 4. 프로필 이미지

- 프로필 이미지는 `.jpg` 또는 `.png` 형식만 허용합니다.
- 프로필 이미지는 정사각형 모양으로 최소 `500x500` 픽셀, 최대 `1000x1000` 픽셀입니다.
- 프로필 이미지의 크기는 최대 1MB입니다.
- 기본 프로필 이미지는 아래 플레이스홀더 이미지를 사용합니다.
  - 멘토: `https://placehold.co/500x500.jpg?text=MENTOR`
  - 멘티: `https://placehold.co/500x500.jpg?text=MENTEE`

### 5. 데이터베이스

- 데이터베이스의 종류는 자유롭게 선택할 수 있습니다.
- 최초 앱 실행시 데이터베이스를 초기화하고 필요한 테이블을 구성할 수 있어야 합니다.
- 멘토와 멘티는 같은 테이블을 사용합니다.
- 프로필 이미지도 데이터베이스에 저장합니다.

### 6. 백엔드 API

- 백엔드 API는 OpenAPI 문서를 자동으로 렌더링할 수 있는 링크를 제공해야 합니다. (예: `http://localhost:8080/openapi.json`)
- 백엔드 API는 Swagger UI 페이지를 렌더링할 수 있는 링크를 제공해야 합니다. (예: `http://localhost:8080/swagger-ui`)
- Swagger UI를 통해 OpenAPI 문서 페이지로 이동할 수 있어야 합니다.
- 백엔드 API URL인 `http://localhost:8080`으로 접속하면 자동으로 Swagger UI 화면으로 이동해야 합니다.

### 7. 보안

- 로컬 HTTPS 인증서는 사용하지 않습니다.
  - 즉, 로컬에서 `http://localhost:3000` 또는 `http://localhost:8080`으로 접속할 수 있으면 충분합니다.
- SQL 인젝션 공격에 대비해야 합니다.
- XSS 공격에 대비해야 합니다.
- OWASP TOP 10 취약점에 대비해야 합니다.

# 멘토-멘티 매칭 앱 API 명세서

- 모든 API 엔드포인트는 `http://localhost:8080/api/` 하위 경로를 기준으로 정의했습니다.
- 모든 인증이 필요한 요청에는 반드시 `Authorization: Bearer <token>` 헤더를 포함해야 합니다.
- 모든 요청과 응답은 JSON 형식의 개체를 주고 받아야 합니다.

## 1. 인증 (Authentication)

### POST `/signup`: 회원가입

#### **Request Body**

```jsonc
{
  "email": "user@example.com",
  "password": "password123",
  "name": "김멘토",
  "role": "mentor" // or "mentee"
}
```

#### **Response:**

- `201 Created`
- `400 Bad request`: 요청 payload 형식이 틀렸을 경우
- `500 Internal server error`: 처리중 에러가 생겼을 경우

### POST `/login`: 로그인

#### **Request Body:**

```jsonc
{
  "email": "user@example.com",
  "password": "password123"
}
```

#### **Response:**

- `200 OK`

    ```jsonc
    {
      "token": "JWT_TOKEN"
    }
    ```

- `400 Bad request`: 요청 payload 형식이 틀렸을 경우
- `401 Unauthorized`: 로그인에 실패했을 경우
- `500 Internal server error`: 처리중 에러가 생겼을 경우

## 2. 사용자 정보

### GET `/me`: 내 정보 조회

#### **Request Headers:**

- `Authorization: Bearer <token>`

#### **Response:**

- `200 OK`

    ```jsonc
    // 멘토
    {
      "id": 1,
      "email": "user@example.com",
      "role": "mentor",
      "profile": {
        "name": "Alice",
        "bio": "Frontend mentor",
        "imageUrl": "/images/mentor/1",
        "skills": ["React", "Vue"]
      }
    }
    ```

    ```jsonc
    // 멘티
    {
      "id": 10,
      "email": "user@example.com",
      "role": "mentee",
      "profile": {
        "name": "Alice",
        "bio": "Frontend mentor",
        "imageUrl": "/images/mentee/10"
      }
    }
    ```

- `401 Unauthorized`: 인증 실패했을 경우
- `500 Internal server error`: 처리중 에러가 생겼을 경우

### GET `/images/:role/:id`: 프로필 이미지

#### **Request Headers:**

- `Authorization: Bearer <token>`

#### **Response:**

- `200 OK`: 프로필 이미지 렌더링
- `401 Unauthorized`: 인증 실패했을 경우
- `500 Internal server error`: 처리중 에러가 생겼을 경우

### PUT `/profile`: 프로필 수정

#### **Request Headers:**

- `Authorization: Bearer <token>`

#### **Request Body:**

```jsonc
// 멘토
{
  "id": 1,
  "name": "Alice",
  "role": "mentor",
  "bio": "Frontend mentor",
  "image": "BASE64_ENCODED_STRING",
  "skills": ["React", "Vue"]
}
```

```jsonc
// 멘티
{
  "id": 21,
  "name": "Alice",
  "role": "mentee",
  "bio": "Frontend mentee",
  "image": "BASE64_ENCODED_STRING"
}
```

#### **Response:**

- `200 OK`

    ```jsonc
    // 멘토
    {
      "id": 1,
      "email": "user@example.com",
      "role": "mentor",
      "profile": {
        "name": "김앞단",
        "bio": "Frontend mentor",
        "imageUrl": "/images/mentor/1",
        "skills": ["React", "Vue"]
      }
    }
    ```

    ```jsonc
    // 멘티
    {
      "id": 21,
      "email": "user@example.com",
      "role": "mentee",
      "profile": {
        "name": "이뒷단",
        "bio": "Passionate backend developer",
        "imageUrl": "/images/mentee/21"
      }
    }
    ```

- `400 Bad request`: 요청 payload 형식이 틀렸을 경우
- `401 Unauthorized`: 인증 실패했을 경우
- `500 Internal server error`: 처리중 에러가 생겼을 경우

## 3. 멘토 리스트 조회

### GET `/mentors`: 멘토 전체 리스트 조회 (멘티 전용)

#### **Request Headers:**

- `Authorization: Bearer <token>`

#### **Query Parameters:**

- `skill=<sill_set>`

  > **NOTE**:
  > 
  > - 한 번에 한 가지 Skill Set만 검색할 수 있습니다. 예를 들어, `react` 또는 `spring` 처럼 키워드 하나만 검색할 수 있지, `react, spring` 처럼 두 개 이상의 키워드를 동시에 검색할 수 없습니다.
  > - 쿼리 파라미터를 제공하지 않으면 전체 멘토 리스트를 반환합니다.

- `order_by=<skill_or_name>`

  > **NOTE**:
  > 
  > - 다수의 멘토를 검색할 경우 skill 또는 name 을 기준으로 멘토 리스트를 오름차순으로 정렬합니다.
  > - 쿼리 파라미터를 제공하지 않으면 mentor ID 기준 오름차순으로 정렬합니다.

#### **Response:**

- `200 OK`

    ```jsonc
    // 조회 결과 없을 경우
    []
    ```

    ```jsonc
    // 조회 결과 있을 경우
    [
      {
        "id": 3,
        "email": "user@example.com",
        "role": "mentor",
        "profile": {
          "name": "김앞단",
          "bio": "Frontend mentor",
          "imageUrl": "/images/mentor/3",
          "skills": ["React", "Vue"]
        }
      },
      {
        "id": 4,
        "name": "이뒷단",
        "role": "mentor",
        "bio": "Backend mentor",
        "imageUrl": "/images/mentor/4",
        "skills": ["Spring Boot", "FastAPI"]
      }
    ]
    ```

- `401 Unauthorized`: 인증 실패했을 경우
- `500 Internal server error`: 처리중 에러가 생겼을 경우

## 4. 멘토 매칭 요청

### POST `/match-requests`: 매칭 요청 보내기 (멘티 전용)

#### **Request Headers:**

- `Authorization: Bearer <token>`

#### **Request Body:**

```jsonc
{
  "mentorId": 3,
  "menteeId": 4,
  "message": "멘토링 받고 싶어요!"
}
```

#### **Response:**

- `200 OK`

    ```jsonc
    {
      "id": 1,
      "mentorId": 3,
      "menteeId": 4,
      "message": "멘토링 받고 싶어요!",
      "status": "pending"
    }
    ```

- `400 Bad request`: 요청 payload 형식이 틀렸을 경우 또는 멘토가 존재하지 않을 경우
- `401 Unauthorized`: 인증 실패했을 경우
- `500 Internal server error`: 처리중 에러가 생겼을 경우

### GET `/match-requests/incoming`: 나에게 들어온 요청 목록 (멘토 전용)

#### **Request Headers:**

- `Authorization: Bearer <token>`

#### **Response:**

- `200 OK`

    ```jsonc
    [
      {
        "id": 11,
        "mentorId": 5,
        "menteeId": 1,
        "message": "멘토링 받고 싶어요!",
        "status": "pending"
      },
      {
        "id": 12,
        "mentorId": 5,
        "menteeId": 2,
        "message": "멘토링 받고 싶어요!",
        "status": "accepted"
      },
      {
        "id": 13,
        "mentorId": 5,
        "menteeId": 3,
        "message": "멘토링 받고 싶어요!",
        "status": "rejected"
      },
      {
        "id": 14,
        "mentorId": 5,
        "menteeId": 4,
        "message": "멘토링 받고 싶어요!",
        "status": "cancelled"
      }
    ]
    ```

- `401 Unauthorized`: 인증 실패했을 경우
- `500 Internal server error`: 처리중 에러가 생겼을 경우

### GET `/match-requests/outgoing`: 내가 보낸 요청 목록 (멘티 전용)

#### **Request Headers:**

- `Authorization: Bearer <token>`

#### **Response:**

- `200 OK`

    ```jsonc
    [
      {
        "id": 11,
        "mentorId": 1,
        "menteeId": 10,
        "status": "pending"
      },
      {
        "id": 12,
        "mentorId": 2,
        "menteeId": 10,
        "status": "accepted"
      },
      {
        "id": 13,
        "mentorId": 3,
        "menteeId": 10,
        "status": "rejected"
      },
      {
        "id": 14,
        "mentorId": 4,
        "menteeId": 10,
        "status": "cancelled"
      }
    ]
    ```

- `401 Unauthorized`: 인증 실패했을 경우
- `500 Internal server error`: 처리중 에러가 생겼을 경우

### PUT `/match-requests/:id/accept`: 요청 수락 (멘토 전용)

#### **Request Headers:**

- `Authorization: Bearer <token>`

#### **Response:**

- `200 OK`

    ```jsonc
    {
      "id": 11,
      "mentorId": 2,
      "menteeId": 1,
      "message": "멘토링 받고 싶어요!",
      "status": "accepted"
    }
    ```

- `404 Not found`: 매칭 요청 ID 값이 존재하지 않을 경우
- `401 Unauthorized`: 인증 실패했을 경우
- `500 Internal server error`: 처리중 에러가 생겼을 경우

### PUT `/match-requests/:id/reject`: 요청 거절 (멘토 전용)

#### **Request Headers:**

- `Authorization: Bearer <token>`

#### **Response:**

- `200 OK`

    ```jsonc
    {
      "id": 11,
      "mentorId": 2,
      "menteeId": 1,
      "message": "멘토링 받고 싶어요!",
      "status": "rejected"
    }
    ```

- `404 Not found`: 매칭 요청 ID 값이 존재하지 않을 경우
- `401 Unauthorized`: 인증 실패했을 경우
- `500 Internal server error`: 처리중 에러가 생겼을 경우

### DELETE `/match-requests/:id`: 요청 삭제/취소 (멘티 전용)

#### **Request Headers:**

- `Authorization: Bearer <token>`

#### **Response:**

- `200 OK`

    ```jsonc
    {
      "id": 11,
      "mentorId": 2,
      "menteeId": 12,
      "message": "멘토링 받고 싶어요!",
      "status": "cancelled"
    }
    ```

- `404 Not found`: 매칭 요청 ID 값이 존재하지 않을 경우
- `401 Unauthorized`: 인증 실패했을 경우
- `500 Internal server error`: 처리중 에러가 생겼을 경우

# 폴더 구조

```
src/
  api/
    auth.ts
    mentors.ts
    matchRequests.ts
  components/
    AuthForm.tsx
    MentorList.tsx
  pages/
    LoginPage.tsx
    SignupPage.tsx
    MentorListPage.tsx
    ProfilePage.tsx
  types/
    user.ts
    mentor.ts
    matchRequest.ts
  App.tsx
  main.tsx
```

# ✅ MentorConnect 요구사항 체크리스트

## 🟦 공통
- [ ] FastAPI(8080) + React TS(3000) + SQLite 조합
- [ ] Monorepo dev 스크립트(concurrently)로 front+back 동시 실행
- [ ] Swagger/OpenAPI 문서 및 Swagger UI 제공, 루트 리다이렉트

## 🟩 백엔드 (FastAPI)
- [ ] FastAPI 앱 초기화, 포트 8080, hot-reload dev 스크립트
- [ ] DB: users, profiles, match_requests 테이블 및 seed 스크립트
- [ ] 3계층 구조(router → service → repository)
- [ ] JWT 인증 (HS256, exp=1h, 필수 클레임)
- [ ] 회원가입 (`POST /api/signup`, bcrypt, 중복 이메일 400)
- [ ] 로그인 (`POST /api/login`, JWT 발급)
- [ ] 내 정보 조회 (`GET /api/me`)
- [ ] 프로필 수정 (`PUT /api/profile`)
- [ ] 멘토 목록 (`GET /api/mentors?skill=&order_by=`, skill 필터/정렬)
- [ ] 매칭 요청 생성 (`POST /api/match-requests`)
- [ ] 받은 요청 목록 (`GET /api/match-requests/incoming`)
- [ ] 보낸 요청 목록 (`GET /api/match-requests/outgoing`)
- [ ] 요청 수락/거절/취소 (`PUT /api/match-requests/{id}/accept|reject`, `DELETE /api/match-requests/{id}`)
- [ ] 프로필 이미지 업로드/검증 (형식·크기·픽셀, `/api/images/:role/:id`)
- [ ] 에러 응답 표준화 `{ code, message, detail }`
- [ ] SQL-i 방어(SQLAlchemy 바인딩), XSS sanitize, OWASP Top 10 체크
- [ ] Pydantic 모델, 타입 힌트, Depends 의존성 주입
- [ ] 코드 포맷: black, ruff
- [ ] pytest fixture 인메모리 sqlite, 통합/보안 테스트

## 🟦 프론트엔드 (React TypeScript, Vite)
- [ ] Vite react-ts 새 프로젝트, devServer 3000
- [ ] 폴더 구조: src/api, src/components, src/pages, src/types 등
- [ ] 타입 분리(user, mentor, matchRequest)
- [ ] API 모듈(auth, mentors, matchRequests)
- [ ] 회원가입/로그인 폼 및 페이지
- [ ] JWT 토큰 저장 및 API 헤더 자동 처리
- [ ] 내 정보/프로필 수정 페이지(이미지 업로드 포함)
- [ ] 멘토 리스트(필터/정렬/매칭 요청 버튼)
- [ ] 매칭 요청/수락/거절/취소 UI
- [ ] 표준 에러 처리 및 안내
- [ ] 프로필 이미지 미설정 시 플레이스홀더 처리
- [ ] XSS 등 입력값 sanitize
- [ ] 코드 포맷: ESLint, Prettier

## 🟧 프론트엔드-백엔드 연동 체크
- [ ] 프론트엔드 API baseURL이 백엔드(`/api`)로 올바르게 연결됨
- [ ] JWT 토큰 발급 후 모든 API 요청에 Authorization 헤더 자동 포함
- [ ] CORS 및 프록시 설정(vite.config 등)으로 개발 환경에서 cross-origin 문제 없음
- [ ] 프로필 이미지, 매칭 요청 등 파일/JSON 요청이 정상적으로 백엔드와 연동됨
- [ ] 에러 응답(코드/메시지/디테일) 프론트에서 표준 처리 및 안내
- [ ] 프론트에서 Swagger/OpenAPI 문서 접근 가능(개발 참고)
- [ ] 프론트/백엔드 동시 실행(dev script, concurrently 등)로 통합 개발 가능

---