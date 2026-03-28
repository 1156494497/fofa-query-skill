"""
增强版自然语言解析器
集成 Fofa 规则库，实现更精准的资产搜索
"""

import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field

from .nl_parser import NLParser, QueryEntity, ParsedQuery
from .rule_library import RuleLibrary, FofaRule


@dataclass
class EnhancedParsedQuery(ParsedQuery):
    """增强版解析后的查询"""
    matched_rules: List[Tuple[FofaRule, float]] = field(default_factory=list)
    suggested_queries: List[str] = field(default_factory=list)
    rule_based_query: Optional[str] = None


class EnhancedNLParser(NLParser):
    """增强版自然语言查询解析器，集成规则库"""
    
    def __init__(self):
        """初始化解析器"""
        super().__init__()
        self.rule_library = RuleLibrary()
    
    def parse(self, query: str) -> EnhancedParsedQuery:
        """
        解析自然语言查询（增强版）
        
        Args:
            query: 用户的自然语言查询
            
        Returns:
            EnhancedParsedQuery: 增强版解析后的查询对象
        """
        # 先调用基础解析
        base_parsed = super().parse(query)
        
        # 使用规则库推荐规则
        matched_rules = self.rule_library.suggest_rules(query)
        
        # 生成基于规则的查询建议
        suggested_queries = []
        rule_based_query = None
        
        if matched_rules:
            # 获取匹配度最高的规则
            best_rule, best_score = matched_rules[0]
            
            if best_score >= 0.6:  # 匹配度阈值
                rule_based_query = best_rule.query
                
                # 生成建议查询
                for rule, score in matched_rules[:3]:  # 前3个建议
                    suggested_queries.append(rule.query)
        
        # 创建增强版解析结果
        return EnhancedParsedQuery(
            raw_query=base_parsed.raw_query,
            entities=base_parsed.entities,
            intent=base_parsed.intent,
            constraints=base_parsed.constraints,
            matched_rules=matched_rules,
            suggested_queries=suggested_queries,
            rule_based_query=rule_based_query
        )
    
    def get_service_rule(self, service_name: str) -> Optional[FofaRule]:
        """
        获取服务的规则定义
        
        Args:
            service_name: 服务名称
            
        Returns:
            Optional[FofaRule]: 规则定义或 None
        """
        return self.rule_library.get_rule_by_name(service_name)
    
    def search_rules(self, keyword: str) -> List[FofaRule]:
        """
        搜索规则
        
        Args:
            keyword: 关键词
            
        Returns:
            List[FofaRule]: 匹配的规则列表
        """
        return self.rule_library.search_rules(keyword)
    
    def get_all_categories(self) -> List[str]:
        """获取所有规则分类"""
        return self.rule_library.get_all_categories()
    
    def list_rules_by_category(self, category: str) -> List[FofaRule]:
        """
        列出某分类下的所有规则
        
        Args:
            category: 分类名称
            
        Returns:
            List[FofaRule]: 规则列表
        """
        return self.rule_library.get_rules_by_category(category)
    
    def explain_parsing_result(self, parsed: EnhancedParsedQuery) -> str:
        """
        解释解析结果
        
        Args:
            parsed: 解析结果
            
        Returns:
            str: 解析说明
        """
        lines = []
        lines.append("=" * 60)
        lines.append("查询解析结果")
        lines.append("=" * 60)
        lines.append(f"\n原始查询: {parsed.raw_query}")
        lines.append(f"查询意图: {parsed.intent}")
        
        # 识别的实体
        if parsed.entities:
            lines.append("\n识别的实体:")
            for entity in parsed.entities:
                lines.append(f"  - {entity.entity_type}: {entity.value}")
        
        # 匹配的规则
        if parsed.matched_rules:
            lines.append("\n匹配的规则:")
            for rule, score in parsed.matched_rules[:5]:
                lines.append(f"  - {rule.name} (匹配度: {score:.2f})")
                lines.append(f"    分类: {rule.category}")
                lines.append(f"    查询: {rule.query}")
        
        # 建议的查询
        if parsed.suggested_queries:
            lines.append("\n建议的 Fofa 查询:")
            for i, sq in enumerate(parsed.suggested_queries, 1):
                lines.append(f"  {i}. {sq}")
        
        # 基于规则的查询
        if parsed.rule_based_query:
            lines.append(f"\n推荐的规则查询: {parsed.rule_based_query}")
        
        lines.append("=" * 60)
        return "\n".join(lines)


# 测试代码
if __name__ == "__main__":
    parser = EnhancedNLParser()
    
    test_queries = [
        "查找广东地区的 OpenClaw 服务",
        "查找中国境内运行 Nginx 的 Web 服务器，端口为 80 或 443",
        "查找暴露的 Redis 服务",
        "查找使用 WordPress 的网站，前100条结果",
        "查找阿里云服务器",
        "查找使用 Spring 框架的应用",
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"查询: {query}")
        print(f"{'='*60}")
        
        result = parser.parse(query)
        print(parser.explain_parsing_result(result))
