from mcp.server.fastmcp import FastMCP
import requests
import json
import os
from typing import Optional

mcp = FastMCP("PDF Parser Service")

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

@mcp.tool()
def parse_pdf(
    file_path: str,
    is_url: bool = False,
    pdf_pwd: Optional[str] = None,
    dpi: int = 144,
    page_start: int = 0,
    page_count: int = 1000,
    table_flavor: str = 'md',
    parse_mode: str = 'scan'
) -> dict:
    """
    PDF转Markdown工具
    :param file_path: PDF文件路径或URL
    :param is_url: 是否为URL
    :param pdf_pwd: PDF密码(可选)
    :param dpi: 分辨率(默认144)
    :param page_start: 起始页(默认0)
    :param page_count: 解析页数(默认1000)
    :param table_flavor: 表格格式(默认'md')
    :param parse_mode: 解析模式(默认'scan')
    :return: 解析结果
    """
    # 从环境变量获取凭证
    app_id = os.getenv("TEXTIN_APP_ID")
    app_secret = os.getenv("TEXTIN_APP_SECRET")
    if not app_id or not app_secret:
        return {"error": "Missing TEXTIN_APP_ID or TEXTIN_APP_SECRET in environment variables"}

    options = {
        'pdf_pwd': pdf_pwd,
        'dpi': dpi,
        'page_start': page_start,
        'page_count': page_count,
        'apply_document_tree': 1,
        'markdown_details': 1,
        'page_details': 0,
        'table_flavor': table_flavor,
        'get_image': 'none',
        'parse_mode': parse_mode
    }
    
    headers = {
        'x-ti-app-id': app_id,
        'x-ti-secret-code': app_secret
    }
    
    url = 'https://api.textin.com/ai/service/v1/pdf_to_markdown'
    
    if is_url:
        image = file_path
        headers['Content-Type'] = 'text/plain'
    else:
        image = get_file_content(file_path)
        headers['Content-Type'] = 'application/octet-stream'

    try:
        resp = requests.post(url, data=image, headers=headers, params=options)
        resp.raise_for_status()
        return json.loads(resp.text)
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run(transport='stdio')
