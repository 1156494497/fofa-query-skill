# Fofa 自然语言查询 Skill 需求文档

## 引言

本 Skill 允许用户使用自然语言描述查询需求，自动将其转换为 Fofa 查询语法，调用 Fofa API 进行搜索，并将结果整理成 Excel 表格和摘要报告。

## 词汇表

- **Fofa**：网络空间搜索引擎，用于搜索互联网资产
- **自然语言查询**：用户使用中文描述查询需求，而非专业的查询语法
- **Fofa 查询语法**：Fofa 支持的专业查询语句，如 `country="CN" && port="80"`
- **API Key**：Fofa API 认证密钥
- **资产**：网络上的服务器、服务、设备等可被搜索到的实体

## 需求

### 需求 1：自然语言解析

**用户故事：** AS 安全研究员，我想要用中文描述查询需求，以便无需学习复杂的 Fofa 查询语法就能进行资产搜索。

#### Acceptance Criteria

1. WHEN 用户输入包含地理位置的自然语言查询，THE Skill SHALL 识别出国家、省份、城市等位置实体
2. WHEN 用户输入包含服务类型的自然语言查询，THE Skill SHALL 识别出 Web 服务器、数据库、CMS 等服务实体
3. WHEN 用户输入包含端口信息的自然语言查询，THE Skill SHALL 识别出端口号
4. WHEN 用户输入包含协议信息的自然语言查询，THE Skill SHALL 识别出协议类型
5. WHEN 用户输入复合查询条件，THE Skill SHALL 正确解析多个实体并建立逻辑关系

### 需求 2：Fofa 查询构建

**用户故事：** AS 安全研究员，我想要将自然语言自动转换为 Fofa 查询语法，以便系统能正确执行搜索。

#### Acceptance Criteria

1. WHEN 系统识别到地理位置实体，THE Skill SHALL 生成对应的 Fofa 查询字段（country、region、city）
2. WHEN 系统识别到服务类型实体，THE Skill SHALL 选择合适的 Fofa 字段（server、app、banner）
3. WHEN 存在多个查询条件，THE Skill SHALL 使用逻辑运算符（&&、||）正确组合查询语句
4. WHEN 查询语句构建完成，THE Skill SHALL 提供自然语言解释说明查询含义
5. WHEN 系统无法识别查询意图，THE Skill SHALL 使用原始查询作为全文搜索

### 需求 3：Fofa API 调用

**用户故事：** AS 安全研究员，我想要系统自动调用 Fofa API 获取搜索结果，以便获得最新的资产数据。

#### Acceptance Criteria

1. WHEN 用户配置 API 认证信息，THE Skill SHALL 验证认证信息的有效性
2. WHEN 用户发起查询请求，THE Skill SHALL 使用 Base64 编码查询语句并调用 Fofa API
3. WHEN API 返回大量结果，THE Skill SHALL 自动分页获取指定数量的结果
4. WHEN API 调用失败，THE Skill SHALL 返回友好的错误信息
5. WHEN 网络请求超时，THE Skill SHALL 提示用户检查网络连接

### 需求 4：结果导出

**用户故事：** AS 安全研究员，我想要将查询结果导出为 Excel 和 CSV 格式，以便进行后续分析和存档。

#### Acceptance Criteria

1. WHEN 用户选择 Excel 格式，THE Skill SHALL 生成包含多工作表的 .xlsx 文件
2. WHEN 用户选择 CSV 格式，THE Skill SHALL 生成标准 CSV 文件
3. WHEN 导出 Excel 文件，THE Skill SHALL 包含查询结果、统计摘要、查询信息三个工作表
4. WHEN 导出结果，THE Skill SHALL 自动调整列宽以适应内容
5. WHEN 导出大量数据，THE Skill SHALL 确保文件格式正确且可正常打开

### 需求 5：摘要生成

**用户故事：** AS 安全研究员，我想要获得查询结果的统计摘要，以便快速了解资产分布情况。

#### Acceptance Criteria

1. WHEN 查询完成，THE Skill SHALL 生成包含统计概览的文本摘要
2. WHEN 结果包含地理位置信息，THE Skill SHALL 统计并按国家、省份、城市分布
3. WHEN 结果包含服务信息，THE Skill SHALL 统计服务器类型、应用类型分布
4. WHEN 结果包含端口信息，THE Skill SHALL 统计端口分布情况
5. WHEN 发现高危端口暴露，THE Skill SHALL 在摘要中提供安全提示

### 需求 6：配置管理

**用户故事：** AS 安全研究员，我想要配置 Fofa API 认证信息，以便系统能正常调用 API。

#### Acceptance Criteria

1. WHEN 用户设置环境变量，THE Skill SHALL 从环境变量读取 API 认证信息
2. WHEN 用户通过参数提供认证信息，THE Skill SHALL 优先使用参数值
3. WHEN 认证信息缺失，THE Skill SHALL 提示用户提供认证信息
4. WHEN 认证失败，THE Skill SHALL 提示检查 email 和 key 是否正确
5. WHEN Skill 启动时，THE Skill SHALL 验证认证信息的有效性

### 需求 7：交互模式

**用户故事：** AS 安全研究员，我想要使用交互模式进行多轮查询，以便连续进行多个资产搜索任务。

#### Acceptance Criteria

1. WHEN 用户启动交互模式，THE Skill SHALL 提示用户输入查询语句
2. WHEN 用户输入查询后，THE Skill SHALL 询问输出格式和结果数量
3. WHEN 查询完成，THE Skill SHALL 返回结果并提示输入下一个查询
4. WHEN 用户输入退出命令，THE Skill SHALL 正常退出交互模式
5. WHEN 用户输入空查询，THE Skill SHALL 提示重新输入

## 非功能性需求

### 性能需求

1. THE Skill SHALL 在 5 秒内完成自然语言解析和查询构建
2. THE Skill SHALL 支持单次查询最多 10000 条结果（受 Fofa API 限制）
3. THE Skill SHALL 在导出大量数据时保持内存使用合理

### 可用性需求

1. THE Skill SHALL 提供清晰的命令行帮助信息
2. THE Skill SHALL 在执行过程中显示进度信息
3. THE Skill SHALL 提供友好的错误提示
4. THE Skill SHALL 支持中文自然语言输入

### 兼容性需求

1. THE Skill SHALL 支持 Python 3.8 及以上版本
2. THE Skill SHALL 生成的 Excel 文件兼容 Microsoft Excel 和 LibreOffice
3. THE Skill SHALL 生成的 CSV 文件使用 UTF-8 编码

## 参考资料

- Fofa API 文档：https://fofa.info/api
- Fofa 规则与指纹：https://fofa.info/library
