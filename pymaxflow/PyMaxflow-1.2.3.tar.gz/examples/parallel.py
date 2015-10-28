
"""
Shows an example of how to perform parallel maxflow computation over a single
graph using the method from [Strandmark2010].

[Strandmark2010] P. Strandmark, F. Kahl, "Parallel and distributed graph cuts by
  dual decomposition," 2010 IEEE Conference on Computer Vision and Pattern
  Recognition (CVPR2010), pp.2085-2092, June 2010
"""

import numpy as np
import maxflow

def main():
    
    shape = (7, 7)
    half = 7 // 2
    
    g = maxflow.Graph[float]()
    nodeids = g.add_grid_nodes(shape)
    
    
