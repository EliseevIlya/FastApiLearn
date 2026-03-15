import logging
import sys
import os
from loguru import logger


class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_logging():
    os.makedirs("logs", exist_ok=True)
    """
    Настраивает логгер для всего приложения в зависимости от окружения.
    """
    # Удаляем стандартный обработчик, чтобы избежать дублирования
    logger.remove()

    # Определяем формат для консоли (разработка)
    dev_format = (
        "<green>{time:HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>"
        "<magenta>{extra}</magenta>"
    )

    # Определяем формат для файла (продакшен)
    prod_format = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function} | {message}"

    # Конфигурация для разработки (если не указано иное)
    if os.getenv("ENV_TYPE", "dev") == "dev":
        logger.add(sys.stderr, level="DEBUG", format=dev_format, colorize=True, backtrace=True, diagnose=True, enqueue=True)

        logger.add(
            "logs/dev_app.log",
            level="DEBUG",
            rotation="100 MB",
            retention="1 month",
            compression="zip",
            serialize=True,  # Структурированное логирование в JSON
            enqueue=True,
            backtrace=True,
            diagnose=True,
        )
        logger.info("Режим разработки: логирование настроено для вывода в консоль.")

    # Конфигурация для продакшена
    else:
        # В консоль выводим только важные сообщения
        logger.add(sys.stderr, level="INFO", format=prod_format, colorize=False, enqueue=True, backtrace=False, diagnose=False)

        # В файл пишем все, начиная с DEBUG, в формате JSON
        logger.add(
            "logs/app.log",
            level="DEBUG",
            rotation="100 MB",
            retention="1 month",
            compression="zip",
            serialize=True,  # Структурированное логирование в JSON
            enqueue=True,
            backtrace=True,
            diagnose=True,
        )
        logger.info("Режим продакшена: логирование настроено для вывода в консоль и файл.")

    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)


    logger.info("Стандартный logging перехвачен и направлен в Loguru.")
