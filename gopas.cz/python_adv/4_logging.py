import logging

# https://docs.python.org/3/library/logging.html
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s ::: %(message)s', filename='/tmp/python_adv_logging.log')

logging.debug("message with param1={0} and param2={1}".format('a', 'b'))

logging.error("some error message with param1={0} and param2={1}".format('a', 'b'))
