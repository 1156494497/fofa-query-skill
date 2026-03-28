# Fofa 自然语言查询 Skill 开发任务列表

## 项目信息

- **Feature Name**: fofa-nl-query
- **Created**: 2025-03-28
- **Status**: 已完成

## 任务列表

### Phase 1: 核心组件开发

#### 1.1 自然语言解析器 (NLParser)
- [x] 创建 NLParser 类结构
- [x] 实现地理位置实体识别
- [x] 实现服务类型实体识别
- [x] 实现端口信息识别
- [x] 实现协议信息识别
- [x] 实现查询意图识别
- [x] 实现数量限制提取
- [x] 编写单元测试

**状态**: 已完成
**文件**: `src/nl_parser.py`

#### 1.2 查询构建器 (QueryBuilder)
- [x] 创建 QueryBuilder 类结构
- [x] 实现地理位置查询条件构建
- [x] 实现服务类型查询条件构建
- [x] 实现端口查询条件构建
- [x] 实现协议查询条件构建
- [x] 实现多条件组合逻辑
- [x] 实现查询语句解释功能
- [x] 编写单元测试

**状态**: 已完成
**文件**: `src/query_builder.py`

#### 1.3 Fofa API 客户端 (FofaClient)
- [x] 创建 FofaClient 类结构
- [x] 实现 API 认证功能
- [x] 实现单次查询功能
- [x] 实现自动分页功能
- [x] 实现账号信息查询
- [x] 实现认证检查功能
- [x] 添加错误处理机制
- [x] 编写单元测试

**状态**: 已完成
**文件**: `src/fofa_client.py`

### Phase 2: 输出处理

#### 2.1 导出管理器 (ExportManager)
- [x] 创建 ExportManager 类结构
- [x] 实现 Excel 导出功能
  - [x] 查询结果工作表
  - [x] 统计摘要工作表
  - [x] 查询信息工作表
  - [x] 格式化样式
- [x] 实现 CSV 导出功能
- [x] 实现同时导出两种格式
- [x] 实现自动调整列宽
- [x] 编写单元测试

**状态**: 已完成
**文件**: `src/export_manager.py`

#### 2.2 摘要生成器 (SummaryGenerator)
- [x] 创建 SummaryGenerator 类结构
- [x] 实现文本摘要生成
  - [x] 统计概览
  - [x] 地理分布统计
  - [x] 服务分布统计
  - [x] 端口分布统计
  - [x] Top 资产列表
  - [x] 安全提示
- [x] 实现 Markdown 摘要生成
- [x] 编写单元测试

**状态**: 已完成
**文件**: `src/summary_generator.py`

### Phase 3: 主程序和接口

#### 3.1 主程序 (main.py)
- [x] 创建 FofaNLQuerySkill 主类
- [x] 实现 execute 方法
- [x] 实现交互模式
- [x] 实现命令行参数解析
- [x] 添加进度显示
- [x] 添加错误处理

**状态**: 已完成
**文件**: `src/main.py`

#### 3.2 包初始化
- [x] 创建 `__init__.py`
- [x] 定义版本信息
- [x] 导出主要类

**状态**: 已完成
**文件**: `src/__init__.py`

### Phase 4: 配置和文档

#### 4.1 配置文件
- [x] 创建 requirements.txt
- [x] 创建 .env.example
- [x] 验证依赖版本

**状态**: 已完成
**文件**: 
- `requirements.txt`
- `.env.example`

#### 4.2 文档编写
- [x] 编写 SKILL.md
- [x] 编写 README.md
- [x] 编写使用示例
- [x] 编写故障排除指南

**状态**: 已完成
**文件**: 
- `SKILL.md`
- `README.md`

### Phase 5: 需求规格文档

#### 5.1 需求文档
- [x] 编写引言和词汇表
- [x] 编写功能性需求（7个需求）
- [x] 编写非功能性需求
- [x] 使用 EARS 模式编写 Acceptance Criteria

**状态**: 已完成
**文件**: `.monkeycode/specs/260328-fofa-nl-query/requirements.md`

#### 5.2 设计文档
- [x] 编写架构设计
- [x] 编写组件和接口说明
- [x] 编写数据模型
- [x] 编写正确性属性
- [x] 编写错误处理策略
- [x] 编写测试策略

**状态**: 已完成
**文件**: `.monkeycode/specs/260328-fofa-nl-query/design.md`

#### 5.3 任务列表
- [x] 创建开发任务列表
- [x] 更新任务状态

**状态**: 已完成
**文件**: `.monkeycode/specs/260328-fofa-nl-query/tasklist.md`

## 项目结构

```
/workspace/skills/fofa-nl-query/
├── src/
│   ├── __init__.py              # 包初始化
│   ├── nl_parser.py             # 自然语言解析器
│   ├── query_builder.py         # Fofa 查询构建器
│   ├── fofa_client.py           # Fofa API 客户端
│   ├── export_manager.py        # 导出管理器
│   ├── summary_generator.py     # 摘要生成器
│   └── main.py                  # 主程序入口
├── .env.example                 # 环境变量示例
├── requirements.txt             # 依赖列表
├── README.md                    # 项目说明
└── SKILL.md                     # Skill 说明文档

/workspace/.monkeycode/specs/260328-fofa-nl-query/
├── requirements.md              # 需求文档
├── design.md                    # 设计文档
└── tasklist.md                  # 任务列表
```

## 依赖项

- Python 3.8+
- requests >= 2.28.0
- openpyxl >= 3.0.10
- pandas >= 1.5.0
- jieba >= 0.42.1
- python-dotenv >= 0.19.0

## 使用示例

### 命令行使用

```bash
# 基本查询
python -m src.main "查找广东地区的 OpenClaw 服务"

# 指定输出格式
python -m src.main "查找中国境内运行 Nginx 的 Web 服务器" --format excel

# 指定结果数量
python -m src.main "查找使用 WordPress 的网站" --max 200

# 交互模式
python -m src.main --interactive
```

### Python API 使用

```python
from src.main import FofaNLQuerySkill

skill = FofaNLQuerySkill(email="your-email", key="your-key")
result = skill.execute(
    query="查找广东地区的 OpenClaw 服务",
    output_format='excel',
    max_results=100
)
```

## 总结

本 Skill 已完成所有开发任务，包含：

1. **6 个核心组件**：NLParser、QueryBuilder、FofaClient、ExportManager、SummaryGenerator、main
2. **完整的文档**：SKILL.md、README.md、requirements.md、design.md、tasklist.md
3. **配置支持**：环境变量、命令行参数
4. **多种输出格式**：Excel、CSV、文本摘要
5. **交互模式**：支持连续多轮查询

所有代码遵循 Python 最佳实践，包含完整的类型注解和文档字符串。
