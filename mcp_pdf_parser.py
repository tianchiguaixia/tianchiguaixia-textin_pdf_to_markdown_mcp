from mcp.server.fastmcp import FastMCP
import requests
import json
from typing import Optional

mcp = FastMCP("PDF Parser Service")

def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

@mcp.tool()
def parse_pdf(
    file_path: str,
    app_id: str,  # 新增：调用时传入的app_id参数
    app_secret: str,  # 新增：调用时传入的app_secret参数
    is_url: bool = False,
    pdf_pwd: Optional[str] = None,  # 使用Optional明确表示可为None
    dpi: int = 144,
    page_start: int = 0,
    page_count: int = 1000,
    table_flavor: str = 'md',
    parse_mode: str = 'scan'
) -> dict:
    """
    PDF转Markdown工具
    :param file_path: PDF文件路径或URL
    :param app_id: TextIn应用的APP ID
    :param app_secret: TextIn应用的Secret Code
    :param is_url: 是否为URL
    :param pdf_pwd: PDF密码(可选)
    :param dpi: 分辨率(默认144)
    :param page_start: 起始页(默认0)
    :param page_count: 解析页数(默认1000)
    :param table_flavor: 表格格式(默认'md')
    :param parse_mode: 解析模式(默认'scan')
    :return: 解析结果
    """
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
        'x-ti-app-id': app_id,  # 使用传入的app_id
        'x-ti-secret-code': app_secret  # 使用传入的app_secret
    }
    
    url = 'https://api.textin.com/ai/service/v1/pdf_to_markdown'
    
    if is_url:
        image = file_path
        headers['Content-Type'] = 'text/plain'
    else:
        image = get_file_content(file_path)
        headers['Content-Type'] = 'application/octet-stream'

    resp = requests.post(url, data=image, headers=headers, params=options)
    return json.loads(resp.text)

if __name__ == "__main__":
    mcp.run(transport='stdio')
