# Fofa 自然语言查询 Skill

使用自然语言查询 Fofa 网络空间搜索引擎，自动转换为 Fofa 查询语法并导出结果为 Excel 和摘要报告。

## 功能特性

- **自然语言理解**：将中文自然语言描述转换为 Fofa 查询语法
- **智能查询构建**：支持地理位置、服务类型、端口、协议等多维度查询
- **结果导出**：支持导出为 Excel (.xlsx) 和 CSV 格式
- **智能摘要**：自动生成查询结果的统计摘要和关键信息
- **配置管理**：支持配置 Fofa API 认证信息

## 安装

### 1. 克隆或下载本 Skill

```bash
cd /path/to/fofa-nl-query
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置 API 认证

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

## 使用方法

### 命令行模式

#### 基本查询

```bash
python -m src.main "查找广东地区的 OpenClaw 服务"
```

#### 指定输出格式

```bash
# 导出为 Excel
python -m src.main "查找中国境内运行 Nginx 的 Web 服务器" --format excel

# 导出为 CSV
python -m src.main "查找中国境内运行 Nginx 的 Web 服务器" --format csv

# 同时导出 Excel 和 CSV
python -m src.main "查找中国境内运行 Nginx 的 Web 服务器" --format both
```

#### 指定结果数量

```bash
python -m src.main "查找使用 WordPress 的网站" --max 200
```

#### 指定输出目录

```bash
python -m src.main "查找广东地区的 Web 服务" --output ./my_results
```

#### 交互模式

```bash
python -m src.main --interactive
```

### Python API 调用

```python
from src.main import FofaNLQuerySkill

# 初始化 Skill
skill = FofaNLQuerySkill(
    email="your-email@example.com",
    key="your-api-key"
)

# 执行查询
result = skill.execute(
    query="查找广东地区的 OpenClaw 服务",
    output_format='excel',  # 可选: 'excel', 'csv', 'both'
    max_results=100
)

if result['success']:
    print(f"查询成功! 共找到 {result['total']} 条结果")
    print(f"生成的文件: {result['files']}")
    print(f"摘要:\n{result['summary']}")
else:
    print(f"查询失败: {result['error']}")
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

## 输出文件说明

### Excel 文件 (.xlsx)

包含三个工作表：

1. **查询结果**：详细的资产信息
   - IP 地址
   - 端口
   - 协议
   - 地理位置（国家、省份、城市）
   - 服务类型
   - 页面标题
   - HTTP 头信息
   - Banner 信息
   - 证书信息

2. **统计摘要**：数据分析
   - 地理分布统计
   - 服务类型分布
   - 端口分布
   - 协议分布

3. **查询信息**：查询详情
   - 查询语句
   - 查询时间
   - 结果数量

### CSV 文件 (.csv)

包含所有字段的原始数据，可用于进一步数据处理。

### 摘要文件 (.txt)

包含查询结果的文本摘要报告，包括：

- 查询信息
- 统计概览
- 地理分布
- 服务分布
- Top 资产列表
- 安全提示

## 项目结构

```
fofa-nl-query/
├── src/
│   ├── __init__.py           # 包初始化
│   ├── nl_parser.py          # 自然语言解析器
│   ├── query_builder.py      # Fofa 查询构建器
│   ├── fofa_client.py        # Fofa API 客户端
│   ├── export_manager.py     # 导出管理器
│   ├── summary_generator.py  # 摘要生成器
│   └── main.py               # 主程序入口
├── .env.example              # 环境变量示例
├── requirements.txt          # 依赖列表
├── README.md                 # 项目说明
└── SKILL.md                  # Skill 说明文档
```

## 核心组件说明

### NLParser（自然语言解析器）

将用户的自然语言查询解析为结构化的查询实体，支持识别：

- 地理位置（省份、国家、区域）
- 服务类型（Web 服务器、数据库、CMS 等）
- 端口号
- 协议类型
- 技术指纹

### QueryBuilder（查询构建器）

将解析后的实体转换为 Fofa 查询语法，支持：

- 多条件组合（AND / OR）
- 字段映射（country、region、port、protocol 等）
- 查询语句解释

### FofaClient（API 客户端）

处理与 Fofa API 的通信，支持：

- 单次查询
- 自动分页获取大量结果
- 账号信息查询
- 错误处理

### ExportManager（导出管理器）

处理查询结果的导出，支持：

- Excel 格式（多工作表、格式化）
- CSV 格式
- 自动调整列宽
- 统计摘要生成

### SummaryGenerator（摘要生成器）

生成查询结果的文本摘要，包括：

- 统计概览
- 地理分布分析
- 服务类型分析
- 端口分布分析
- 安全风险提示

## 配置说明

### 环境变量

| 变量名 | 说明 | 必需 |
|--------|------|------|
| FOFA_EMAIL | Fofa 账号邮箱 | 是 |
| FOFA_KEY | Fofa API Key | 是 |
| FOFA_MAX_RESULTS | 默认最大结果数 | 否 |
| FOFA_OUTPUT_DIR | 默认输出目录 | 否 |

### 命令行参数

| 参数 | 简写 | 说明 | 默认值 |
|------|------|------|--------|
| query | - | 自然语言查询语句 | - |
| --format | -f | 输出格式 | excel |
| --max | -m | 最大结果数 | 100 |
| --output | -o | 输出目录 | ./fofa_results |
| --email | -e | Fofa 邮箱 | 环境变量 |
| --key | -k | Fofa API Key | 环境变量 |
| --interactive | -i | 交互模式 | False |

## 注意事项

1. **API 限制**：Fofa API 有查询频率和结果数量限制，请参考 Fofa 官方文档
2. **数据安全**：查询结果可能包含敏感信息，请妥善保管
3. **合规使用**：请遵守相关法律法规和 Fofa 使用条款
4. **网络要求**：需要能够访问 Fofa API 的网络环境

## 依赖项

- Python 3.8+
- requests >= 2.28.0
- openpyxl >= 3.0.10
- pandas >= 1.5.0
- jieba >= 0.42.1
- python-dotenv >= 0.19.0

## 故障排除

### 认证失败

```
错误: API 认证失败，请检查 email 和 key 是否正确
```

解决方案：

1. 检查 `.env` 文件或环境变量是否正确设置
2. 确认 Fofa 账号是否有效
3. 检查 API Key 是否正确

### 查询超时

```
网络请求失败: 请求超时
```

解决方案：

1. 检查网络连接
2. 减少查询结果数量
3. 稍后重试

### 未找到结果

```
查询成功! 共找到 0 条结果
```

可能原因：

1. 查询条件过于严格
2. Fofa 数据库中无匹配数据
3. 自然语言解析错误（请检查生成的 Fofa 查询语句）

## 参考资料

- Fofa 官网：https://fofa.info
- Fofa API 文档：https://fofa.info/api
- Fofa 规则与指纹：https://fofa.info/library

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！
