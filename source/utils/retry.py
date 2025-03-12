import time
from functools import wraps
from typing import TypeVar, Callable, Any

T = TypeVar('T')

def retry_with_timeout(max_retries: int = 3, timeout: int = 60) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """
    Декоратор для повторных попыток выполнения функции с таймаутом.
    
    Args:
        max_retries (int): Максимальное количество попыток
        timeout (int): Максимальное время ожидания в секундах
        
    Returns:
        Результат выполнения декорированной функции
        
    Raises:
        TimeoutError: Если превышено время ожидания
        Exception: Если все попытки завершились неудачно
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            start_time = time.time()
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if time.time() - start_time > timeout:
                        raise TimeoutError(f"Превышено время ожидания {timeout} секунд")
                    time.sleep(min(2 ** attempt, timeout))  # Exponential backoff
                    
            raise last_exception or Exception("Все попытки выполнения завершились неудачно")
        return wrapper
    return decorator 