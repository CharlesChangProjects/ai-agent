import yaml
from pathlib import Path
from typing import Dict, Any

class ConfigLoader:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_all()
        return cls._instance

    def _load_all(self):
        self.llm_config = self._load_yaml("llm_configs.yaml")
        self.tool_config = self._load_yaml("tool_configs.yaml")

    def _load_yaml(self, filename: str) -> Dict[str, Any]:
        path = Path(__file__).parent / filename
        with open(path, encoding='utf-8') as f:
            return yaml.safe_load(f)

    @property
    def deepseek_config(self) -> Dict[str, Any]:
        return self.llm_config["deepseek"]