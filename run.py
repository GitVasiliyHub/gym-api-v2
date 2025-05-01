
# from gym_api.main import run
import gym_api


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("gym_api.main:app", host="0.0.0.0", port=3000, reload=True)

