#!/usr/bin/env python3
"""Original pellet maze chase with simple roaming enemies, offline."""
import curses,random,time,collections
from ui import put,run
MAP=('#####################','#.........#.........#','#.###.###.#.###.###.#','#o#...............#o#','#.#.###.#####.###.#.#','#.....#...#...#.....#','###.#.###.#.###.#.###','#...#...........#...#','#.#####.#.#.#.#####.#','#.......#...#.......#','#####################')
class Chase:
 def __init__(self,seed=0):
  self.map=MAP;self.player=(1,1);self.enemies=[(19,1),(19,9)];self.pellets={(x,y) for y,row in enumerate(MAP) for x,c in enumerate(row) if c in '.o'};self.power=0;self.lives=3;self.score=0;self.rng=random.Random(seed);self.pellets.discard(self.player)
 def neighbors(self,p):
  x,y=p;return [(nx,ny) for nx,ny in ((x+1,y),(x-1,y),(x,y+1),(x,y-1)) if 0<=ny<len(MAP) and 0<=nx<len(MAP[0]) and MAP[ny][nx]!='#']
 def step(self,direction=(0,0)):
  x,y=self.player;nextp=(x+direction[0],y+direction[1]);old=self.player
  if nextp in self.neighbors(self.player):self.player=nextp
  if self.player in self.pellets:
   self.pellets.remove(self.player);self.score+=10
   if MAP[self.player[1]][self.player[0]]=='o':self.power=30
  else:self.power=max(0,self.power-1)
  previous=self.enemies[:]
  for i,p in enumerate(self.enemies):
   choices=self.neighbors(p);target=self.player
   # Breadth-first distance to player, then chase or flee depending on power.
   dist={target:0};todo=collections.deque([target])
   while todo:
    cur=todo.popleft()
    for n in self.neighbors(cur):
     if n not in dist:dist[n]=dist[cur]+1;todo.append(n)
   self.rng.shuffle(choices);self.enemies[i]=(max if self.power else min)(choices,key=lambda n:dist.get(n,999))
  for i,p in enumerate(self.enemies):
   if p==self.player or previous[i]==self.player and p==old:
    if self.power:self.score+=50;self.enemies[i]=(19,9)
    else:self.lives-=1;self.player=(1,1);self.enemies=[(19,1),(19,9)];break
  return self.lives<=0 or not self.pellets

def loop(s):
 s.timeout(40);g=Chase();direction=(0,0);paused=True;done=False;last=time.monotonic()
 while True:
  h,w=s.getmaxyx();key=s.getch()
  if key in (27,ord('q')):return
  if key==ord('r'):g=Chase();done=False;paused=True
  if key==ord(' '):paused=not paused
  keys={curses.KEY_UP:(0,-1),curses.KEY_DOWN:(0,1),curses.KEY_LEFT:(-1,0),curses.KEY_RIGHT:(1,0),ord('w'):(0,-1),ord('s'):(0,1),ord('a'):(-1,0),ord('d'):(1,0)}
  if key in keys:direction=keys[key];paused=False
  if time.monotonic()-last>.3 and not paused and not done and w>=43 and h>=16:done=g.step(direction);last=time.monotonic()
  s.erase();put(s,0,1,'MAZE CHASE  score '+str(g.score)+' lives '+str(g.lives)+' pellets '+str(len(g.pellets)),curses.A_BOLD)
  if w<43 or h<16:put(s,2,1,'Resize to43x16.')
  else:
   sx=max(2,(w-2)//21);sy=max(1,(h-5)//11);left=max(0,(w-sx*21)//2)
   for y,row in enumerate(MAP):
    for x,c in enumerate(row):
     mark='█' if c=='#' else ('○' if c=='o' else '·') if (x,y) in g.pellets else ' '
     for dy in range(sy):put(s,2+y*sy+dy,left+x*sx,mark*sx if c=='#' else mark)
   put(s,2+g.player[1]*sy,left+g.player[0]*sx,'C',curses.A_REVERSE)
   for x,y in g.enemies:put(s,2+y*sy,left+x*sx,'g' if g.power else 'G',curses.A_BOLD)
   if done:put(s,h-3,1,'ALL PELLETS CLEARED! R restarts' if g.lives else 'GAME OVER. R restarts')
   elif paused:put(s,h-3,1,'Press arrows or Space to start.')
  put(s,h-1,1,'Arrows/WASD move | power circles let you tag ghosts | Space pause | R reset | Esc/q exit');s.refresh()
if __name__=='__main__':
 import sys
 if '--version' in sys.argv:print('1.0.0')
 else:raise SystemExit(run(loop))
