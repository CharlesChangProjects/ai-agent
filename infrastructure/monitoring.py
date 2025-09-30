import time
from functools import wraps


def monitor_performance(metric_name: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start_time

            # 可集成Prometheus或自定义监控系统
            print(f"[METRIC] {metric_name}: {elapsed:.2f}s")
            return result

        return wrapper

    return decorator