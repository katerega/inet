import logging

from inet import inet

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

i = inet.Inet('test.csv')
i.start(iterations=1)
