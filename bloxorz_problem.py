##############################################################################
#
# File:         bloxorz_problem.py
# Date:         Wed 31 Aug 2011  11:40
# Author:       Ken Basye
# Description:  Bloxorz search problem
#
##############################################################################

import cs210_utils
from searchProblem import Arc, Search_problem
import searchGeneric
import searchBFS
#import searchBranchAndBound
import io
from bloxorz import Board
from bloxorz import next_position

class BloxorzProblem(Search_problem):
    """
    >>> board_string = (
    ... '''BLOX 1
    ... 5 3
    ... X X X O O
    ... S X G X O
    ... W W W W X
    ... ''')
    
    >>> fake_file = io.StringIO(board_string)
    >>> board0 = Board.read_board(fake_file)
    >>> bp0 = BloxorzProblem(board0)
    >>> bp0.start
    ((0, 1), (0, 1))

    >>> searcher = searchBFS.BFSSearcher(bp0)  
    >>> path = searcher.search()  
    2507 paths have been expanded and 2399 paths remain in the frontier

    >>> path   
    ((0, 1), (0, 1))
       --R--> ((1, 1), (2, 1))
       --U--> ((1, 0), (2, 0))
       --L--> ((0, 0), (0, 0))
       --D--> ((0, 1), (0, 2))
       --R--> ((1, 1), (1, 2))
       --R--> ((2, 1), (2, 2))
       --U--> ((2, 0), (2, 0))
       --L--> ((0, 0), (1, 0))
       --D--> ((0, 1), (1, 1))
       --R--> ((2, 1), (2, 1))
    
    >>> a_pos, b_pos = path.end()   #doctest: 
    >>> a_pos == b_pos == board0.goal   #doctest: 
    True

    >>> searcher = searchBFS.BFSMultiPruneSearcher(bp0) 
    >>> path = searcher.search()   
    16 paths have been expanded and 1 paths remain in the frontier

    >>> path   
    ((0, 1), (0, 1))
       --R--> ((1, 1), (2, 1))
       --U--> ((1, 0), (2, 0))
       --L--> ((0, 0), (0, 0))
       --D--> ((0, 1), (0, 2))
       --R--> ((1, 1), (1, 2))
       --R--> ((2, 1), (2, 2))
       --U--> ((2, 0), (2, 0))
       --L--> ((0, 0), (1, 0))
       --D--> ((0, 1), (1, 1))
       --R--> ((2, 1), (2, 1))

    >>> searcher = searchGeneric.AStarSearcher(bp0) #doctest: 
    >>> path = searcher.search()   #doctest: 
    1259 paths have been expanded and 1880 paths remain in the frontier

    >>> path   #doctest: 
    ((0, 1), (0, 1))
       --R--> ((1, 1), (2, 1))
       --U--> ((1, 0), (2, 0))
       --L--> ((0, 0), (0, 0))
       --D--> ((0, 1), (0, 2))
       --R--> ((1, 1), (1, 2))
       --R--> ((2, 1), (2, 2))
       --U--> ((2, 0), (2, 0))
       --L--> ((0, 0), (1, 0))
       --D--> ((0, 1), (1, 1))
       --R--> ((2, 1), (2, 1))


    >>> bp0.heuristic = bp0.heuristic1  
    >>> searcher = searchGeneric.AStarSearcher(bp0)
    >>> path = searcher.search()   
    1118 paths have been expanded and 1803 paths remain in the frontier

    >>> path   
    ((0, 1), (0, 1))
       --R--> ((1, 1), (2, 1))
       --U--> ((1, 0), (2, 0))
       --L--> ((0, 0), (0, 0))
       --D--> ((0, 1), (0, 2))
       --R--> ((1, 1), (1, 2))
       --R--> ((2, 1), (2, 2))
       --U--> ((2, 0), (2, 0))
       --L--> ((0, 0), (1, 0))
       --D--> ((0, 1), (1, 1))
       --R--> ((2, 1), (2, 1))

    >>> bp0.heuristic = bp0.heuristic1 #doctest: 
    >>> searcher = searchGeneric.AStarMultiPruneSearcher(bp0)
    >>> path = searcher.search()  #doctest:
    15 paths have been expanded and 1 paths remain in the frontier

    >>> path #doctest: 
    ((0, 1), (0, 1))
       --R--> ((1, 1), (2, 1))
       --U--> ((1, 0), (2, 0))
       --L--> ((0, 0), (0, 0))
       --D--> ((0, 1), (0, 2))
       --R--> ((1, 1), (1, 2))
       --R--> ((2, 1), (2, 2))
       --U--> ((2, 0), (2, 0))
       --L--> ((0, 0), (1, 0))
       --D--> ((0, 1), (1, 1))
       --R--> ((2, 1), (2, 1))

"""
    def __init__(self, board):
        """
        Build a problem instance from a board
        """
        self.board = board
        self.start = (board.start, board.start)
        self.goal = (board.goal, board.goal)
        
    def start_node(self):
        """Returns start node"""
        return self.start
    
    def is_goal(self,node):
        """Returns True if node is a goal"""
        return node == self.goal

    def neighbors(self,node):
      """
        Given a node, return a sequence of Arcs usable
        from this node. 
        """
      arc_output=[]
      Actions=tuple(("U","D","L","R"))
      #get new position from board class and check if that is legal or not 
      #and if that's  a legal add it to the arc list

      for a in Actions:
        next_poslist=next_position(node, a)
        if self.board.legal_position(next_poslist):
          arc=Arc(node, next_poslist, cost=1, action=a)
          arc_output.append(arc)
          
      return (arc_output)

    def heuristic(self, node):
        """Gives the heuristic value of node n.
        Returns 0 if not overridden."""
        
        return 0  
    
    def heuristic1(self, node): 
     
        #difference between the goal and the current position 
        distance_cube1_Xcoord= abs(self.goal[0][0]-node[0][0])
        distance_cube1_Ycoord=abs(self.goal[0][1]-node[0][1])
        #for second cube distance to the cube
        distance_cube2_Xcoord= abs(self.goal[0][0]-node[1][0])
        distance_cube2_Ycoord=abs(self.goal[0][1]-node[1][1])

        #calculating the minimum distance of their coordinates 

        minX= min( distance_cube1_Xcoord,distance_cube1_Ycoord)
        minY= min(distance_cube2_Xcoord,distance_cube2_Ycoord)
        #calculating manhaattan distance
        manhattanDistance=(minX+minY)/1.5
        return manhattanDistance

        

        



        

        
 
     

    

if __name__ == '__main__':
  

    cs210_utils.cs210_mainstartup()

