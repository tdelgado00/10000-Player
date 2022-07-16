import numpy as np

EPSILON = 0.1


# Environmnent for one turn of the TenThousand game (we don't consider the distance to the 10000 mark)
class TenThousand:
    def __init__(self, verbose=False):
        self.points = None
        self.to_throw = None
        self.afterstates = None
        self.verbose = verbose
        self.dice_thrown = None
        self.score = None

    def set(self, to_throw, points):
        self.to_throw = to_throw
        self.points = points
        self.score = None
        self.dice_thrown = False
        self.throw_dice()
        if len(self.afterstates) == 0:
            return None
        return self.afterstates

    def throw_dice(self, dice=None):
        if dice is None:
            dice = np.random.randint(6, size=self.to_throw) + 1

        if self.verbose:
            print("Dice throw!", dice)

        quantities = np.zeros(6, dtype=np.int32)
        for d in dice:
            quantities[d-1] += 1

        dice_possibilities = [[] for _ in range(6)]

        for i in range(quantities[0] + 1):
            if i < 3:
                dice_possibilities[0].append((i, 100 * i))
            else:
                dice_possibilities[0].append((i, 100 * (i - 3) + 1000))

        for i in range(quantities[4] + 1):
            if i < 3:
                dice_possibilities[4].append((i, 50 * i))
            else:
                dice_possibilities[4].append((i, 50 * (i - 3) + 500))

        for dice in [1, 2, 3, 5]:
            if quantities[dice] >= 3:
                dice_possibilities[dice].append((3, (dice + 1) * 100))
            dice_possibilities[dice].append((0, 0))

        throw_points = [0 for _ in range(self.to_throw + 1)]
        q = [[]]
        while len(q) > 0:
            c = q.pop()
            if len(c) == 6:
                dice_used = sum([d[0] for d in c])
                points = sum([d[1] for d in c])
                throw_points[dice_used] = max(points, throw_points[dice_used])
            else:
                for poss in dice_possibilities[len(c)]:
                    q.append(c + [poss])

        self.afterstates = []
        for throw in range(1, self.to_throw + 1):
            next_throw = self.to_throw - throw
            if next_throw == 0:
                next_throw = 5
            if throw_points[throw] > 0:
                self.afterstates.append((next_throw, self.points + throw_points[throw]))

        if self.verbose:
            print(self.afterstates)

        self.dice_thrown = True

    def step(self, a, dice=None):
        if self.dice_thrown:
            assert a < len(self.afterstates)

            if self.verbose:
                print("Selected", self.afterstates[a])

            self.to_throw, self.points = self.afterstates[a]
            self.dice_thrown = False
            return self.to_throw, self.points
        else:
            if not a:
                if self.verbose:
                    print("Breaking with", self.points)
                self.score = self.points
                return None
            else:
                if self.verbose:
                    print("Continuing")
                self.throw_dice(dice=dice)
                if len(self.afterstates) == 0:
                    if self.verbose:
                        print("Lost everything")
                    self.score = 0
                    return None
                return self.afterstates

    def reset(self, dice=None):
        self.points = 0
        self.to_throw = 5
        self.throw_dice(dice=dice)
        if len(self.afterstates) == 0:
            self.score = 0
            return None
        else:
            self.score = None
            return self.afterstates


if __name__ == "__main__":
    env = TenThousand(verbose=True)
    obs = env.reset()
    while obs is not None:
        obs, points = env.step(np.random.randint(len(obs)))
