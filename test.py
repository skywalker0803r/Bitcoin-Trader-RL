import gym
import pandas as pd

from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import A2C

from env.BitcoinTradingEnv import BitcoinTradingEnv

df = pd.read_csv('./data/bitstamp.csv')
df = df.sort_values('Timestamp')

slice_point = int(len(df) - 50000)

test_df = df[slice_point:]

total_timesteps = 20000

model = A2C.load("./model/model{}".format(total_timesteps))

test_env = DummyVecEnv(
    [lambda: BitcoinTradingEnv(test_df, serial=True)])

obs = test_env.reset()
for i in range(50000):
    action, _states = model.predict(obs)
    obs, rewards, done, info = test_env.step(action)
    test_env.render(mode="human")

test_env.close()
