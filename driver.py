##############################################################################
#
# File:         driver.py
# Date:         Tue 11 Sep 2018  11:33
# Author:       Ken Basye
# Description:  Driver for testing bloxorz algorithms
#
##############################################################################

"""
Driver for testing bloxorz algorithms

"""

from bloxorz_problem import BloxorzProblem
from bloxorz import Board
import searchGeneric
import searchBFS
import os
import glob
import pandas as pd
import numpy as np

if __name__ == "__main__":
    board_names = glob.glob("boards/*.blx")
    noSolution_board= ['ben','cat','mike','navid','rayyan','skyler','yu','zongyao','tyler']
    #three excel files for 3 differnent algorithms
    tableFormat1={"Board"  :[],
                  "BFSMultiprune_Length"   :[],
                  "BFSMultiprune_Expansions"  :[]
    }
    tableFormat2={"Board"  :[],
                  "AstarMUltiPrune_length" :[],
                  "AstarMUltiPrune_expansions": []
    } 
    tableFormat3={"Board"  :[],
                  "AStar_Length"  :[],
                  "Astar_expansions" :[]
    } 

                  
     #testing for BFSMultipruneSearcher            
    for board_name in board_names:
        if board_name[7:] in noSolution_board:
          print('unsolvable board '+ str(board_name[7:]))
          continue

        print("Loading board file %s" % (board_name,))
        with open(board_name) as file:
            board = Board.read_board(file)

        tableFormat1["Board"].append(board_name[7:])
        bp0 = BloxorzProblem(board)

        searcher = searchBFS.BFSMultiPruneSearcher(bp0)
        result = searcher.search()
        # length=0

        if result is None:
          print("For board %s, found no solution!" % (board_name,))
          tableFormat1['BFSMultiprune_Length'].append(0)
          tableFormat1['BFSMultiprune_Expansions'].append(0)
        else:
          sequence = [arc.action for arc in result.arcs()]
          # length=(len(sequence))
          print("For board %s, found solution with length %d using %d expansions" % (board_name, len(sequence), searcher.num_expanded))
          tableFormat1['BFSMultiprune_Length'].append(len(sequence))
          tableFormat1['BFSMultiprune_Expansions'].append((searcher.num_expanded))
          continue

#dataframe and converion to xml and html file with a average of the lengths and expansions
        df=pd.DataFrame(tableFormat1)
        average=df["BFSMultiprune_Length"].mean()
        average2=df["BFSMultiprune_Expansions"].mean()
        print(average, average2)

        new_row={"Board"  : "Average",
                  "BFSMultiprune_Length"   :average,
                  "BFSMultiprune_Expansions"  :average2}
        df=df.append(new_row, ignore_index=True)
        
        # df_new= pd.DataFrame(np.insert(df.values, df["Board"].iloc[-1], values=["Average",average, average2], axis=0))

        df.to_excel("/content/drive/My Drive/AI/table.xlsx", index=False)
        
        htmlsetup=df.to_html(index=False)
        html_file= open("/content/drive/My Drive/AI/htmlFile.html","w")
        html_file.write(htmlsetup)
        html_file.close()
        print(df)


   #testing for AstarMultipruning
    for board_name in board_names:
        print("Loading board file %s" % (board_name,))
        with open(board_name) as file:
            board = Board.read_board(file)

        tableFormat2["Board"].append(board_name[7:])
        bp0 = BloxorzProblem(board)
        searcher = searchGeneric.AStarMultiPruneSearcher(bp0)
        result = searcher.search()

        if result is None:
          print("For board %s, found no solution!" % (board_name,))
          tableFormat2['AstarMUltiPrune_length'].append(0)
          tableFormat2['AstarMUltiPrune_expansions'].append(0)
        else:
          sequence = [arc.action for arc in result.arcs()]
          print("For board %s, found solution with length %d using %d expansions" % (board_name, len(sequence), searcher.num_expanded))
          tableFormat2['AstarMUltiPrune_length'].append((len(sequence)))
          tableFormat2["AstarMUltiPrune_expansions"].append((searcher.num_expanded))
          continue
        #dataframe and converion to xml and html file with a average of the lengths and expansions

        df2=pd.DataFrame(tableFormat2)
        average=df2["AstarMUltiPrune_length"].mean()
        average2=df2["AstarMUltiPrune_expansions"].mean()
        print(average, average2)

        new_row={"Board"  : "Average",
                  "AstarMUltiPrune_length"   :average,
                  "AstarMUltiPrune_expansions"  :average2}
        df2=df2.append(new_row, ignore_index=True)
        
        
        df2.to_excel("/content/drive/My Drive/AI/table2.xlsx", index=False)
        htmlsetup=df2.to_html(index=False)
        html_file= open("/content/drive/My Drive/AI/htmlFile2.html","w")
        html_file.write(htmlsetup)
        html_file.close()

        print(df2)

#testing for Astarsearching
    for board_name in board_names:
        # print("Hello testing for loop")
        if board_name[7:-4] in noSolution_board:

          print('unsolvable board '+ str(board_name[7:]))
          continue

        print("Loading board file %s" % (board_name,))
        with open(board_name) as file:
            board = Board.read_board(file)

        tableFormat3["Board"].append(board_name[7:])
        bp0 = BloxorzProblem(board)

        # bp0.heuristic = bp0.heuristic1
        searcher = searchGeneric.AStarSearcher(bp0)
        result = searcher.search()

        if result is None:
          print("For board %s, found no solution!" % (board_name,))
          tableFormat3['AStar_Length'].append(0)
          tableFormat3['Astar_expansions'].append(0)
        else:
          sequence = [arc.action for arc in result.arcs()]
          #print("For board %s, found solution with length %d using %d expansions" % (board_name, len(sequence), searcher.num_expanded))
          tableFormat3['AStar_Length'].append(len(sequence))
          tableFormat3['Astar_expansions'].append(searcher.num_expanded)
          continue
          #dataframe and converion to xml and html file with a average of the lengths and expansions

        df3=pd.DataFrame(tableFormat3)
        average=df3["AStar_Length"].mean()
        average2=df3["Astar_expansions"].mean()
        print(average, average2)

        new_row={"Board"  : "Average",
                  "Astar_expansions"   :average,
                  "Astar_expansions"  :average2}
        df3=df3.append(new_row, ignore_index=True)

        df3.to_excel("/content/drive/My Drive/AI/table3.xlsx", index=False)
        htmlsetup=df3.to_html(index=False)
        html_file= open("/content/drive/My Drive/AI/htmlFile3.html","w")
        html_file.write(htmlsetup)
        html_file.close()
        print(df3)
           

        
    print(); print()






