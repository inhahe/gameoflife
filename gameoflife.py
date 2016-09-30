#!/usr/bin/env python

import random, pygame, time

bs = bw, bh = 50, 50
cw = 10
fps = 10

invfps = 1.0/fps
ss = sw, sh = bw*cw, bh*cw
lcells = set()
dcells = set()

pygame.init()
s = pygame.display.set_mode(ss)

def lcadd(x, y):
  lcells.add((x, y))
  for x2, y2 in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)):
    if not (x+x2, x+y2) in lcells:
      dcells.add((x+x2, y+y2))
  pygame.draw.rect(s, (255, 255, 255), (x*cw, y*cw, cw, cw))

for t in xrange((bw*bh)/2):
  x = random.randint(0, bw)
  y = random.randint(0, bh)
  lcadd(x, y)  

while pygame.event.poll().type != pygame.QUIT:
  then = time.time()
    
  if pygame.mouse.get_pressed()[0]:
    px, py = pygame.mouse.get_pos()
    cx, cy = px/cw, py/cw
    if (cx, cy) in lcells:
      dcells.add((cx, cy))
      lcells.remove((cx, cy))
    else:
      lcadd(cx, cy)
      dcells.discard((cx, cy))
      
  pygame.display.flip()
  for (x, y) in tuple(lcells):
    n = sum(((x+x2, y+y2) in lcells for (x2, y2) in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))))
    if n not in (2, 3):
      lcells.remove((x, y))
      dcells.add((x, y))
      pygame.draw.rect(s, (0, 0, 0), (x*cw, y*cw, cw, cw))

  for (x, y) in tuple(dcells):
    n = sum(((x+x2, y+y2) in lcells for (x2, y2) in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))))
    if n == 3:
      lcadd(x, y)
      dcells.remove((x, y))
      lcells.add((x, y))

  # garbage collector
  dct = ()
  ldct = len(dct)
  i = 0
  while time.time()-then < invfps and i < ldct:  
    (x, y) = dct[i]
    if not any(((x+x2, y+y2) in lcells for (x2, y2) in ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)))):
      dcells.remove((x+x2, y+y2))
    i += 1
  time.sleep(invfps-time.time()+then)

# is it possible to create a wall that things will bounce off of?

