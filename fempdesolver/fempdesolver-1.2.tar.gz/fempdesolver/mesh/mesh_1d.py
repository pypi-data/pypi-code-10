# -*- coding: utf-8 -*-
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
SHOW_Y = 4.; SHOW_DY = 0.003
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
import numpy as np
import matplotlib.pyplot as plt

from mesh import Mesh
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
class Mesh1D(Mesh):
    '''
    ___DESCRIPTION____________________________________________________________
    Construct 1D mesh. * See parent class Mesh for more information.
    '''
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    def __init__(self):
        Mesh.__init__(self)
        self.p_dim = 1
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    def construct(self, params):
        '''
        ___INPUT______________________________________________________________
        params- parameters of selected mesh
                type: dict
            'mesh_type' - mesh type
                          type: str : 'simple'
            'x_lim'     - are min-max values of x
                          type: list [2] of float
            'size'      - total number of points
                          type: int
        '''
        self.mesh_type = params['mesh_type']
        self.x_lim = params['x_lim']
        self.vol = abs(self.x_lim[1]-self.x_lim[0])
        if self.mesh_type == 'simple':
            self.p = []
            for i in range(params['size']):
                self.p.append(self.x_lim[0]+
                              (self.x_lim[1]-self.x_lim[0])/(params['size']-1)*i)
            self.p = np.array(self.p).reshape((1, -1))            
            self.e_con = np.zeros((2, params['size']-1), dtype=int)
            self.e_centers = np.zeros((1, params['size']-1)) 
            self.e_volumes = np.zeros(params['size']-1)
            for i in range(params['size']-1):             
                self.e_con[:, i] = [i, i+1]
                self.e_centers[:, i] = (self.p[:, i+1] + self.p[:, i])/2.
                self.e_volumes[i] = abs(self.p[0, i+1] - self.p[0, i]) 
        else:
            print 'Error in Mesh1D.construct: unknown mesh type.'; return
        self.p_num = self.p.shape[1]
        self.e_dim = self.e_con.shape[0]
        self.e_num = self.e_con.shape[1]
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    def construct_bd(self):
        ''' (Inner function) See construct_borders().  '''
        self.rd_num = len(self.bd_nums)
        self.rd_con = np.zeros((1, self.rd_num), dtype=int)
        self.rd_centers = np.zeros((1, self.rd_num))
        self.rd_volumes = np.zeros(self.rd_num)
        for i, bd_num in enumerate(self.bd_nums):
            if bd_num == 0:
                self.rd_con[i] = 0
                self.rd_centers[i] = self.p[:, 0]
            elif bd_num == 2:
                self.rd_con[i] = self.p_num-1
                self.rd_centers[i] = self.p[:, self.p_num-1]
            else:
                print 'Error in Mesh1D.construct_bd: incorrect bd_nums.'; return
        self.pd_con = self.rd_con.copy().reshape(-1)
        self.pd_num = self.rd_num
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    def construct_bn(self):
        ''' (Inner function) See construct_borders().  '''
        self.rn_num = len(self.bn_nums)
        self.rn_con = np.zeros((1, self.rn_num), dtype=int)
        self.rn_centers = np.zeros((1, self.rn_num))
        self.rn_volumes = np.zeros(self.rn_num)
        for i, bn_num in enumerate(self.bn_nums):
            if bn_num == 0:
                self.rn_con[i] = 0
                self.rn_centers[i] = self.p[:, 0]
            elif bn_num == 2:
                self.rn_con[i] = self.p_num-1
                self.rn_centers[i] = self.p[:, self.p_num-1]
            else:
                print 'Error in Mesh1D.construct_bn: incorrect bn_nums.'; return
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    def construct_bi(self):
        ''' (Inner function) See construct_borders().  '''
        self.ri_num = len(self.bi_nums)
        self.ri_con = np.zeros((1, self.ri_num), dtype=int)
        self.ri_centers = np.zeros((1, self.ri_num))
        self.ri_volumes = np.zeros(self.ri_num)
        for i, bi_num in enumerate(self.bi_nums):
            if bi_num == 0:
                self.ri_con[i] = 0
                self.ri_centers[i] = self.p[:, 0]
            elif bi_num == 2:
                self.ri_con[i] = self.p_num-1
                self.ri_centers[i] = self.p[:, self.p_num-1]
            else:
                print 'Error in Mesh1D.construct_bi: incorrect bi_nums.'; return
        self.pi_con = self.ri_con.copy().reshape(-1)
        self.pi_num = self.ri_num
        self.pi_corn_con = self.pi_con.copy()
        self.pi_corn_num = self.pi_num
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
        plt.ylim(SHOW_Y-SHOW_DY*10, SHOW_Y+SHOW_DY*10)
        plt.show()
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    def __str__(self):
        return show_info(self)
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def show_p(Mesh):
    for j in range(Mesh.p_num):
        plt.scatter(Mesh.p[0, j], SHOW_Y, c='blue')
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def show_p_txt(Mesh):
    for j in range(Mesh.p_num):
        plt.text(Mesh.p[0, j], SHOW_Y + SHOW_DY, 'p%d'%j)
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def show_e(Mesh):
    for j in range(Mesh.e_num):
        for i1 in range(Mesh.e_con.shape[0]):
            for i2 in range(i1+1, Mesh.e_con.shape[0]): 
                P1 = Mesh.p[:, Mesh.e_con[i1, j]]
                P2 = Mesh.p[:, Mesh.e_con[i2, j]]
                plt.plot([P1[0], P2[0]], [SHOW_Y, SHOW_Y], c='black')
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def show_e_txt(Mesh): 
    for j in range(Mesh.e_num):
        plt.scatter(Mesh.e_centers[0, j], SHOW_Y, c='green')
        plt.text(Mesh.e_centers[0, j], SHOW_Y - SHOW_DY, 'e%d'%j)
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def show_rd(Mesh):
    pass
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def show_rd_txt(Mesh):
    for j in range(Mesh.rd_num):
        plt.scatter(Mesh.rd_centers[0, j], SHOW_Y, c='green')
        plt.text(Mesh.rd_centers[0, j], SHOW_Y - SHOW_DY, 'rd%d'%j)
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def show_pd(Mesh):
    plt.scatter(Mesh.p[0, Mesh.pd_con], SHOW_Y, c='blue')
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def show_pd_txt(Mesh):
    for j in range(Mesh.pd_num):
        p = Mesh.p[:, Mesh.pd_con[j]]
        plt.scatter(p[0], SHOW_Y, c='blue')
        plt.text(p[0], SHOW_Y - SHOW_DY, 'pd%d'%Mesh.pd_con[j])
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def show_rn(Mesh):
    pass
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def show_rn_txt(Mesh):
    for j in range(Mesh.rn_num):
        plt.scatter(Mesh.rn_centers[0, j], SHOW_Y, c='green')
        plt.text(Mesh.rn_centers[0, j], SHOW_Y - SHOW_DY, 'rn%d'%j)
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def show_pi(Mesh):
    plt.scatter(Mesh.p[0, Mesh.pi_con], SHOW_Y, c='blue')
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def show_pi_txt(Mesh):
    for j in range(Mesh.pi_num):
        p_num = Mesh.pi_con[j]; p = Mesh.p[:, p_num]
        if p_num in Mesh.pi_corn_con:
            plt.text(p[0], SHOW_Y - SHOW_DY, 'pi%d(corn)'%p_num)
        else:
            plt.text(p[0], SHOW_Y - SHOW_DY, 'pi%d'%p_num)
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def show_info(Mesh):
    s = '------------- Mesh description  (type: ' + Mesh.mesh_type + ').'
    s+= '\n X limits                      : '
    s+= Mesh.x_lim.__str__()
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
    s+= '\n Number of points of interest  : %d'
    s = s%(Mesh.pi_num)          
    return s
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=




