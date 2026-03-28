"""
Fofa 规则库查询模块
从 Fofa 规则库获取资产规则，实现更精准的资产搜索
"""

import requests
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from functools import lru_cache
import json


@dataclass
class FofaRule:
    """Fofa 规则定义"""
    name: str                    # 规则名称
    query: str                   # Fofa 查询语句
    category: str                # 分类（如：Web服务器、数据库等）
    description: str             # 规则描述
    tags: List[str]              # 标签
    vendor: Optional[str]        # 厂商
    product: Optional[str]       # 产品名


class RuleLibrary:
    """Fofa 规则库管理器"""
    
    # Fofa 规则库基础 URL
    BASE_URL = "https://fofa.info"
    LIBRARY_URL = "https://fofa.info/library"
    
    def __init__(self):
        """初始化规则库"""
        self.rules_cache: Dict[str, List[FofaRule]] = {}
        self._init_default_rules()
    
    def _init_default_rules(self):
        """初始化默认规则库（常用资产规则）"""
        self.default_rules = {
            # Web 服务器
            "nginx": FofaRule(
                name="Nginx",
                query="app=\"nginx\"",
                category="Web服务器",
                description="Nginx Web服务器",
                tags=["web", "server", "nginx"],
                vendor="Nginx",
                product="Nginx"
            ),
            "apache": FofaRule(
                name="Apache",
                query="app=\"Apache\"",
                category="Web服务器",
                description="Apache HTTP Server",
                tags=["web", "server", "apache"],
                vendor="Apache",
                product="Apache HTTP Server"
            ),
            "iis": FofaRule(
                name="IIS",
                query="app=\"IIS\"",
                category="Web服务器",
                description="Microsoft IIS",
                tags=["web", "server", "iis", "microsoft"],
                vendor="Microsoft",
                product="IIS"
            ),
            "tomcat": FofaRule(
                name="Tomcat",
                query="app=\"Apache-Tomcat\"",
                category="Web服务器",
                description="Apache Tomcat",
                tags=["web", "server", "tomcat", "java"],
                vendor="Apache",
                product="Tomcat"
            ),
            
            # 数据库
            "mysql": FofaRule(
                name="MySQL",
                query="app=\"MySQL\"",
                category="数据库",
                description="MySQL 数据库",
                tags=["database", "mysql", "sql"],
                vendor="Oracle",
                product="MySQL"
            ),
            "redis": FofaRule(
                name="Redis",
                query="app=\"Redis\"",
                category="数据库",
                description="Redis 内存数据库",
                tags=["database", "redis", "nosql"],
                vendor="Redis",
                product="Redis"
            ),
            "mongodb": FofaRule(
                name="MongoDB",
                query="app=\"MongoDB\"",
                category="数据库",
                description="MongoDB 文档数据库",
                tags=["database", "mongodb", "nosql"],
                vendor="MongoDB",
                product="MongoDB"
            ),
            "postgresql": FofaRule(
                name="PostgreSQL",
                query="app=\"PostgreSQL\"",
                category="数据库",
                description="PostgreSQL 关系型数据库",
                tags=["database", "postgresql", "sql"],
                vendor="PostgreSQL",
                product="PostgreSQL"
            ),
            "elasticsearch": FofaRule(
                name="Elasticsearch",
                query="app=\"Elasticsearch\"",
                category="数据库",
                description="Elasticsearch 搜索引擎",
                tags=["database", "elasticsearch", "search"],
                vendor="Elastic",
                product="Elasticsearch"
            ),
            
            # CMS
            "wordpress": FofaRule(
                name="WordPress",
                query="app=\"WordPress\"",
                category="CMS",
                description="WordPress 内容管理系统",
                tags=["cms", "wordpress", "php"],
                vendor="WordPress",
                product="WordPress"
            ),
            "drupal": FofaRule(
                name="Drupal",
                query="app=\"Drupal\"",
                category="CMS",
                description="Drupal 内容管理系统",
                tags=["cms", "drupal", "php"],
                vendor="Drupal",
                product="Drupal"
            ),
            "joomla": FofaRule(
                name="Joomla",
                query="app=\"Joomla\"",
                category="CMS",
                description="Joomla 内容管理系统",
                tags=["cms", "joomla", "php"],
                vendor="Joomla",
                product="Joomla"
            ),
            
            # 框架
            "spring": FofaRule(
                name="Spring",
                query="app=\"Spring\"",
                category="框架",
                description="Spring Framework",
                tags=["framework", "spring", "java"],
                vendor="Spring",
                product="Spring"
            ),
            "django": FofaRule(
                name="Django",
                query="app=\"Django\"",
                category="框架",
                description="Django Web框架",
                tags=["framework", "django", "python"],
                vendor="Django",
                product="Django"
            ),
            "laravel": FofaRule(
                name="Laravel",
                query="app=\"Laravel\"",
                category="框架",
                description="Laravel PHP框架",
                tags=["framework", "laravel", "php"],
                vendor="Laravel",
                product="Laravel"
            ),
            "thinkphp": FofaRule(
                name="ThinkPHP",
                query="app=\"ThinkPHP\"",
                category="框架",
                description="ThinkPHP PHP框架",
                tags=["framework", "thinkphp", "php"],
                vendor="ThinkPHP",
                product="ThinkPHP"
            ),
            
            # 中间件
            "weblogic": FofaRule(
                name="WebLogic",
                query="app=\"WebLogic\"",
                category="中间件",
                description="Oracle WebLogic Server",
                tags=["middleware", "weblogic", "java", "oracle"],
                vendor="Oracle",
                product="WebLogic"
            ),
            "jboss": FofaRule(
                name="JBoss",
                query="app=\"JBoss\"",
                category="中间件",
                description="JBoss Application Server",
                tags=["middleware", "jboss", "java"],
                vendor="Red Hat",
                product="JBoss"
            ),
            "websphere": FofaRule(
                name="WebSphere",
                query="app=\"WebSphere\"",
                category="中间件",
                description="IBM WebSphere",
                tags=["middleware", "websphere", "java", "ibm"],
                vendor="IBM",
                product="WebSphere"
            ),
            
            # 安全设备
            "防火墙": FofaRule(
                name="防火墙",
                query="title=\"防火墙\" || header=\"firewall\"",
                category="安全设备",
                description="防火墙设备",
                tags=["security", "firewall"],
                vendor=None,
                product="防火墙"
            ),
            "waf": FofaRule(
                name="WAF",
                query="app=\"WAF\" || header=\"WAF\"",
                category="安全设备",
                description="Web应用防火墙",
                tags=["security", "waf"],
                vendor=None,
                product="WAF"
            ),
            
            # 云服务
            "阿里云": FofaRule(
                name="阿里云",
                query="header=\"aliyun\" || header=\"Aliyun\"",
                category="云服务",
                description="阿里云服务器",
                tags=["cloud", "aliyun", "阿里云"],
                vendor="阿里云",
                product="阿里云 ECS"
            ),
            "腾讯云": FofaRule(
                name="腾讯云",
                query="header=\"tencent\" || header=\"Tencent\"",
                category="云服务",
                description="腾讯云服务器",
                tags=["cloud", "tencent", "腾讯云"],
                vendor="腾讯云",
                product="腾讯云 CVM"
            ),
            "aws": FofaRule(
                name="AWS",
                query="header=\"aws\" || header=\"Amazon\"",
                category="云服务",
                description="Amazon Web Services",
                tags=["cloud", "aws", "amazon"],
                vendor="Amazon",
                product="AWS"
            ),
        }
    
    def search_rules(self, keyword: str) -> List[FofaRule]:
        """
        根据关键词搜索规则
        
        Args:
            keyword: 搜索关键词
            
        Returns:
            List[FofaRule]: 匹配的规则列表
        """
        keyword_lower = keyword.lower()
        results = []
        
        for rule in self.default_rules.values():
            # 匹配规则名称
            if keyword_lower in rule.name.lower():
                results.append(rule)
                continue
            
            # 匹配分类
            if keyword_lower in rule.category.lower():
                results.append(rule)
                continue
            
            # 匹配标签
            for tag in rule.tags:
                if keyword_lower in tag.lower():
                    results.append(rule)
                    break
            
            # 匹配厂商
            if rule.vendor and keyword_lower in rule.vendor.lower():
                results.append(rule)
                continue
            
            # 匹配产品
            if rule.product and keyword_lower in rule.product.lower():
                results.append(rule)
                continue
        
        return results
    
    def get_rule_by_name(self, name: str) -> Optional[FofaRule]:
        """
        根据名称获取规则
        
        Args:
            name: 规则名称
            
        Returns:
            Optional[FofaRule]: 规则对象或 None
        """
        name_lower = name.lower()
        
        # 直接匹配
        if name_lower in self.default_rules:
            return self.default_rules[name_lower]
        
        # 模糊匹配
        for key, rule in self.default_rules.items():
            if name_lower in rule.name.lower() or name_lower in key:
                return rule
        
        return None
    
    def get_rules_by_category(self, category: str) -> List[FofaRule]:
        """
        根据分类获取规则
        
        Args:
            category: 分类名称
            
        Returns:
            List[FofaRule]: 该分类下的所有规则
        """
        category_lower = category.lower()
        return [
            rule for rule in self.default_rules.values()
            if category_lower in rule.category.lower()
        ]
    
    def get_all_categories(self) -> List[str]:
        """获取所有分类"""
        categories = set()
        for rule in self.default_rules.values():
            categories.add(rule.category)
        return sorted(list(categories))
    
    def suggest_rules(self, query: str) -> List[Tuple[FofaRule, float]]:
        """
        根据查询推荐规则
        
        Args:
            query: 自然语言查询
            
        Returns:
            List[Tuple[FofaRule, float]]: 规则和建议度
        """
        query_lower = query.lower()
        suggestions = []
        
        for rule in self.default_rules.values():
            score = 0.0
            
            # 名称匹配
            if rule.name.lower() in query_lower:
                score += 1.0
            
            # 分类匹配
            if rule.category.lower() in query_lower:
                score += 0.8
            
            # 标签匹配
            for tag in rule.tags:
                if tag.lower() in query_lower:
                    score += 0.6
                    break
            
            # 厂商匹配
            if rule.vendor and rule.vendor.lower() in query_lower:
                score += 0.7
            
            # 产品匹配
            if rule.product and rule.product.lower() in query_lower:
                score += 0.9
            
            if score > 0:
                suggestions.append((rule, score))
        
        # 按分数排序
        suggestions.sort(key=lambda x: x[1], reverse=True)
        return suggestions[:5]  # 返回前5个建议
    
    def get_rule_query(self, service_name: str) -> Optional[str]:
        """
        获取服务的 Fofa 查询语句
        
        Args:
            service_name: 服务名称
            
        Returns:
            Optional[str]: Fofa 查询语句或 None
        """
        rule = self.get_rule_by_name(service_name)
        if rule:
            return rule.query
        return None
    
    def list_all_rules(self) -> Dict[str, List[FofaRule]]:
        """
        列出所有规则（按分类组织）
        
        Returns:
            Dict[str, List[FofaRule]]: 分类到规则的映射
        """
        result = {}
        for rule in self.default_rules.values():
            if rule.category not in result:
                result[rule.category] = []
            result[rule.category].append(rule)
        return result
    
    def print_rules_summary(self):
        """打印规则库摘要"""
        print("=" * 60)
        print("Fofa 规则库摘要")
        print("=" * 60)
        
        rules_by_category = self.list_all_rules()
        
        for category, rules in sorted(rules_by_category.items()):
            print(f"\n【{category}】({len(rules)} 个规则)")
            for rule in rules:
                print(f"  - {rule.name}: {rule.query}")
        
        print(f"\n总计: {len(self.default_rules)} 个规则")
        print("=" * 60)


# 测试代码
if __name__ == "__main__":
    library = RuleLibrary()
    
    # 打印规则库摘要
    library.print_rules_summary()
    
    # 测试搜索
    print("\n\n测试搜索 'nginx':")
    results = library.search_rules("nginx")
    for rule in results:
        print(f"  - {rule.name}: {rule.query}")
    
    # 测试建议
    print("\n\n测试查询 '查找广东地区的 Web 服务器':")
    suggestions = library.suggest_rules("查找广东地区的 Web 服务器")
    for rule, score in suggestions:
        print(f"  - {rule.name} (匹配度: {score:.2f}): {rule.query}")
