import os

# 1. 상위 입력/출력 폴더 설정
BASE_INPUT_FOLDER = "./scripts"        # 날짜별 폴더들이 들어있는 상위 폴더
BASE_OUTPUT_FOLDER = "./merged_scripts" # 합쳐진 txt 파일들이 저장될 상위 폴더


def process_date_folder(date_folder_name):
    """특정 날짜 폴더 내의 .txt 파일들을 카테고리별로 병합하는 함수"""
    input_date_path = os.path.join(BASE_INPUT_FOLDER, date_folder_name)
    output_date_path = os.path.join(BASE_OUTPUT_FOLDER, date_folder_name)

    # 해당 날짜의 .txt 파일 목록 가져오기
    txt_files = [f for f in os.listdir(input_date_path) if f.lower().endswith(".txt")]

    if not txt_files:
        print(f"📂 [{date_folder_name}] 텍스트 파일이 없습니다. 건너뜁니다.")
        return

    # 날짜별 출력 폴더 생성
    os.makedirs(output_date_path, exist_ok=True)

    # 카테고리별 그룹화
    # 예: "01_거주지_01_묘사.txt" -> category: "01_거주지", subtitle: "01_묘사"
    category_groups = {}

    for filename in sorted(txt_files):
        name_without_ext = os.path.splitext(filename)[0]
        parts = name_without_ext.split("_")

        # 파일명 분리 로직 (글자 수/길이에 관계없이 '_' 기준으로 분리)
        # 예: ['01', '거주지', '01', '묘사'] -> category: "01_거주지", subtitle: "01_묘사"
        if len(parts) >= 4:
            category = f"{parts[0]}_{parts[1]}"
            subtitle = "_".join(parts[2:])
        elif len(parts) >= 2:
            category = parts[0]
            subtitle = "_".join(parts[1:])
        else:
            category = "기타"
            subtitle = name_without_ext

        if category not in category_groups:
            category_groups[category] = []

        category_groups[category].append((subtitle, filename))

    print(f"📂 [{date_folder_name}] 총 {len(category_groups)}개 카테고리로 병합 중...")

    # 카테고리별 파일 생성 및 내용 병합
    for category, file_list in category_groups.items():
        output_filename = f"{category}.txt"
        output_filepath = os.path.join(output_date_path, output_filename)

        merged_content = []

        for subtitle, filename in file_list:
            file_path = os.path.join(input_date_path, filename)

            # UTF-8 또는 CP949 인코딩 읽기 처리
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read().strip()
            except UnicodeDecodeError:
                with open(file_path, "r", encoding="cp949") as f:
                    content = f.read().strip()

            # 소제목 구분선 작성
            header = f"=== [{subtitle}] ==="
            merged_content.append(f"{header}\n\n{content}\n\n" + "-" * 40 + "\n")

        # 병합된 내용 저장
        with open(output_filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(merged_content))

        print(f"  ✅ 생성 완료: {output_filename} ({len(file_list)}개 스크립트 포함)")


def batch_merge_all():
    if not os.path.exists(BASE_INPUT_FOLDER):
        print(f"❌ '{BASE_INPUT_FOLDER}' 폴더를 찾을 수 없습니다.")
        return

    # scripts 폴더 내부의 모든 날짜별 하위 폴더 검색
    entries = os.listdir(BASE_INPUT_FOLDER)
    date_folders = [
        entry for entry in entries
        if os.path.isdir(os.path.join(BASE_INPUT_FOLDER, entry))
    ]

    if not date_folders:
        print(f"⚠️ '{BASE_INPUT_FOLDER}' 폴더 안에 날짜별 하위 폴더가 없습니다.")
        return

    print(f"🚀 총 {len(date_folders)}개의 날짜 폴더를 순회하며 파일 병합을 시작합니다...\n")

    for date_folder in sorted(date_folders):
        process_date_folder(date_folder)
        print()

    print(f"🎉 모든 날짜 폴더의 병합 작업이 끝났습니다! '{BASE_OUTPUT_FOLDER}' 폴더에서 확인하세요.")


if __name__ == "__main__":
    batch_merge_all()