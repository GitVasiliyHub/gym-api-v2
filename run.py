
# from gym_api.main import run



if __name__ == '__main__':
    import logging
    import os
    logger = logging.getLogger('gym-api')
    logger.info('Runing app gym-api')
    logger.info(os.environ)
    import uvicorn
    import gym_api
    uvicorn.run("gym_api.main:app", host="0.0.0.0", port=3000, reload=True)

