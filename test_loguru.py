from loguru import logger 

def test():
    logger.debug("debug message"    ) 
    logger.info("info level message") 
    logger.warning("warning level message") 
    logger.critical("critical level message") 

    info_dict = {'name':'liyanjie', 'age':31}
    logger.info(info_dict)

def test_rotation():    
    logger.add('output/file_{time}.log', rotation = "200KB")
    for n in range(10000):
        logger.info(f"test - {n}")

if __name__ == '__main__':
    test()
    # test_rotation()
