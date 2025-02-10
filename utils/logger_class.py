import logging


class Logger:
    def __init__(self, name, level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.name = name
        handler = logging.FileHandler(f"{name}.log", mode='w', encoding='utf-8')
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
        self.logger.addHandler(handler)

    def debug(self, msg, *args, **kwargs):
        self._log('debug', msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self._log('info', msg, *args, **kwargs)

    def _log(self, level, msg, *args, **kwargs):
        msg = f"[{self.name}] - {msg}"
        getattr(self.logger, level)(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self._log('warning', msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self._log('error', msg, *args, **kwargs)
