# **Mosaist**
[https://mosaist.org](https://mosaist.org)

# **FYI**
## **주요 디렉토리 및 파일.**
```
Mosaist
├── datasets: 학습, 검증, 테스트를 위한 데이터 셋 모음.
│   └── {dateset_name}
│       ├── images: 원본 이미지.
│       └── labels: 이미지에 대한 라벨.
├── inputs: 입력 버퍼처럼 사용하는 디렉토리.
│   ├── images: 입력 이미지 파일 모음.
│   └── videos: 입력 동영상 파일 모음.
├── outputs: 출력 버퍼처럼 사용하는 디렉토리.
│   ├── images: 출력 이미지 파일 모음.
│   └── videos: 출력 동영상 파일 모음.
├── server: 주요 서비스 로직 모음.
│   ├── back: 모자이크 처리 등 백엔드 구현 모음.
|   |   ├── api.py: 백엔드 HTTP API 구현.
|   |   ├── facial_stuffs.py: 얼굴 인식 구현.
|   |   ├── image_stuffs.py: 이미지 처리 구현.
|   |   ├── model_stuffs.py: 모델 학습 관련.
|   |   ├── socket_api.py: 백엔드 소켓 API 구현.
|   |   └── video_stuffs.py: 비디오 처리 구현.
│   ├── front: 프론트 구현 모음.
|   |   ├── api.py
|   |   └── api.py
│   └── proxy.py: 프록시 서버 구현.
├── yolov5: YOLOv5에 대한 코드 모음.
├── config.json: 전역 서버 설정 파일.
├── init.py: 초기 환경 구성 스크립트.
└── requirements.txt: 필요 라이브러리 모음.
```