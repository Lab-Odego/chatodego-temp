# Getting Started Odego server

## *Fastapi*

---

### `installation list`
```
% pip install fastapi
% pip install “uvicorn [standard]”
```

### `fastapi server start`
```
% uvicorn main:app --reload
```
<br>

**🔥 Uvicorn running at** <br>
> ► [http://127.0.0.1:8000](http://127.0.0.1:8000) <br>

**🔥 SwaggerUI (router test)** <br>
> ► [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) <br>

**🔥 SwaggerUI (read only)** <br>
> ► [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

<br>

## *Ngrok*

---

### `installation list`
```
% brew install ngrok/ngrok/ngrok
% ngrok config add-authtoken
```

### `fastapi에서 Ngrok서버 접속`
```
% ngrok http 8000
```
<br>

**🔥 ngrok 서버에 접속한 포트 목록 확인** <br>
> ► [https://dashboard.ngrok.com/tunnels/agents](https://dashboard.ngrok.com/tunnels/agents)

**🔥 ngrok tunnel request log** <br>
> [http://127.0.0.1:4040/](http://127.0.0.1:4040/)

<br>

## directory structure

---

```
odegotalk(odegoapi)
│
├── client
│   └── ... 
├── server
│   ├── routes
│   │   ├── chatbot_router.py
│   │   └── user_router.py (예정)
│   ├── schema 
│   │   ├── chatbot_schema.py (미완료-필요 유무 점검 중)
│   │   └── user_schema.py (예정)
│   └── crud (DB 연결 후 작성 예정)
│
├── database.py (DB 연결 후 작성 예정)
├── main.py
└── models.py (DB 연결 후 작성 예정)


```

| 파일명           |            내용            |
|---------------|:------------------------|
| `main.py`     | FastAPI 프로젝트의 전체적인 환경 설정 (지금은 fastapi 로컬 서버를 ngrok 서버에 올리는 코드 작성됨) |
| `~router.py` |       API 라우트 엔트포인트 동작 정의       |
| `~schema.py`    |        모델의 입출력 데이터 형식 정의         |
| `~crud.py`      |       데이터베이스 입출력 동작 정의       |