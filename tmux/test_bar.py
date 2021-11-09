from tqdm import tqdm, trange
from random import random, randint
from time import sleep
import sys

pbar = tqdm(total = 100, ncols=80)
for i in range(100):
    pbar.update(1)
    sleep(0.5)

sys.exit(0)

with trange(100) as t:
    for i in t:
        # Description will be displayed on the left
        t.set_description('GEN %i' % i)
        # Postfix will be displayed on the right,
        # formatted automatically based on argument's datatype
        t.set_postfix(loss=random(), gen=randint(1,999), str='h',
                      lst=[1, 2])
        sleep(1)

with tqdm(total=100, bar_format="{postfix[0]} {postfix[1][value]:>8.2g}",
          postfix=["Batch", dict(value=0)]) as t:
    for i in range(10):
        sleep(0.1)
        t.postfix[1]["value"] = i / 2
        t.update()