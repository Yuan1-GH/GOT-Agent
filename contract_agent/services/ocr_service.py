import os
import subprocess
from pdf2image import convert_from_path

def extract_text_from_file(file_path: str) -> str:
    BASE_DIR = "/home/yuan/GOT-OCR2.0"  # 你的主目录
    OCR_SCRIPT = os.path.join(BASE_DIR, "GOT-OCR-2.0-master/GOT/demo/run_ocr_2.0.py")
    MODEL_PATH = "/mnt/y/GOT_weights/GOT_weights"
    file_path = os.path.abspath(file_path)

    # 1️⃣ 纯文本文件直接读取
    if file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    # 2️⃣ PDF → 转 PNG 再 OCR
    if file_path.endswith(".pdf"):
        print(f"[INFO] Detected PDF, converting to PNG...")
        output_dir = os.path.splitext(file_path)[0] + "_pages"
        os.makedirs(output_dir, exist_ok=True)

        try:
            pages = convert_from_path(file_path, dpi=300)
        except Exception as e:
            print(f"[ERROR] PDF conversion failed: {e}")
            return ""

        texts = []
        for i, page in enumerate(pages):
            img_path = os.path.join(output_dir, f"page_{i+1}.png")
            page.save(img_path, "PNG")
            print(f"[INFO] Saved: {img_path}")

            # 调用 OCR 获取结果
            text = extract_text_from_file(img_path)
            texts.append(text)
        print(f"[INFO] OCR finished for {len(pages)} pages")

        return "\n".join(texts)

    # 3️⃣ 图片文件（PNG / JPG / JPEG）
    if file_path.lower().endswith((".png", ".jpg", ".jpeg")):
        cmd = [
            "python3",
            OCR_SCRIPT,
            "--model-name", MODEL_PATH,
            "--image-file", file_path,
            "--type", "ocr"
        ]


        print(f"[INFO] Running OCR on {file_path}")
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,       # 关键！将输出解码为 str
            encoding="utf-8" # 防止中文乱码
        )

        if result.returncode != 0:
            print(f"[ERROR] OCR failed: {result.stderr}")
            return ""

        # result.stdout 就是模型输出的文本
        ocr_text = result.stdout.strip()
        print(f"[INFO] OCR finished, length={len(ocr_text)} chars\n")
        return ocr_text

    # 4️⃣ 不支持的文件类型
    print(f"[WARN] Unsupported file type: {file_path}")
    return ""

