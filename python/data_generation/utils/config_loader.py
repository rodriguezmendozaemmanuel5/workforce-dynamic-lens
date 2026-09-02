# =============================================================================
# WORKFORCE DYNAMIC LENS — MODULE v0.6.0
# Configuration & Catalog File Loader
# =============================================================================

import yaml
import json
from pathlib import Path
from typing import Dict, Any, List

class ConfigLoader:
    def __init__(self, config_dir: str = "python/data_generation/config"):
        self.config_dir = Path(config_dir)

    def load_yaml_config(self, filename: str = "config.yaml") -> Dict[str, Any]:
        path = self.config_dir / filename
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def load_json_catalog(self, filename: str) -> List[Dict[str, Any]]:
        path = self.config_dir / filename
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def load_fx_rates(self, filename: str = "country_fx_rates.json") -> Dict[str, Any]:
        path = self.config_dir / filename
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
