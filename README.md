# PDF Parser MCP Service

基于FastMCP框架的PDF转Markdown解析服务，通过Model Context Protocol提供标准化接口。

## 功能特性
- 支持本地PDF文件和URL解析
- 可配置解析参数（DPI、页数范围等）
- 通过MCP协议标准化接口

## 快速开始
### 安装依赖
```bash
pip install -r requirements.txt

### 安装依赖
```json
{
  "mcpServers": {
    "textin-pdf-parser": {
      "isActive": false,
      "type": "stdio",
      "command": "python",
      "args": [
        "C:/Users/User/Desktop/mcp_pdf_parser.py"
      ],
      "env": {
        "TEXTIN_APP_ID": "xxxxxxxxxxx",
        "TEXTIN_APP_SECRET": "xxxxxxxxxx"
      },
      "name": "textin-pdf-parser"
    }
  }
}
