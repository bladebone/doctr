import os

import fitz
from anthropic import Anthropic
from dotenv import load_dotenv

# .env 파일에서 환경변수 로드
load_dotenv()
api_key = os.getenv('ANTHROPIC_API_KEY')
assert api_key

# 한글 폰트 파일 경로
font_path = "fonts/NotoSerifKR-Regular.ttf"
assert os.path.exists(font_path)
font = fitz.Font(fontfile=font_path)


def translate_pdf_overlay(pdf_path, translator_func):
    doc = fitz.open(pdf_path)

    for page_num in range(len(doc)):
        page = doc[page_num]

        # 텍스트 블록들을 추출하되 위치 정보와 스타일 정보 보존
        text_dict = page.get_text("dict")

        for block in text_dict["blocks"]:
            if "lines" in block:  # 텍스트 블록
                for line in block["lines"]:
                    for span in line["spans"]:
                        original_text = span["text"].strip()
                        if original_text and len(original_text) > 1:
                            # 번역
                            translated_text = translator_func(original_text)

                            # 원본 텍스트의 스타일 정보 추출
                            rect = fitz.Rect(span["bbox"])
                            font_size = span["size"]
                            # 색상을 0-1 범위의 RGB 튜플로 변환
                            color_int = span["color"]
                            text_color = (
                                ((color_int >> 16) & 255) / 255.0,  # Red
                                ((color_int >> 8) & 255) / 255.0,  # Green
                                (color_int & 255) / 255.0  # Blue
                            )

                            print(f"Original: '{original_text}' -> Translated: '{translated_text[:50]}...'")
                            print(f"Font size: {font_size}, Color: {text_color}, Position: {rect}")

                            # 원본 텍스트를 흰색으로 덮기 (스타일 보존을 위해)
                            page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1))

                            # 번역된 텍스트를 원본과 동일한 스타일로 삽입
                            text_point = fitz.Point(rect.x0, rect.y1 - 2)

                            # 폰트 크기를 한 단계 줄임 (최소 8pt 유지)
                            reduced_font_size = max(8.0, font_size - 2.0)

                            try:
                                page.insert_font(fontname="NotoSerifKR", fontfile=font_path)
                                page.insert_text(
                                    text_point,
                                    translated_text,
                                    fontsize=reduced_font_size,
                                    fontname="NotoSerifKR",
                                    color=text_color  # 원본 색상 사용
                                )
                                print(f"Text insertion successful (font size: {font_size} -> {reduced_font_size})")
                            except Exception as e:
                                print(f"Font insertion failed for '{translated_text[:30]}...': {e}")
                                # 기본 폰트로 폴백하되 원본 색상과 줄어든 크기 보존
                                page.insert_text(
                                    text_point,
                                    "TRANSLATED",
                                    fontsize=reduced_font_size,
                                    color=text_color
                                )

    doc.save(pdf_path.replace('.pdf', '_translated.pdf'))
    doc.close()


def translate_with_claude(text):
    """Claude API를 사용하여 텍스트를 한국어로 번역"""

    client = Anthropic(api_key=api_key)

    try:
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            temperature=0.0,
            max_tokens=1000,
            messages=[
                {
                    "role": "user",
                    "content": f"다음 텍스트를 한국어로 번역해주세요. 번역된 텍스트만 답변해주세요:\n\n{text}"
                }
            ]
        )
        return message.content[0].text.strip()
    except Exception as e:
        print(f"Translation failed for '{text}': {e}")
        return text  # 번역 실패시 원본 텍스트 반환


translate_pdf_overlay("1.pdf", translate_with_claude)
