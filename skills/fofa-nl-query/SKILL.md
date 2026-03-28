---
name: fofa-nl-query
description: 使用自然语言查询 Fofa 网络空间搜索引擎，自动转换为 Fofa 查询语法并导出结果为 Excel 和摘要报告
arguments:
  - name: query
    description: 自然语言描述的查询需求，例如"查找广东地区的 OpenClaw 服务"
    required: true
  - name: output_format
    description: 输出格式，可选 excel、csv 或 both（默认 excel）
    required: false
    default: excel
  - name: max_results
    description: 最大返回结果数量（默认 100）
    required: false
    default: 100
---

# Fofa 自然语言查询 Skill

## 概述

本 Skill 允许用户使用自然语言描述查询需求，自动将其转换为 Fofa 查询语法，调用 Fofa API 进行搜索，并将结果整理成 Excel 表格和摘要报告。

## 功能特性

1. **自然语言理解**：将用户的中文自然语言描述转换为 Fofa 查询语法
2. **智能查询构建**：支持地理位置、服务类型、端口、协议等多维度查询
3. **结果导出**：支持导出为 Excel (.xlsx) 和 CSV 格式
4. **智能摘要**：自动生成查询结果的统计摘要和关键信息
5. **配置管理**：支持配置 Fofa API 认证信息

## 使用方法

### 基本用法

```
/fofa-nl-query "查找广东地区的 OpenClaw 服务"
```

### 高级用法

```
/fofa-nl-query "查找中国境内运行 Nginx 的 Web 服务器，端口为 80 或 443，导出为 Excel" --max-results 200
```

## 支持的查询类型

### 地理位置查询
- 省份/城市：`广东`、`北京`、`上海`
- 国家：`中国`、`美国`、`日本`
- 区域：`亚洲`、`欧洲`

### 服务类型查询
- Web 服务：`Nginx`、`Apache`、`IIS`
- 数据库：`MySQL`、`MongoDB`、`Redis`
- 中间件：`Tomcat`、`WebLogic`、`JBoss`
- 安全设备：`防火墙`、`WAF`、`IDS`

### 技术指纹查询
- CMS：`WordPress`、`Drupal`、`Joomla`
- 框架：`Spring`、`Django`、`Laravel`
- 组件：`jQuery`、`Bootstrap`、`Vue.js`

### 网络特征查询
- 端口：`80 端口`、`443 端口`、`3306 端口`
- 协议：`HTTP`、`HTTPS`、`SSH`、`FTP`
- 状态码：`200`、`404`、`500`

## 配置说明

首次使用前需要配置 Fofa API 认证信息：

```bash
# 设置环境变量
export FOFA_EMAIL="your-email@example.com"
export FOFA_KEY="your-api-key"
```

或在配置文件中设置：

```json
{
  "fofa_email": "your-email@example.com",
  "fofa_key": "your-api-key"
}
```

## 输出格式

### Excel 输出
- 工作表 1：查询结果详情（IP、端口、协议、标题、位置等）
- 工作表 2：统计摘要（按地区、服务类型分布等）
- 工作表 3：原始 Fofa 查询语句

### CSV 输出
- 包含所有字段的 CSV 文件
- 可用于进一步数据处理

## 示例

### 示例 1：基础查询
```
输入：查找广东地区的 OpenClaw 服务
输出：fofa-query-results-20250328.xlsx
- 查询语句：region="Guangdong" && app="OpenClaw"
- 结果数量：156 条
- 包含字段：IP、端口、协议、标题、位置、服务类型
```

### 示例 2：复合查询
```
输入：查找中国境内使用 Nginx 的 Web 服务器，端口为 80 或 443
输出：fofa-query-results-20250328.xlsx
- 查询语句：country="CN" && server="nginx" && (port="80" || port="443")
- 结果数量：2,847 条
- 按省份分布统计
```

### 示例 3：特定服务查询
```
输入：查找暴露的 Redis 服务，没有密码认证
输出：fofa-query-results-20250328.xlsx
- 查询语句：protocol="redis" && banner="*NOAUTH*"
- 结果数量：89 条
- 安全风险标记
```

## 技术实现

### 架构设计

```
用户输入 (自然语言)
    ↓
[自然语言解析器] → 提取实体和意图
    ↓
[查询构建器] → 生成 Fofa 查询语法
    ↓
[API 客户端] → 调用 Fofa API
    ↓
[结果处理器] → 解析和格式化数据
    ↓
[导出模块] → 生成 Excel/CSV
    ↓
[摘要生成器] → 生成统计报告
    ↓
输出文件 + 摘要
```

### 核心组件

1. **NLParser**：自然语言解析器，识别查询实体
2. **QueryBuilder**：查询构建器，生成 Fofa 语法
3. **FofaClient**：API 客户端，处理 HTTP 请求
4. **DataProcessor**：数据处理器，格式化结果
5. **ExportManager**：导出管理器，生成文件
6. **SummaryGenerator**：摘要生成器，统计分析

## 依赖项

- Python 3.8+
- requests (HTTP 客户端)
- openpyxl (Excel 处理)
- pandas (数据处理)
- jieba (中文分词)

## 安装

```bash
pip install -r requirements.txt
```

## 注意事项

1. **API 限制**：Fofa API 有查询频率和结果数量限制，请查阅官方文档
2. **数据安全**：查询结果可能包含敏感信息，请妥善保管
3. **合规使用**：请遵守相关法律法规和 Fofa 使用条款
4. **错误处理**：网络异常或 API 限制时会返回友好错误信息

## 参考资料

- Fofa API 文档：https://fofa.info/api
- Fofa 规则与指纹：https://fofa.info/library
