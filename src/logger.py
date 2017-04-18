import logging
from logging.handlers import RotatingFileHandler
from src.arguments import args


logger = logging.getLogger('s3sync')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)-15s ==> %(message)s")

# rotate handler
handler = RotatingFileHandler('s3sync.log', backupCount=10, maxBytes=1e6)
handler.setFormatter(formatter)
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)

# stream handler
handler = logging.StreamHandler()
handler.setFormatter(formatter)

if args.verbose:
    handler.setLevel(logging.DEBUG)
else:
    handler.setLevel(logging.INFO)

logger.addHandler(handler)


