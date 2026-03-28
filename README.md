# Fofa 自然语言查询 Skill

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Fofa](https://img.shields.io/badge/Fofa-API-orange.svg)](https://fofa.info)

使用自然语言查询 Fofa 网络空间搜索引擎，自动转换为 Fofa 查询语法并导出结果为 Excel 和摘要报告。

## 功能特性

- **自然语言理解**：将中文自然语言描述转换为 Fofa 查询语法
- **智能查询构建**：支持地理位置、服务类型、端口、协议等多维度查询
- **结果导出**：支持导出为 Excel (.xlsx) 和 CSV 格式
- **智能摘要**：自动生成查询结果的统计摘要和关键信息
- **配置管理**：支持配置 Fofa API 认证信息

## 快速开始

### 安装

```bash
# 克隆仓库
git clone https://github.com/1156494497/fofa-query-skill.git
cd fofa-query-skill/skills/fofa-nl-query

# 安装依赖
pip install -r requirements.txt
```

### 配置

复制 `.env.example` 为 `.env` 并填写你的 Fofa API 认证信息：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
FOFA_EMAIL=your-email@example.com
FOFA_KEY=your-api-key
```

或者设置环境变量：

```bash
export FOFA_EMAIL="your-email@example.com"
export FOFA_KEY="your-api-key"
```

### 使用示例

#### 基本查询

```bash
python -m src.main "查找广东地区的 OpenClaw 服务"
```

#### 复合查询

```bash
python -m src.main "查找中国境内运行 Nginx 的 Web 服务器，端口为 80 或 443"
```

#### 指定输出格式

```bash
# 导出为 Excel（默认）
python -m src.main "查找使用 WordPress 的网站" --format excel

# 导出为 CSV
python -m src.main "查找使用 WordPress 的网站" --format csv

# 同时导出 Excel 和 CSV
python -m src.main "查找使用 WordPress 的网站" --format both
```

#### 指定结果数量

```bash
python -m src.main "查找暴露的 Redis 服务" --max 500
```

#### 交互模式

```bash
python -m src.main --interactive
```

## 支持的查询类型

### 地理位置查询

- **省份/城市**：广东、北京、上海、浙江等
- **国家**：中国、美国、日本、韩国等
- **区域**：亚洲、欧洲、北美洲等

示例：

```bash
python -m src.main "查找广东地区的 Web 服务器"
python -m src.main "查找中国境内的数据库服务"
python -m src.main "查找美国的云服务器"
```

### 服务类型查询

- **Web 服务器**：Nginx、Apache、IIS、Tomcat
- **数据库**：MySQL、MongoDB、Redis、PostgreSQL
- **中间件**：WebLogic、JBoss、WebSphere
- **CMS**：WordPress、Drupal、Joomla
- **框架**：Spring、Django、Laravel、ThinkPHP

示例：

```bash
python -m src.main "查找使用 Nginx 的网站"
python -m src.main "查找暴露的 Redis 服务"
python -m src.main "查找使用 WordPress 的博客"
```

### 端口查询

示例：

```bash
python -m src.main "查找 80 端口的 Web 服务"
python -m src.main "查找 3306 端口的数据库"
python -m src.main "查找 22 端口的 SSH 服务"
```

### 协议查询

示例：

```bash
python -m src.main "查找 HTTP 服务"
python -m src.main "查找 HTTPS 网站"
python -m src.main "查找 SSH 服务"
```

### 复合查询

示例：

```bash
python -m src.main "查找广东地区使用 Nginx 的 Web 服务器，端口为 80 或 443"
python -m src.main "查找中国境内暴露的 MySQL 和 Redis 数据库"
python -m src.main "查找使用 WordPress 且运行在美国的服务器"
```

## Python API 使用

```python
from skills.fofa-nl-query.src.main import FofaNLQuerySkill

# 初始化 Skill
skill = FofaNLQuerySkill(
    email="your-email@example.com",
    key="your-api-key"
)

# 执行查询
result = skill.execute(
    query="查找广东地区的 OpenClaw 服务",
    output_format='excel',
    max_results=100
)

if result['success']:
    print(f"查询成功! 共找到 {result['total']} 条结果")
    print(f"生成的文件: {result['files']}")
    print(f"摘要:\n{result['summary']}")
else:
    print(f"查询失败: {result['error']}")
```

## 输出文件说明

### Excel 文件 (.xlsx)

包含三个工作表：

1. **查询结果**：详细的资产信息
   - IP 地址、端口、协议
   - 地理位置（国家、省份、城市）
   - 服务类型、页面标题
   - HTTP 头信息、Banner 信息

2. **统计摘要**：数据分析
   - 地理分布统计
   - 服务类型分布
   - 端口分布统计

3. **查询信息**：查询详情
   - 查询语句、查询时间
   - 结果数量

### CSV 文件 (.csv)

包含所有字段的原始数据，可用于进一步数据处理。

### 摘要文件 (.txt)

包含查询结果的文本摘要报告，包括统计概览、地理分布、安全提示等。

## 项目结构

```
fofa-query-skill/
├── skills/fofa-nl-query/
│   ├── src/
│   │   ├── __init__.py
│   │   ├── nl_parser.py
│   │   ├── query_builder.py
│   │   ├── fofa_client.py
│   │   ├── export_manager.py
│   │   ├── summary_generator.py
│   │   └── main.py
│   ├── .env.example
│   ├── requirements.txt
│   └── README.md
├── .monkeycode/specs/
│   └── 260328-fofa-nl-query/
│       ├── requirements.md
│       ├── design.md
│       └── tasklist.md
└── README.md
```

## 核心组件

### NLParser（自然语言解析器）

将用户的自然语言查询解析为结构化的查询实体。

### QueryBuilder（查询构建器）

将解析后的实体转换为 Fofa 查询语法。

### FofaClient（API 客户端）

处理与 Fofa API 的通信。

### ExportManager（导出管理器）

处理查询结果的导出。

### SummaryGenerator（摘要生成器）

生成查询结果的文本摘要。

## 依赖项

- Python 3.8+
- requests >= 2.28.0
- openpyxl >= 3.0.10
- pandas >= 1.5.0
- jieba >= 0.42.1
- python-dotenv >= 0.19.0

## 注意事项

1. **API 限制**：Fofa API 有查询频率和结果数量限制
2. **数据安全**：查询结果可能包含敏感信息，请妥善保管
3. **合规使用**：请遵守相关法律法规和 Fofa 使用条款
4. **网络要求**：需要能够访问 Fofa API 的网络环境

## 参考资料

- Fofa 官网：https://fofa.info
- Fofa API 文档：https://fofa.info/api
- Fofa 规则与指纹：https://fofa.info/library

## 许可证

MIT License

## 作者

- GitHub: [@1156494497](https://github.com/1156494497)

---

如果这个项目对你有帮助，请给个 Star 支持一下！
