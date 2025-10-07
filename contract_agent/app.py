from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel # 虽然此示例中不再使用，但保持导入
import markdown
import os # 导入 os 库用于路径操作和目录创建


from services.ocr_service import extract_text_from_file
from services.llm_service import run_contract_review
from services.parser_service import clean_ocr_text



app = FastAPI(title="合同审查智能代理前端")
templates = Jinja2Templates(directory="templates")

# 确保 'uploads' 目录存在，用于保存上传文件
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)




@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    提供带文件上传表单的首页。
    """
    # 渲染 templates/index.html
    return templates.TemplateResponse("index.html", {"request": request, "title": "合同文件上传"})




@app.post("/review", response_class=HTMLResponse)
async def review_contract(request: Request, file: UploadFile = File(...)):
    """
    处理文件上传，执行 OCR、文本清洗和 LLM 审查，然后显示结果。
    """
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    html_result = ""
    
    try:
        # 1. 保存文件
        contents = await file.read()
        with open(file_path, "wb") as f:
            f.write(contents)
            
        print(f"文件已保存至: {file_path}")

        # 2. OCR 提取文本 (替换为您的 extract_text_from_file)
        text = extract_text_from_file(file_path) 

        # 3. 文本清洗 (替换为您的 clean_ocr_text)
        text = clean_ocr_text(text)
        
        # 4. 调用模型执行 Prompt (替换为您的 run_contract_review)
        review_result_markdown = run_contract_review(text)

        # 5. 将 Markdown 结果转换为 HTML
        html_result = markdown.markdown(
            review_result_markdown, 
            extensions=["fenced_code", "tables"]
        )
    
    except Exception as e:
        # 错误处理
        html_result = f"## 处理出错\n\n文件处理过程中发生错误: `{e}`"
    finally:
        # 运行完成后，清理临时上传的文件 (可选)
        if os.path.exists(file_path):
            os.remove(file_path)
        pass


    # 6. 返回审查结果模板
    return templates.TemplateResponse(
        "review_result.html",
        {
            "request": request,
            "html_result": html_result,
            "file_name": file.filename,
            "original_text": text, # 新增
            "review_result_markdown": review_result_markdown, # 新增
        }
    )

if __name__ == "__main__":
    import uvicorn
    # 请确保您有 'templates/index.html' 和 'templates/review_result.html'
    print("🚀 启动合同审查代理前端...")
    uvicorn.run(app, host="0.0.0.0", port=8000)