import unittest,random,collections
import game
modules={'maze-chase':game}
class Tests(unittest.TestCase):
 def test_maze_connected(self):
  g=modules['maze-chase'].Chase();seen={g.player};todo=collections.deque(seen)
  while todo:
   for n in g.neighbors(todo.popleft()):
    if n not in seen:seen.add(n);todo.append(n)
  self.assertTrue(g.pellets<=seen)
 def test_maze_wall(self):
  g=modules['maze-chase'].Chase();g.step((-1,0));self.assertEqual(g.player,(1,1))
 def test_maze_eat(self):
  g=modules['maze-chase'].Chase();n=len(g.pellets);g.step((1,0));self.assertEqual(len(g.pellets),n-1)
if __name__=="__main__":unittest.main()
