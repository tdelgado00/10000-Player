import numpy as np
from game import TenThousand


class Agent:
    def __init__(self):
        pass

    def bestAction(self, obs):
        raise NotImplementedError

    def play(self, env, eps):
        results = []
        for ep in range(eps):
            obs = env.reset()
            while obs is not None:
                obs = env.step(self.bestAction(obs))
            results.append(env.score)
        return np.mean(results)


class RandomAgent(Agent):
    def __init__(self):
        super().__init__()

    def bestAction(self, obs):
        if type(obs) == list:
            return np.random.randint(len(obs))
        else:
            return np.random.rand() < 0.1  # probability of continuing


class RLAgent(Agent):
    @classmethod
    def from_txt(cls):
        agent = RLAgent()
        agent.n = np.loadtxt("n.csv")
        agent.v = np.loadtxt("v.csv")

        return agent

    def __init__(self, verbose=False):
        super().__init__()

        self.verbose = verbose
        self.v = np.zeros((5, 10000 // 50))
        # v[i, j] is the expected value after choosing an option that leaves us
        # with j points and i dices, before throwing the dice, but assuming that we will continue

        self.n = np.zeros((5, 10000 // 50))

    def train2(self, env, steps):
        while steps >= 0:
            print("Epoch done", steps)
            for to_throw in range(1, 6):
                for points in range(0, 3000):
                    obs = env.set(to_throw, points)
                    # dice have been thrown, we have to choose an option
                    i = env.to_throw - 1
                    j = env.points // 50

                    target = 0 if obs is None else max(max(self.eval(obs)), max([s[1] for s in obs]))

                    self.n[i, j] += 1
                    self.v[i, j] += (target - self.v[i, j]) / self.n[i, j]

                    steps -= 1

    def train(self, env, steps):
        obs = env.reset()
        for t in range(steps):
            # dice have been thrown, we have to choose an option
            i = env.to_throw - 1
            j = env.points // 50

            target = 0 if obs is None else max(max(self.eval(obs)), max([s[1] for s in obs]))

            self.n[i, j] += 1
            self.v[i, j] += (target - self.v[i, j]) / self.n[i, j]

            if obs is None:
                obs = env.reset()
                continue

            a = np.random.randint(len(obs))

            env.step(a)
            obs = env.step(True)  # when training, the agent always continues

    def eval(self, obs):
        return [self.v[s[0]-1, s[1] // 50] for s in obs]

    def bestAction(self, obs, verbose=False):
        if type(obs) == list:
            if verbose:
                print("Value of continuing with each action:")
                print(self.eval(obs))
            if max(self.eval(obs)) <= max([s[1] for s in obs]):
                return np.argmax([s[1] for s in obs])  # if nothing is good for continuing, I break
            else:
                return np.argmax(self.eval(obs))
        else:
            if verbose:
                print("Value of continuing:", self.v[obs[0]-1, obs[1] // 50])
            return self.v[obs[0]-1, obs[1] // 50] > obs[1]


if __name__ == "__main__":
    env = TenThousand(verbose=False)
    agent = RandomAgent()
    print("Random agent performance", agent.play(env, 50000))

    agent = RLAgent(verbose=False)
    print("Starting agent performance", agent.play(env, 50000))

    print("Training...")
    agent.train2(env, 500000)

    print("Trained agent performance", agent.play(env, 50000))

    np.savetxt("v.csv", agent.v, fmt="%.2f")
    np.savetxt("n.csv", agent.n, fmt="%.2f")