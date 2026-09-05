import asyncio
import os
import edge_tts

# 1. 메인 입력/출력 폴더 설정
BASE_INPUT_FOLDER = "./scripts"  # 날짜별 폴더들이 들어있는 상위 폴더
BASE_OUTPUT_FOLDER = "./audio_outputs"  # 결과물 MP3가 저장될 상위 폴더

# 2. 오픽 추천 AI 목소리 선택 (한글/고유명사 및 영어 병행 추천)
VOICE = "en-US-AvaMultilingualNeural"

# 3. 재생 속도 설정
# "-10%" -> 약 0.9배속 (추천)
# "-20%" -> 약 0.8배속
RATE = "-10%"


async def convert_file(txt_filepath, mp3_filepath):
    """단일 텍스트 파일을 MP3로 변환하는 함수"""

    # 이미 MP3 파일이 존재하면 변환하지 않고 건너뜁니다.
    # (속도를 바꿔서 새로 만드시려면 audio_outputs 폴더 안의 기존 MP3들을 삭제 후 실행해 주세요!)
    if os.path.exists(mp3_filepath):
        print(f"  ⏭️ [건너뜀] 이미 생성되어 있음: {os.path.basename(mp3_filepath)}")
        return

    try:
        # UTF-8 또는 CP949 인코딩 자동 처리
        try:
            with open(txt_filepath, "r", encoding="utf-8") as f:
                text = f.read()
        except UnicodeDecodeError:
            with open(txt_filepath, "r", encoding="cp949") as f:
                text = f.read()

        if not text.strip():
            print(f"  ⚠️ [건너뜀] 내용이 비어있음: {os.path.basename(txt_filepath)}")
            return

        # '/' 끊어 읽기 슬래시 기호를 natural pause인 ','(쉼표)로 자동 변환
        text = text.replace("/", ",")

        # Edge-TTS 변환 및 속도(rate) 적용
        communicate = edge_tts.Communicate(text, VOICE, rate=RATE)
        await communicate.save(mp3_filepath)
        print(f"  ✅ [완료] {os.path.basename(txt_filepath)} -> {os.path.basename(mp3_filepath)} (속도: {RATE})")

    except Exception as e:
        print(f"  ❌ [오류] {os.path.basename(txt_filepath)}: {e}")


async def batch_process_all():
    if not os.path.exists(BASE_INPUT_FOLDER):
        os.makedirs(BASE_INPUT_FOLDER)
        print(f"📁 '{BASE_INPUT_FOLDER}' 폴더가 생성되었습니다.")
        return

    entries = os.listdir(BASE_INPUT_FOLDER)
    date_folders = [
        entry for entry in entries
        if os.path.isdir(os.path.join(BASE_INPUT_FOLDER, entry))
    ]

    if not date_folders:
        print(f"⚠️ '{BASE_INPUT_FOLDER}' 폴더 안에 날짜별 하위 폴더가 없습니다.")
        return

    print(f"🚀 총 {len(date_folders)}개의 날짜 폴더를 검사합니다... (목소리: {VOICE}, 속도: {RATE})\n")

    for date_folder in sorted(date_folders):
        input_date_path = os.path.join(BASE_INPUT_FOLDER, date_folder)
        output_date_path = os.path.join(BASE_OUTPUT_FOLDER, date_folder)

        os.makedirs(output_date_path, exist_ok=True)

        txt_files = [f for f in os.listdir(input_date_path) if f.lower().endswith(".txt")]

        if not txt_files:
            continue

        print(f"📂 [{date_folder}] 폴더 검사 및 변환 시작...")

        for filename in sorted(txt_files):
            txt_filepath = os.path.join(input_date_path, filename)
            mp3_filename = os.path.splitext(filename)[0] + ".mp3"
            mp3_filepath = os.path.join(output_date_path, mp3_filename)

            await convert_file(txt_filepath, mp3_filepath)
        print()

    print("🎉 속도가 적용된 MP3 변환 작업이 모두 완료되었습니다!")


if __name__ == "__main__":
    asyncio.run(batch_process_all())