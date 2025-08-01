import fitz
import re
import os
from anthropic import Anthropic


def translate_pdf_overlay(pdf_path, translator_func):
    doc = fitz.open(pdf_path)
    
    # 한글 폰트 파일 경로
    font_path = "fonts/NotoSansKR-Regular.otf"
    
    # 폰트가 존재하는지 확인
    if not os.path.exists(font_path):
        print(f"Font file not found: {font_path}")
        return
    
    # 폰트 객체 생성
    try:
        font = fitz.Font(fontfile=font_path)
    except Exception as e:
        return
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        
        # 텍스트 블록들을 추출하되 위치 정보 보존
        text_dict = page.get_text("dict")
        
        for block in text_dict["blocks"]:
            if "lines" in block:  # 텍스트 블록
                for line in block["lines"]:
                    for span in line["spans"]:
                        original_text = span["text"].strip()
                        if original_text and len(original_text) > 1:
                            # 번역
                            translated_text = translator_func(original_text)
                            
                            # 원본 텍스트를 흰색으로 덮기
                            rect = fitz.Rect(span["bbox"])
                            page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1))
                            
                            # 번역된 텍스트를 같은 위치에 삽입
                            # baseline 위치 계산 (bottom_left에서 약간 위로)
                            text_point = fitz.Point(rect.x0, rect.y1 - 2)
                            
                            try:
                                # Font 객체를 사용하여 텍스트 삽입
                                page.insert_text(
                                    text_point,
                                    translated_text,
                                    fontsize=span["size"],
                                    font=font,
                                    color=(0, 0, 0)
                                )
                            except Exception as e:
                                print(f"Font insertion failed for '{translated_text}': {e}")
                                # 기본 폰트로 영어 텍스트 삽입
                                page.insert_text(
                                    text_point,
                                    "TRANSLATED",
                                    fontsize=span["size"],
                                    color=(0, 0, 0)
                                )
    
    doc.save(pdf_path.replace('.pdf', '_translated.pdf'))
    doc.close()


def translate_with_claude(text):
    """Claude API를 사용하여 텍스트를 한국어로 번역"""
    client = Anthropic(
        # API 키는 환경변수 ANTHROPIC_API_KEY에서 자동으로 읽음
        # 또는 api_key="your-api-key-here" 직접 설정
    )
    
    try:
        message = client.messages.create(
            model="claude-3-haiku-20240307",
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

