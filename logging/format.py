import logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG) # The information would be printed to console without setting filename
logging.debug('This message should appear on the console')
logging.info('So should this')
logging.warning('And this, too')