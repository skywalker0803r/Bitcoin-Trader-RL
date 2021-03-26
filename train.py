import gym
import pandas as pd

from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines import A2C

from env.BitcoinTradingEnv import BitcoinTradingEnv

df = pd.read_csv('./data/bitstamp.csv')
df = df.sort_values('Timestamp')

slice_point = int(len(df) - 50000)

train_df = df[:slice_point]
test_df = df[slice_point:]

train_env = DummyVecEnv(
    [lambda: BitcoinTradingEnv(train_df, serial=True)])

model = A2C(MlpPolicy, train_env, verbose=1,
            tensorboard_log="./tensorboard/")
total_timesteps = 2000
model.learn(total_timesteps=total_timesteps)

model.save("./model/model{}".format(total_timesteps))

print('model training done!')
