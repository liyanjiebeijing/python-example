from loguru import logger 

def test():
    logger.debug("debug message"    ) 
    logger.info("info level message") 
    logger.warning("warning level message") 
    logger.critical("critical level message") 

if __name__ == '__main__':
    test()
