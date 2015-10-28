# -*- coding: utf-8 -*-
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
class Mesh(object):
    '''
    ___DESCRIPTION____________________________________________________________
    Parent (virtual) class for construction of 1D and 2D mesh 
    (only for rectangular domain for 2D case in current version).
    Available 1D mesh types: 
           'simple':          mesh is divided into segments of equal length.
    Available 2D mesh types: 
           'rect':            rectangles parallel to the coordinate axes,
           'tangl_from_rect': rectangles parallel to the coordinate axes 
                              are divided into two triangles. 
           'tangl_delone':    Delone triangulation.
    Main mesh parameters: connection (con) matrices (global indices of points) 
    for (finite) elements, ridges with Dirichlet (D), Neumann (N) 
    boundary conditions, points with Dirichlet boundary condition,
    ridges and points of interest (I).
    '''
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    def __init__(self):
        # General parameters:
        self.mesh_type = None
        self.x_lim = None
        self.y_lim = None
        self.vol = None     # total volume of the mesh 
        # Mesh points:
        self.p = None       # np.array [p_dim, p_num]
        self.p_dim = 0
        self.p_num = 0
        # Mesh (finite) elements:
        self.e_con = None   # np.array [e_dim, e_num]
        self.e_dim = 0
        self.e_num = 0
        self.e_centers = None
        self.e_volumes = None
        # Ridges with Dirichlet bound. cond.:
        self.bd_nums = []   # list with D. borders numbers
        self.rd_con = None  # np.array [2, rd_num]
        self.rd_num = 0
        self.rd_centers = None
        self.rd_volumes = None
        # Points with Dirichlet bound. cond.:
        self.pd_con = None  # np.array [pd_num]
        self.pd_num = 0
        # Ridges with Neumann bound. cond.:
        self.bn_nums = []   # list with N. borders numbers
        self.rn_con = None  # np.array [2, rn_num]
        self.rn_num = 0
        self.rn_centers = None
        self.rn_volumes = None
        # Ridges on border(s) of interest:
        self.bi_nums = []   # list with I. borders numbers
        self.ri_con = None  # np.array [2, ri_num]
        self.ri_num = 0
        self.ri_centers = None
        self.ri_volumes = None
        # Points on border(s) of interest:
        self.pi_con = None  # np.array [pi_num]
        self.pi_num = 0
        # Points on corners of border(s) of interest:
        self.pi_corn_con = None  # np.array [pi_corn_num]
        self.pi_corn_num = 0
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    def construct_borders(self, bd_nums=[], bn_nums=[], bi_nums=[]):
        '''
        ___INPUT______________________________________________________________
        bd_nums - numbers of borders with Dirichlet bound. cond.
                  type: list
        bn_nums - numbers of borders with Neumann bound. cond.
                  type: list
        bi_nums - numbers of borders of interest
                  type: list
        * Used numeration for borders: 0 - left; 1 - up; 2 - right; 3 - down.
        ** In 1D case only 0 - left and 2 - right may be used.
        '''
        if len(bd_nums) > 0:
            self.bd_nums = bd_nums
            self.construct_bd()
        if len(bn_nums) > 0:
            self.bn_nums = bn_nums
            self.construct_bn()
        if len(bi_nums) > 0:
            self.bi_nums = bi_nums
            self.construct_bi()
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=  
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=