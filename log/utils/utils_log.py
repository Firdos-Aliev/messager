import logging
import sys

format_str = logging.Formatter('%(asctime)s | %(levelname)-8s | %(message)s')

file_handler = logging.FileHandler('logging_files/utils.log', encoding="utf-8")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(format_str)

# console_handler = logging.StreamHandler(sys.stdout)
# console_handler.setLevel(logging.INFO)
# console_handler.setFormatter(format_str)

log = logging.getLogger('loger')
log.setLevel(logging.INFO)
log.addHandler(file_handler)
# log.addHandler(console_handler)

if __name__ == '__main__':
    log.critical("critical")
    log.error("error")
    log.warning("warning")
    log.info("info")
    log.debug('debug')
