"""
增强版 Fofa 查询构建器
集成规则库，实现更精准的查询构建
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass

from .query_builder import QueryBuilder, FofaQuery
from .nl_parser_enhanced import EnhancedParsedQuery, EnhancedNLParser
from .rule_library import FofaRule


@dataclass
class EnhancedFofaQuery(FofaQuery):
    """增强版 Fofa 查询对象"""
    matched_rules: List[FofaRule] = None
    query_source: str = "auto"  # auto, rule, manual
    confidence: float = 1.0
    
    def __post_init__(self):
        if self.matched_rules is None:
            self.matched_rules = []


class EnhancedQueryBuilder(QueryBuilder):
    """增强版 Fofa 查询构建器"""
    
    def __init__(self):
        """初始化查询构建器"""
        super().__init__()
        self.nl_parser = EnhancedNLParser()
    
    def build(self, parsed_query: EnhancedParsedQuery, max_results: int = 100) -> EnhancedFofaQuery:
        """
        构建增强版 Fofa 查询
        
        Args:
            parsed_query: 增强版解析后的查询对象
            max_results: 最大结果数量
            
        Returns:
            EnhancedFofaQuery: 增强版 Fofa 查询对象
        """
        # 如果有高置信度的规则匹配，优先使用规则查询
        if parsed_query.rule_based_query and parsed_query.matched_rules:
            best_rule = parsed_query.matched_rules[0][0]
            best_score = parsed_query.matched_rules[0][1]
            
            if best_score >= 0.7:
                # 使用规则查询作为基础
                query_string = self._build_rule_based_query(
                    parsed_query, best_rule
                )
                query_source = "rule"
                confidence = best_score
                matched_rules = [r for r, _ in parsed_query.matched_rules[:3]]
            else:
                # 使用传统方式构建查询
                base_query = super().build(parsed_query, max_results)
                query_string = base_query.query_string
                query_source = "auto"
                confidence = best_score
                matched_rules = []
        else:
            # 使用传统方式构建查询
            base_query = super().build(parsed_query, max_results)
            query_string = base_query.query_string
            query_source = "auto"
            confidence = 0.5
            matched_rules = []
        
        # 获取限制数量
        limit = parsed_query.constraints.get('limit', max_results)
        
        return EnhancedFofaQuery(
            query_string=query_string,
            fields=self.DEFAULT_FIELDS,
            page=1,
            size=min(limit, 10000),
            full=False,
            matched_rules=matched_rules,
            query_source=query_source,
            confidence=confidence
        )
    
    def _build_rule_based_query(self, parsed_query: EnhancedParsedQuery, 
                                rule: FofaRule) -> str:
        """
        基于规则构建查询
        
        Args:
            parsed_query: 解析后的查询
            rule: 匹配的规则
            
        Returns:
            str: 组合后的查询语句
        """
        conditions = [rule.query]  # 以规则查询为基础
        
        # 添加地理位置条件
        location_conditions = self._build_location_conditions(parsed_query.entities)
        if location_conditions:
            conditions.extend(location_conditions)
        
        # 添加端口条件
        port_conditions = self._build_port_conditions(parsed_query.entities)
        if port_conditions:
            conditions.extend(port_conditions)
        
        # 添加协议条件
        protocol_conditions = self._build_protocol_conditions(parsed_query.entities)
        if protocol_conditions:
            conditions.extend(protocol_conditions)
        
        # 组合查询条件
        if len(conditions) > 1:
            return ' && '.join(conditions)
        else:
            return conditions[0]
    
    def explain_query(self, fofa_query: EnhancedFofaQuery) -> str:
        """
        解释增强版查询语句
        
        Args:
            fofa_query: 增强版 Fofa 查询对象
            
        Returns:
            str: 查询语句的自然语言解释
        """
        lines = []
        lines.append("=" * 60)
        lines.append("Fofa 查询解释")
        lines.append("=" * 60)
        
        lines.append(f"\n查询语句: {fofa_query.query_string}")
        lines.append(f"查询来源: {fofa_query.query_source}")
        lines.append(f"置信度: {fofa_query.confidence:.2f}")
        
        # 基础解释
        base_explanation = super().explain_query(fofa_query)
        lines.append(f"\n{base_explanation}")
        
        # 匹配的规则
        if fofa_query.matched_rules:
            lines.append("\n匹配的规则:")
            for rule in fofa_query.matched_rules:
                lines.append(f"  - {rule.name} ({rule.category})")
                lines.append(f"    描述: {rule.description}")
                lines.append(f"    标签: {', '.join(rule.tags)}")
        
        lines.append("=" * 60)
        return "\n".join(lines)
    
    def suggest_optimizations(self, fofa_query: EnhancedFofaQuery) -> List[str]:
        """
        建议查询优化
        
        Args:
            fofa_query: Fofa 查询对象
            
        Returns:
            List[str]: 优化建议列表
        """
        suggestions = []
        query = fofa_query.query_string
        
        # 检查是否过于宽泛
        if '&&' not in query and '||' not in query:
            suggestions.append("建议添加更多条件（如地理位置、端口）以缩小搜索范围")
        
        # 检查是否包含通配符
        if '*' in query:
            suggestions.append("包含通配符的查询可能较慢，建议尽量使用精确匹配")
        
        # 检查端口范围
        if 'port=' in query:
            port_matches = re.findall(r'port="(\d+)"', query)
            if len(port_matches) > 5:
                suggestions.append(f"指定了 {len(port_matches)} 个端口，建议减少端口数量以提高查询效率")
        
        # 建议添加更多条件
        if 'country=' not in query and 'region=' not in query:
            suggestions.append("建议添加地理位置条件（如国家、省份）以提高搜索精度")
        
        return suggestions


# 测试代码
if __name__ == "__main__":
    from nl_parser_enhanced import EnhancedNLParser
    
    parser = EnhancedNLParser()
    builder = EnhancedQueryBuilder()
    
    test_queries = [
        "查找广东地区的 OpenClaw 服务",
        "查找中国境内运行 Nginx 的 Web 服务器，端口为 80 或 443",
        "查找暴露的 Redis 服务",
        "查找使用 WordPress 的网站",
        "查找阿里云服务器",
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"原始查询: {query}")
        
        parsed = parser.parse(query)
        fofa_query = builder.build(parsed)
        
        print(f"\nFofa 查询语句: {fofa_query.query_string}")
        print(f"查询来源: {fofa_query.query_source}")
        print(f"置信度: {fofa_query.confidence:.2f}")
        
        if fofa_query.matched_rules:
            print(f"\n匹配的规则:")
            for rule in fofa_query.matched_rules:
                print(f"  - {rule.name}: {rule.query}")
        
        print(f"\n{builder.explain_query(fofa_query)}")
