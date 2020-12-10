import logging
import sys

format_str = logging.Formatter('%(asctime)s | %(levelname)-8s | %(message)s')

file_handler = logging.FileHandler('logging_files/client.log', encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(format_str)

log = logging.getLogger('loger')
log.setLevel(logging.DEBUG)
log.addHandler(file_handler)

if __name__ == '__main__':
    pass
    # file_handler.critical("critical")
    # file_handler.error("error")
    # file_handler.warning("warning")
    # file_handler.info("info")
    # file_handler.debug('debug')
