import logging
from .maker import make

def handler(code: str, model: str):
    m = make(code, model=model)
    logging.warn(m)
    return m