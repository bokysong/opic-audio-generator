Markdown
# 🎙️ OPIc Audio Generator (with Edge-TTS)

> **오픽(OPIc) 스피킹 연습용 텍스트 스크립트를 자연스러운 AI 발화 MP3 음원으로 일괄 자동 변환하는 파이썬 파이프라인**  
> Google Gemini와의 페어 프로그래밍을 통해 개발되었습니다.

---

## 📌 Background
오픽(OPIc) 시험 대비의 핵심은 **"작성한 스크립트를 귀로 반복해서 듣고 따라 말하는 섀도잉(Shadowing)"** 입니다.  
하지만 날짜별·문항별로 작성한 수많은 텍스트 파일들을 무료 TTS 웹사이트에 일일이 복사·붙여넣기하여 음원을 다운로드하는 과정에서 심한 작업 병목이 발생했습니다.

컴퓨터 앞에서의 단순 반복 수작업을 줄이고 학습 효율을 극대화하기 위해, **로컬 텍스트 파일을 순회하여 스피킹 훈련에 최적화된 MP3로 일괄 변환하는 자동화 스크립트**를 제작했습니다.

---

## ✨ Key Features
- **비동기 고속 일괄 변환 (`asyncio` + `edge-tts`)**: 수십 개의 텍스트 파일도 대기 시간 없이 빠르게 MP3로 변환
- **자연스러운 끊어 읽기(Pause) 지원**: 
  - 스크립트 작성 시 호흡을 위해 표시한 슬래시(`/`)를 TTS 엔진이 숨을 고를 수 있도록 쉼표(`,`)로 자동 치환
- **스피킹 맞춤형 음성 설정**:
  - Voice: 다국어 및 발화가 자연스러운 `en-US-AvaMultilingualNeural` 엔진 사용
  - Rate: 섀도잉 발음 훈련에 최적화된 0.9배속(`-10%`) 기본 적용
- **스마트 캐싱 & 인코딩 방어**:
  - 이미 생성된 MP3 파일은 자동으로 건너뛰어(Skip) 불필요한 중복 렌더링 방지
  - `UTF-8` 및 `CP949` 자동 분기 처리로 윈도우/맥 환경의 텍스트 인코딩 충돌 방지

---

## 📁 Directory Structure

```text
.
├── scripts/                  # 입력: 날짜별 스크립트 폴더 (.gitignore 제외)
│   └── YYYY-MM-DD/
│       └── 01_주제_01_묘사.txt
├── audio_outputs/            # 출력: 변환된 MP3 음원 폴더 (.gitignore 제외)
│   └── YYYY-MM-DD/
│       └── 01_주제_01_묘사.mp3
├── main.py                   # 변환 실행 스크립트
├── .gitignore
└── README.md
```

🔒 Privacy Note: 실제 개인 학습용 오픽 스크립트와 생성된 MP3 음원 파일은 개인정보 보호를 위해 .gitignore로 제외되어 있습니다.

## 🚀 Getting Started
1. Requirements
Python 3.8 이상 환경에서 실행합니다.

    ```Bash
    pip install edge-tts
    ```

2. Folder Setup & Script Preparation
scripts 폴더 내부에 날짜별(또는 주제별) 하위 폴더를 만듭니다.

    * 하위 폴더 안에 .txt 형식으로 스크립트를 작성합니다.

    * Tip: 문장 중간에 쉬어갈 부분에 /를 넣으면 음원이 자연스럽게 끊어 읽어줍니다.

    ```Plaintext
    I live in an apartment / with my family. / It has three rooms / and a cozy living room.
    ```
3. Run
    ```Bash
    python main.py
    ```
    실행이 완료되면 audio_outputs/ 폴더에 동일한 구조로 MP3 파일이 생성됩니다.

#### 🛠 Tech Stack

Language: Python 3

Libraries: edge-tts, asyncio, os

AI Pair Programmer: Google Gemini
