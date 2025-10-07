import re

def clean_ocr_text(raw_text):
    """
    对OCR原始文本进行清洗和主要信息提取
    """
    text = re.sub(r'\s+', ' ', raw_text)
    text = text.replace('<imagepad>', '')
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = text.replace('system You should follow the instructions carefully and explain your answers in detailuser  OCR assistant', '')

    return text    
