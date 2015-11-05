# -*- coding: utf-8 -*-
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import spsolve
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
class Fem2D(object):
    '''
    ___DESCRIPTION____________________________________________________________
    Solve 2D PDE by (triangular) finite elements method.
    All functions with PDE parameters wait as input 1D numpy arrays with
    parameters values on centers of finite elements or in centers of 
    appropriate mesh ridges (for boundary coefficients).
    PDE: -1* div(c(x)*grad(u(x)))+b(x)*grad(u(x))+a(x)*u(x)=f(x),
                 b(x) = [b1(x), b2(x)] , x = [x1, x2],
                 Border D:    u(x) = d(x) ,
                 Border N:    c(x)*grad(u(x))*NormVect(x) + s(x)*u(x)= m(x)
   * Only b(x) = None is avaliable now.
   The following names are used for PDE coefficients and related matrices:
                Coeff       Related FEM matrix name
                c, b, a     K
                f           F
                d           D
                s           H
                m           G
    '''
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    def __init__(self, Mesh):
        '''
        ___INPUT______________________________________________________________
        Mesh         - is the triangular mesh in the X-domain
                       type: Mesh2D
        '''
        self.Mesh = Mesh
        self.N = None; self.K = None; self.F = None; 
        self.H = None; self.G = None; self.D = None
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    def calc_fe_int(self):
        a1 = self.Mesh.p[:, self.Mesh.e_con[0, :]]
        a2 = self.Mesh.p[:, self.Mesh.e_con[1, :]]
        a3 = self.Mesh.p[:, self.Mesh.e_con[2, :]]

        self.grd1 = np.zeros((self.Mesh.p_dim, self.Mesh.e_num))
        self.grd2 = np.zeros((self.Mesh.p_dim, self.Mesh.e_num))
        self.grd3 = np.zeros((self.Mesh.p_dim, self.Mesh.e_num))

        self.grd1[0,:] = (a2[1] - a3[1]) / 2. / self.Mesh.e_volumes
        self.grd1[1,:] = (a3[0] - a2[0]) / 2. / self.Mesh.e_volumes

        self.grd2[0,:] = (a3[1] - a1[1]) / 2. / self.Mesh.e_volumes
        self.grd2[1,:] = (a1[0] - a3[0]) / 2. / self.Mesh.e_volumes

        self.grd3[0,:] = (a1[1] - a2[1]) / 2. / self.Mesh.e_volumes
        self.grd3[1,:] = (a2[0] - a1[0]) / 2. / self.Mesh.e_volumes
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    def calc_N(self):
        poi_ew = [i for i in range(self.Mesh.p_num) 
                  if not (i in self.Mesh.pd_con)]
        self.N = csr_matrix((np.ones(len(poi_ew)), 
                            (poi_ew, np.arange(len(poi_ew)))), 
                            shape=(self.Mesh.p_num, len(poi_ew)))
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    def calc_K(self, a=None, b=None, c=None):
        if a is None: a=np.zeros(self.Mesh.e_num)
        if b is None: pass
        if c is None: c=np.zeros(self.Mesh.e_num)
        a0 = a * self.Mesh.e_volumes / 12.
        ad = a0 * 4 # 2*diag elem
        cx =c * self.Mesh.e_volumes
        k12=cx*(self.grd1[0,:]*self.grd2[0,:]+self.grd1[1,:]*self.grd2[1,:])+a0
        k23=cx*(self.grd2[0,:]*self.grd3[0,:]+self.grd2[1,:]*self.grd3[1,:])+a0
        k31=cx*(self.grd3[0,:]*self.grd1[0,:]+self.grd3[1,:]*self.grd1[1,:])+a0
        n = self.Mesh.p_num
        con1 = self.Mesh.e_con[0, :]
        con2 = self.Mesh.e_con[1, :]
        con3 = self.Mesh.e_con[2, :]
        self.K =          csr_matrix((k12, (con1, con2)), shape=(n, n))
        self.K = self.K + csr_matrix((k23, (con2, con3)), shape=(n, n))
        self.K = self.K + csr_matrix((k31, (con3, con1)), shape=(n, n))
        self.K = self.K + self.K.T
        self.K = self.K + csr_matrix((ad-k31-k12, (con1, con1)), shape=(n, n))
        self.K = self.K + csr_matrix((ad-k12-k23, (con2, con2)), shape=(n, n))
        self.K = self.K + csr_matrix((ad-k23-k31, (con3, con3)), shape=(n, n))
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    def calc_F(self, f=None):
        if f is None: return
        f0 = f * self.Mesh.e_volumes / 3.
        n = self.Mesh.p_num
        con1 = self.Mesh.e_con[0, :]
        con2 = self.Mesh.e_con[1, :]
        con3 = self.Mesh.e_con[2, :]
        self.F =          csr_matrix((f0, (con1, np.zeros(len(f0)))), 
                                     shape=(n, 1))
        self.F = self.F + csr_matrix((f0, (con2, np.zeros(len(f0)))), 
                                     shape=(n, 1))
        self.F = self.F + csr_matrix((f0, (con3, np.zeros(len(f0)))), 
                                     shape=(n, 1))
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    def calc_H(self, s=None):
        if s is None: return
        s0 = s * self.Mesh.rn_volumes / 6.
        sd = s0 * 2.
        n = self.Mesh.p_num
        con1 = self.Mesh.rn_con[0, :]
        con2 = self.Mesh.rn_con[1, :]
        self.H =          csr_matrix((s0, (con1, con2)), shape=(n, n))
        self.H = self.H + csr_matrix((s0, (con2, con1)), shape=(n, n))
        self.H = self.H + csr_matrix((sd, (con1, con1)), shape=(n, n))
        self.H = self.H + csr_matrix((sd, (con2, con2)), shape=(n, n))
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    def calc_G(self, m=None):
        if m is None: return
        m0 = m * self.Mesh.rn_volumes / 2.
        n = self.Mesh.p_num
        con1 = self.Mesh.rn_con[0, :]
        con2 = self.Mesh.rn_con[1, :]
        self.G =          csr_matrix((m0, (con1, np.zeros(len(m0)))), 
                                     shape=(n, 1))
        self.G = self.G + csr_matrix((m0, (con2, np.zeros(len(m0)))), 
                                     shape=(n, 1))
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    def calc_D(self, d):
        if d is None: return
        self.D = csr_matrix((d, (self.Mesh.pd_con,np.zeros(self.Mesh.pd_num))), 
                            shape=(self.Mesh.p_num, 1))
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    def _construct_K0F0(self):
        '''
        ___DESCRIPTION________________________________________________________
        (Inner function) Calculate K0 and F0 matrices.
        ___OUTPUT_____________________________________________________________
        K0,FO        - are K0 and F0 matrices
        '''
        NT = self.N.T
        K0 = self.K.copy()
        if self.H != None:
            K0 = K0 + self.H
        F0 = self.F.copy()
        if self.G != None:
            F0 = F0 + self.G
        if self.D != None:
            F0 = F0 - K0.dot(self.D)
            F0 = NT.dot(F0)
            K0 = NT.dot(K0)
            K0 = K0.dot(self.N)
        return K0, F0
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    def solve(self):
        '''
        ___DESCRIPTION________________________________________________________
        Solve PDE using prepared discretization matrices.
        K0 = N.T (K+H) N
        F0 = N.T (F+G-(K+H)Ud)
        U0 is solution of K0 U0 = Fo
        U = N U0 + Ud - is the full solution
        ___OUTPUT_____________________________________________________________
        U0           - is the PDE solution in all mesh nodes
                       type: ndarray [Mesh.p_num] of float
        K            - is the K matrix in PDE of form K U0 = F
                       type: ndarray [Mesh.p_num, Mesh.p_num] of float
        '''

        K0, F0 = self._construct_K0F0()
        U0 = spsolve(K0,F0)
        U0 = self.N.dot(U0)
        U0 = U0.reshape((-1,1))
        if self.D != None:
            U0 = U0 + self.D
        self.U0 = np.array([U0[i, 0] for i in range(U0.shape[0])])
        return self.U0, self.K
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    def sol_in_poi(self, x, eps=1.E-10):
        '''
        ___DESCRIPTION________________________________________________________
        Construct approximation of solution's value in given point
        (interpolation is used).
        ___INPUT______________________________________________________________
        x            - is the space point
                       type: np.array [2]
        eps          - (optional) is a zero level
                       type: float
        ___OUTPUT_____________________________________________________________
        u            - is the solution
                       type: float
        '''
        for i in range(self.Mesh.e_num):
            p_nums = self.Mesh.e_con[:, i]
            w = tangl_interpol(self.Mesh.p[:,p_nums[0]], 
                               self.Mesh.p[:,p_nums[1]], 
                               self.Mesh.p[:,p_nums[2]], x)
            if w is not None:
                return sum([w[i]*self.U0[p_num] 
                           for i, p_num in enumerate(p_nums)])
        print 'Error in fem_2d.sol_in_poi: point is outside the mesh region.'
        return None
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def tangl_interpol(A, B, C, x, eps=1.E-10):
    if np.linalg.norm(A-x) < eps:
        return [1., 0., 0.]
    if np.linalg.norm(B-x) < eps:
        return [0., 1., 0.]
    if np.linalg.norm(C-x) < eps:
        return [0., 0., 1.]
    S_ABC = np.cross(C-A, B-A)
    S_ABX = np.cross(x-A, B-A)/S_ABC
    if S_ABX<-eps:
        return None
    S_ACX = np.cross(C-A, x-A)/S_ABC
    if S_ACX<-eps:
        return None
    S_CBX = np.cross(B-C, x-C)/S_ABC
    if S_CBX<-eps:
        return None
    return [S_CBX, S_ACX, S_ABX]
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=