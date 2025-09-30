import logging
from datetime import datetime

class AgentLogger:
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler(f"logs/{name}_{datetime.now().strftime('%Y%m%d')}.log")
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log_interaction(self, session_id: str, input: str, output: str):
        self.logger.info(
            f"Session: {session_id}\n"
            f"Input: {input}\n"
            f"Output: {output}\n"
            "="*50
        )