from agent import RLAgent
from game import TenThousand
import numpy as np


def read_dice(n):
    dice = list(map(int, input("Input "+str(n)+" dice: ").split(" ")))
    assert len(dice) == n
    return dice


def read_action():
    a = int(input("Input action index: "))
    cont = bool(input("Would like to continue? Y/N ") == "Y")
    return a, cont


if __name__ == "__main__":
    agent = RLAgent.from_txt()

    env = TenThousand(verbose=True)
    dice = read_dice(5)
    obs = env.reset(dice=dice)

    while obs is not None:
        a = agent.bestAction(obs, verbose=True)
        to_throw, points = env.step(a)

        cont = agent.bestAction((to_throw, points), verbose=True)
        if cont:
            dice = read_dice(to_throw)
            obs = env.step(cont, dice=dice)
        else:
            obs = env.step(cont)