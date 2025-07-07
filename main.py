from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

# 1. 初始化 FastAPI 应用（核心入口）
app = FastAPI(
    title="基础 FastAPI 应用",
    description="包含必备组件的最小化框架",
    version="1.0.0"
)

# 2. 静态文件托管（可选但常用）
# 用于存放 CSS、JavaScript、图片等前端资源
app.mount("/static", StaticFiles(directory="static"), name="static")

# 3. 模板引擎配置（可选但常用）
# 用于渲染 HTML 页面
templates = Jinja2Templates(directory="templates")

# 4. 数据模型定义（API 输入输出验证）
class Item(BaseModel):
    name: str
    price: float
    is_available: bool = False  # 可选字段

# 5. 基础路由定义
# 根路径 - 简单响应
@app.get("/")
async def read_root():
    """根路径默认响应"""
    return {"message": "Hello, FastAPI!"}

# 带参数的路径
@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    """带路径参数和查询参数的示例"""
    return {"item_id": item_id, "query": q}

# 接收 JSON 数据的 POST 请求
@app.post("/items/")
async def create_item(item: Item):
    """创建项目（演示请求体验证）"""
    return {"item_name": item.name, "item_price": item.price, "tax": item.price * 0.1}

# 渲染 HTML 页面（使用模板引擎）
@app.get("/page", response_class=HTMLResponse)
async def read_page(request: Request):
    """演示 HTML 页面渲染"""
    return templates.TemplateResponse(
        "index.html",  # 模板文件路径
        {"request": request, "title": "FastAPI 基础页面"}  # 传递给模板的数据
    )

# 6. 应用启动入口
if __name__ == "__main__":
    import uvicorn
    # 用 uvicorn 启动服务
    uvicorn.run(
        app="main:app",  # 应用入口
        host="0.0.0.0",  # 允许外部访问
        port=8666,       # 端口
        reload=True      # 开发模式自动重载
    )
