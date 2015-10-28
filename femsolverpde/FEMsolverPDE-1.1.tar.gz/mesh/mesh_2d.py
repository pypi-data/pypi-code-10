# -*- coding: utf-8 -*-
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
import numpy as np
import matplotlib.pyplot as plt

import triangle

from mesh import Mesh
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
class Mesh2D(Mesh):
    '''
    ___DESCRIPTION____________________________________________________________
    Construct 2D mesh. * See parent class Mesh for more information.
    '''
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    def __init__(self):
        Mesh.__init__(self)
        self.p_dim = 2
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    def construct(self, params):
        '''
        ___INPUT______________________________________________________________
        params- parameters of selected mesh
                type: dict
            'mesh_type' - mesh type
                          type: str : 'rect', 'tangl_from_rect', 'tangl_delone'
            'x_lim'     - are min-max values of x
                          type: list [2] of float
            'y_lim'     - are min-max values of y
                          type: list [2] of float
            'size'      - total number of points for 'rect', 'tangl_from_rect'
                        - element's maximum relative volume for 'tangl_delone'
                          type: int
        '''
        self.mesh_type = params['mesh_type']
        self.x_lim = params['x_lim']; self.y_lim = params['y_lim']
        self.vol = abs((self.x_lim[1]-self.x_lim[0])*(self.y_lim[1]-self.y_lim[0]))
        if self.mesh_type == 'rect':
            self.p, self.e_con = create_rect(self.x_lim, self.y_lim, 
                                             params['size'])
        elif self.mesh_type == 'tangl_from_rect':
            self.p, self.e_con = create_tangl_from_rect(self.x_lim, self.y_lim, 
                                                        params['size'])
        elif self.mesh_type == 'tangl_delone':
            self.p, self.e_con = create_tangl_delone(self.x_lim, self.y_lim, 
                                                     params['size'])                                      
        else:
            print 'Error in Mesh2D.construct: unknown mesh type.'; return
        self.p_num = self.p.shape[1]
        self.e_dim = self.e_con.shape[0]
        self.e_num = self.e_con.shape[1]
        self.e_centers, self.e_volumes = centers_volumes(self.p, self.e_con)
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    def construct_bd(self):
        ''' (Inner function) See construct_borders().  '''
        self.rd_con = r_con(self.p, self.e_con, self.bd_nums, self.x_lim, self.y_lim)
        self.rd_num = self.rd_con.shape[1] 
        self.rd_centers, self.rd_volumes = centers_volumes(self.p, self.rd_con)
        self.pd_con = np.array(sorted(list(set(self.rd_con.reshape(-1)))))
        self.pd_num = len(self.pd_con)
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    def construct_bn(self):
        ''' (Inner function) See construct_borders().  '''
        self.rn_con = r_con(self.p, self.e_con, self.bn_nums, self.x_lim, self.y_lim)
        self.rn_num = self.rn_con.shape[1] 
        self.rn_centers, self.rn_volumes = centers_volumes(self.p, self.rn_con)
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    def construct_bi(self):
        ''' (Inner function) See construct_borders().  '''
        self.ri_con = r_con(self.p, self.e_con, self.bi_nums, self.x_lim, self.y_lim)
        self.ri_num = self.ri_con.shape[1] 
        self.ri_centers, self.ri_volumes = centers_volumes(self.p, self.ri_con)
        self.pi_con = np.array(sorted(list(set(self.ri_con.reshape(-1)))))
        self.pi_num = len(self.pi_con)
        ri_con_tmp = list(self.ri_con.reshape(-1))
        self.pi_corn_con = []
        for i, p_num in enumerate(ri_con_tmp):
            if ri_con_tmp.count(p_num)==1:
                self.pi_corn_con.append(p_num)
        self.pi_corn_con = np.array(self.pi_corn_con)
        self.pi_corn_num = len(self.pi_corn_con)
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    def show(self, p=False, p_txt=False, e=False, e_txt=False, 
             rd=False, rd_txt=False, pd=False, pd_txt=False,
             rn=False, rn_txt=False, pi=False, pi_txt=False):
        ''' Present constructed mesh on one plot.
            p - points, e - elements, r - ridges (d- Dirichlet, n - Neumann),
            pi - points of interest.  ''' 
        if p: show_p(self)
        if p_txt: show_p_txt(self)
        if e: show_e(self)
        if e_txt: show_e_txt(self)
        if rd: show_rd(self)
        if rd_txt: show_rd_txt(self)
        if pd: show_pd(self)
        if pd_txt: show_pd_txt(self)
        if rn: show_rn(self)
        if rn_txt: show_rn_txt(self)
        if pi: show_pi(self)
        if pi_txt: show_pi_txt(self)
        plt.show()
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    def __str__(self):
        return show_info(self)
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def create_rect(x_lim, y_lim, size):
    '''
    ___DESCRIPTION____________________________________________________________
    Construct 2D rectangular mesh of rectangles parallel to the coordinate axis.
    ___INPUT__________________________________________________________________
    x_lim  - are limits of x
             type: list [2] of float
    y_lim  - are limits of y
             type: list [2] of float
    size   - total number of points
             type: int (sqrt(size) must be int)
    ___OUTPUT_________________________________________________________________
    p      - mesh points
             type: ndarray [2, p_num] of float
    e_con  - connection matrix of the elements
             type: ndarray [4, e_num] of int
    '''
    size1d = int(np.sqrt(size))
    if size1d**2 != size:
        print 'Warning in Mesh2D.create_rect: mesh size is not exact 2-power.'
    p = np.zeros((2, size))
    e_con = np.zeros((4, (size1d-1)**2), dtype=int)
    p_num_curr = 0; e_num_curr = 0
    for i in range(size1d):
        for j in range(size1d):
            p[0, p_num_curr] = x_lim[0] + (x_lim[1]-x_lim[0]) / (size1d-1) * i
            p[1, p_num_curr] = y_lim[0] + (y_lim[1]-y_lim[0]) / (size1d-1) * j
            p_num_curr += 1
            if (i>=size1d-1) or (j>=size1d-1):
                continue
            e_con[0, e_num_curr] = size1d*i + j
            e_con[1, e_num_curr] = size1d*(i+1) + j
            e_con[2, e_num_curr] = size1d*(i+1) + (j+1)
            e_con[3, e_num_curr] = size1d*i + (j+1)
            e_num_curr += 1
    return p, e_con
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def create_tangl_from_rect(x_lim, y_lim, size):
    '''
    ___DESCRIPTION____________________________________________________________
    Construct 2D triangular mesh by partition (into two triangles)
    of rectangles parallel to the coordinate axis.
    ___INPUT__________________________________________________________________
    x_lim  - are limits of x
             type: list [2] of float
    y_lim  - are limits of y
             type: list [2] of float
    size   - total number of points
             type: int (sqrt(size) must be int)
    ___OUTPUT_________________________________________________________________
    p      - mesh points
             type: ndarray [2, p_num] of float
    e_con  - connection matrix of the elements
             type: ndarray [3, e_num] of int
    '''
    size1d = int(np.sqrt(size))
    if size1d**2 != size:
        print 'Warning in Mesh2D.create_tangl_from_rect: mesh size is not exact 2-power.'
    p = np.zeros((2, size))
    e_con = np.zeros((3, 2*(size1d-1)**2), dtype=int)
    p_num_curr = 0; e_num_curr = 0
    for i in range(size1d):
        for j in range(size1d):
            p[0, p_num_curr] = x_lim[0] + (x_lim[1]-x_lim[0]) / (size1d-1) * i
            p[1, p_num_curr] = y_lim[0] + (y_lim[1]-y_lim[0]) / (size1d-1) * j
            p_num_curr += 1
            if (i>=size1d-1) or (j>=size1d-1):
                continue
            e_con[0, e_num_curr] = size1d*i + (j+1)
            e_con[1, e_num_curr] = size1d*i + j
            e_con[2, e_num_curr] = size1d*(i+1) + (j+1)
            e_num_curr += 1
            e_con[0, e_num_curr] = size1d*(i+1) + j
            e_con[1, e_num_curr] = size1d*(i+1) + (j+1)
            e_con[2, e_num_curr] = size1d*i + j
            e_num_curr += 1
    return p, e_con
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def create_tangl_delone(x_lim, y_lim, size):
    '''
    ___DESCRIPTION____________________________________________________________
    Construct 2D triangular mesh by Delone triangulation.
    ___INPUT__________________________________________________________________
    x_lim  - are limits of x
             type: list [2] of float
    y_lim  - are limits of y
             type: list [2] of float
    size   - element's maximum relative volume
             type: int, float
    ___OUTPUT_________________________________________________________________
    p      - mesh points
             type: ndarray [2, p_num] of float
    e_con  - connection matrix of the elements
             type: ndarray [3, e_num] of int
    '''
    D = dict(vertices=np.array(((x_lim[0],y_lim[0]),    \
                                (x_lim[1],y_lim[0]),    \
                                (x_lim[1],y_lim[1]),    \
                                (x_lim[0],y_lim[1])   )))
    Mesh = triangle.triangulate(D, 'qa'+str(1./size))
    p = Mesh.items()[1][1].T
    e_con = Mesh.items()[2][1].T
    return p, e_con
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def r_con(p, e_con, b_nums, x_lim, y_lim, zero=1.E-10):
    '''
    ___DESCRIPTION____________________________________________________________
    Construct connection matrix for ridges on selected border.
    ___INPUT__________________________________________________________________
    p        - mesh points
               type: ndarray [2, p_num] of float
    e_con    - connection matrix of the elements
               type: ndarray [2, e_num] of int
    b_nums   - numbers of borders
               type: list of int (0-left, 1-up, 2-right, 3-down)
    x_lim    - are limits of x
               type: list [2] of float
    y_lim    - are limits of y
               type: list [2] of float   
    zero     - (optional) is a zero level
               type: float
    ___OUTPUT_________________________________________________________________
    r_con    - connection matrix of the ridges
               type: ndarray [2, r_num] of int
    '''
    r_con = []
    for j in range(e_con.shape[1]):
        p_nums = [[], [], [], []]
        for i in range(e_con.shape[0]):
            if abs(p[0, e_con[i, j]] - x_lim[0]) <= zero:
                p_nums[0].append(e_con[i, j])
            if abs(p[1, e_con[i, j]] - y_lim[1]) <= zero:
                p_nums[1].append(e_con[i, j])
            if abs(p[0, e_con[i, j]] - x_lim[1]) <= zero:
                p_nums[2].append(e_con[i, j])
            if abs(p[1, e_con[i, j]] - y_lim[0]) <= zero:
                p_nums[3].append(e_con[i, j])
        for b_num in b_nums:
            if len(p_nums[b_num]) == 2:
                r_con.append(sorted(p_nums[b_num]))
    return np.array(r_con).T
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def centers_volumes(p, con):
    '''
    ___DESCRIPTION____________________________________________________________
    Find centers and volumes of given mesh elements or ridges.
    ___INPUT__________________________________________________________________
    p        - mesh points
               type: ndarray [2, p_num] of float
    con      - connection matrix of the elements or ridges
               type: ndarray [dim, num] of int
    ___OUTPUT_________________________________________________________________
    centers  - centers of mesh elements or ridges
               type: ndarray [2, num] of float
    volumes  - volumes of mesh elements or ridges
               type: ndarray [num] of float
    '''
    centers = np.zeros((p.shape[0], con.shape[1]))
    volumes = np.zeros(con.shape[1])
    for j in range(con.shape[1]):
        pois = p[:, con[:, j]]
        centers[:, j] = np.sum(pois, axis=1) / con.shape[0]
        if con.shape[0] == 2:
            volumes[j] = float(np.linalg.norm(pois[:, 1] - pois[:, 0]))
        elif con.shape[0] == 3:
            AB = pois[:, 1] - pois[:, 0]
            AC = pois[:, 2] - pois[:, 0]
            volumes[j] = abs(AB[0]*AC[1]-AB[1]*AC[0])/2.
        elif con.shape[0] == 4:
            AB = pois[:, 1] - pois[:, 0]
            BC = pois[:, 2] - pois[:, 1]
            CD = pois[:, 3] - pois[:, 2]
            DA = pois[:, 0] - pois[:, 3]
            volumes[j] = abs(AB[0]*BC[1]-AB[1]*BC[0])/2. + \
                         abs(CD[0]*DA[1]-CD[1]*DA[0])/2.
        else:
            print 'Error in mesh_2d_utils.centers_volumes: incorrect con matrix'
    return centers, volumes
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def show_p(Mesh):
    plt.scatter(Mesh.p[0, :], Mesh.p[1, :], c='blue')
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def show_p_txt(Mesh):
    for j in range(Mesh.p_num):
        plt.text(Mesh.p[0, j], Mesh.p[1, j], 'p%d'%j)
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def show_e(Mesh):
    for j in range(Mesh.e_num):
        for i1 in range(Mesh.e_con.shape[0]):
            if i1 < Mesh.e_con.shape[0]-1:
                i2 = i1 + 1
            else:
                i2 = 0
            P1 = Mesh.p[:, Mesh.e_con[i1, j]]
            P2 = Mesh.p[:, Mesh.e_con[i2, j]]
            plt.plot([P1[0], P2[0]], [P1[1], P2[1]], c='black')
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def show_e_txt(Mesh): 
    for j in range(Mesh.e_num):
        plt.scatter(Mesh.e_centers[0, j], Mesh.e_centers[1, j], c='green')
        plt.text(Mesh.e_centers[0, j], Mesh.e_centers[1, j], 'e%d'%j)
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def show_rd(Mesh):
    for j in range(Mesh.rd_num):
        P1 = Mesh.p[:, Mesh.rd_con[0, j]]
        P2 = Mesh.p[:, Mesh.rd_con[1, j]]
        plt.plot([P1[0], P2[0]], [P1[1], P2[1]], c='magenta')
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def show_rd_txt(Mesh):
    for j in range(Mesh.rd_num):
        plt.scatter(Mesh.rd_centers[0, j], Mesh.rd_centers[1, j], c='green')
        plt.text(Mesh.rd_centers[0, j], Mesh.rd_centers[1, j], 'rd%d'%j)
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def show_pd(Mesh):
    plt.scatter(Mesh.p[0, Mesh.pd_con], Mesh.p[1, Mesh.pd_con], c='blue')
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def show_pd_txt(Mesh):
    for j in range(Mesh.pd_num):
        p = Mesh.p[:, Mesh.pd_con[j]]
        plt.scatter(p[0], p[1], c='blue')
        plt.text(p[0], p[1], 'pd%d'%Mesh.pd_con[j])
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def show_rn(Mesh):
    for j in range(Mesh.rn_num):
        P1 = Mesh.p[:, Mesh.rn_con[0, j]]
        P2 = Mesh.p[:, Mesh.rn_con[1, j]]
        plt.plot([P1[0], P2[0]], [P1[1], P2[1]], c='brown')
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def show_rn_txt(Mesh):
    for j in range(Mesh.rn_num):
        plt.scatter(Mesh.rn_centers[0, j], Mesh.rn_centers[1, j], c='green')
        plt.text(Mesh.rn_centers[0, j], Mesh.rn_centers[1, j], 'rn%d'%j)
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def show_pi(Mesh):
    plt.scatter(Mesh.p[0, Mesh.pi_con], Mesh.p[1, Mesh.pi_con], c='blue')
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def show_pi_txt(Mesh):
    for j in range(Mesh.pi_num):
        p_num = Mesh.pi_con[j]; p = Mesh.p[:, p_num]
        if p_num in Mesh.pi_corn_con:
            plt.text(p[0], p[1], 'pi%d(corn)'%p_num)
        else:
            plt.text(p[0], p[1], 'pi%d'%p_num)
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def show_info(Mesh):
    s = '------------- Mesh description  (type: ' + Mesh.mesh_type + ').'
    s+= '\n X/Y limits                    : '
    s+= Mesh.x_lim.__str__() +' / ' + Mesh.y_lim.__str__()
    s+= '\n Dimension/Number of points    : %d / %d'
    s = s%(Mesh.p_dim, Mesh.p_num)
    s+= '\n Dimension/Number of elements  : %d / %d'
    s = s%(Mesh.e_dim, Mesh.e_num)
    s+= '\n Max/Min volume of elements    : %-10.6f / %-10.6f'
    s = s%(np.max(Mesh.e_volumes), np.min(Mesh.e_volumes))
    s+= '\n Dirichlet/Neumann borders     : '
    s+= Mesh.bd_nums.__str__() +' / ' + Mesh.bn_nums.__str__()
    s+= '\n Number of D./N. ridges        : %d / %d'
    s = s%(Mesh.rd_num, Mesh.rn_num)
    s+= '\n Max/Min volume of D. ridges   : %-10.6f / %-10.6f'
    s = s%(np.max(Mesh.rd_volumes), np.min(Mesh.rd_volumes))                                                                  
    s+= '\n Max/Min volume of N. ridges   : %-10.6f / %-10.6f'
    s = s%(np.max(Mesh.rn_volumes), np.min(Mesh.rn_volumes)) 
    s+= '\n Number of points of interest  : %d'
    s = s%(Mesh.pi_num)          
    return s
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=