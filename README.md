# **Front-Test**
[Front-Test](https://mosaist.github.io/Mosaist/front/templates/html/index.html)

# **FYI**
## **주요 디렉토리 및 파일.**
```
YOLO
├── datasets: 학습, 검증, 테스트를 위한 데이터셋.
│   └── {dateset_name}
│       ├── images: 원본 이미지.
│       └── labels: 이미지에 대한 라벨.
├── environments: 파이썬 가상 환경 설정 파일.
├── image_handling: 이미지/동영상 입출력 및 처리 관련 코드 모음.
│   ├── api.py: HTTP를 이용해 사용할 수 있도록 API 제공.
│   ├── config.py: 기본 디렉토리 및 포트 등 설정 모음.
│   ├── facial_stuffs.py: 얼굴 인식 등 인공지능 모델과 관련된 코드 모음.
│   ├── image_stuffs.py: 이미지 전처리 및 후처리와 관련된 코드 모음.
│   ├── model_stuffs.py: 인공지능 모델 관련 코드 모음.
│   └── video_stuffs.py: 동영상 전처리 및 후처리와 관련된 코드 모음.
├── inputs: 입력 버퍼처럼 사용하는 디렉토리.
│   ├── images: 이미지 파일 모음.
│   └── videos: 동영상 파일 모음.
├── outputs: 출력 버퍼처럼 사용하는 디텍토리.
│   ├── images: 이미지 파일 모음.
│   └── videos: 동영상 파일 모음.
├── tests: 코드 테스트 파일 모음.
├── yolov5: YOLOv5에 대한 코드 모음.
│   ├── test.py: 학습 테스트 시 사용.
│   ├── train.py: 모델 학습 시 사용.
│   └── val.py: 모델 검증 시 사용.
└── yolov7: YOLOv7에 대한 코드 모음.

+ 기타 Node 관련 파일. (구조 개편 필요)
```

입력은 파일 시스템을 이용.  
입출력 전용 디렉토리 지정 및 해당 디렉토리를 버퍼처럼 사용.  

# **To-Do**
## AI 모델 관련 
동영상에 소리 처리 추가.  
실시간 모델 변경 시 메모리 부족 해결.  
라벨에서 적절한 영역을 따는 방안 모색. (얼굴의 경우 미리 학습된 모델을 이용해 라벨링)  

## API 관련
api에서 동영상과 관련하여 디스크를 사용하지 않고 처리하는 방법 추가.  

## 기타
폴더 구조 개편.  
README.md 갱신.  
프로젝트 초기 설정 방법 추가.  
