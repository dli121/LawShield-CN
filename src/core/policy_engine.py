import yaml
import os
from typing import List, Dict, Tuple, Optional

class PolicyEngine:
    def __init__(self, config_path: str = "config/rules.yaml"):
        """
        初始化策略引擎，加载 YAML 规则
        """
        self.config_path = config_path
        self.rules = self._load_rules()
        print(f"✅ [PolicyEngine] 规则加载成功: 包含 {len(self.rules.get('block_rules', []))} 条拦截规则")

    def _load_rules(self) -> Dict:
        """读取 YAML 配置文件"""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"配置文件未找到: {self.config_path}")
        
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def check_input(self, text: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        核心检查逻辑
        :param text: 用户输入的问题
        :return: (is_blocked, blocked_reason, legal_ref)
        """
        # 1. 检查 Block Rules (强拦截)
        block_rules = self.rules.get("block_rules", [])
        for rule in block_rules:
            for keyword in rule["keywords"]:
                if keyword in text:
                    # 发现违规关键词！
                    print(f"🚨 [拦截触发] 关键词: {keyword} | 规则: {rule['name']}")
                    return True, rule["response_msg"], rule["legal_ref"]
        
        # 2. 检查 Monitor Rules (这里先简单打印，未来可以做日志审计)
        monitor_rules = self.rules.get("monitor_rules", [])
        for rule in monitor_rules:
            for keyword in rule["keywords"]:
                if keyword in text:
                    print(f"⚠️ [风险审计] 监测到敏感词: {keyword} | 风险等级: {rule.get('risk_level')}")
                    # Monitor 规则只记录，不拦截
                    
        return False, None, None

# 单例模式：全局只创建一个引擎实例，避免重复读取文件

engine = PolicyEngine()