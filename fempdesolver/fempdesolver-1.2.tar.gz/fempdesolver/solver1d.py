# -*- coding: utf-8 -*-
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import spsolve
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
class Fem1D(object):
    '''
    ___DESCRIPTION____________________________________________________________
    Solve 1D PDE by finite elements method.
    All functions with PDE parameters wait as input 1D numpy arrays with
    parameters values on centers of finite elements or in centers of 
    appropriate mesh ridges (for boundary coefficients).
    PDE: -1* div(c(x)*grad(u(x)))+b(x)*grad(u(x))+a(x)*u(x)=f(x),
                 b(x) = [b1(x)]       , x = [x1],
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
        Mesh         - is the constructed mesh in the X-domain
                       type: Mesh1D
        '''
        self.Mesh = Mesh
        self.K = None; self.F = None
        self.H = None; self.G = None; self.D = None
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    def calc_fe_int(self):
        return
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    def calc_N(self):
        return
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    def calc_K(self, a=None, b=None, c=None):
        if a is None: a=np.zeros(self.Mesh.e_num)
        if b is None: pass
        if c is None: c=np.zeros(self.Mesh.e_num)
        if isinstance(a, list): a=np.array(a)
        if isinstance(b, list): b=np.array(b)
        if isinstance(c, list): c=np.array(c)
        a0 = a * self.Mesh.e_volumes / 6.
        ad = a0 * 2 # 1*diag elem
        c0 =-c / self.Mesh.e_volumes
        cd =-c0 # 1*diag elem
        k12 = c0 + a0
        n = self.Mesh.p_num
        con1 = self.Mesh.e_con[0, :]
        con2 = self.Mesh.e_con[1, :]
        self.K =          csr_matrix((k12, (con1, con2)), shape=(n, n))
        self.K = self.K + self.K.T
        self.K = self.K + csr_matrix((ad + cd, (con1, con1)), shape=(n, n))
        self.K = self.K + csr_matrix((ad + cd, (con2, con2)), shape=(n, n))
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    def calc_F(self, f=None):
        if f is None: return
        f0 = f * self.Mesh.e_volumes / 2.
        n = self.Mesh.p_num
        con1 = self.Mesh.e_con[0, :]
        con2 = self.Mesh.e_con[1, :]
        self.F =          csr_matrix((f0, (con1, np.zeros(len(f0)))), 
                                     shape=(n, 1))
        self.F = self.F + csr_matrix((f0, (con2, np.zeros(len(f0)))), 
                                     shape=(n, 1))
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    def calc_H(self, s=None):
        return
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    def calc_G(self, m=None):
        if m is None: return
        self.Bd_m = m
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    def calc_D(self, d):
        if d is None: return 
        self.Bd_Ud = d
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    def _construct_K0F0(self):
        '''
        ___DESCRIPTION________________________________________________________
        (Inner function) Calculate K0 and F0 matrices.
        ___INPUT______________________________________________________________
        OutType      - (optional) is a type of output
                       type: str :
                           'K', 'KF'
        ___OUTPUT_____________________________________________________________
        K0,FO        - are K0 and F0 matrices
        '''
        K0 = self.K.copy()
        F0 = self.F.copy() 
        for i,Poi in enumerate(self.Mesh.pd_con):
            if Poi != 0:
                K0[Poi,Poi-1]= 0
            if Poi != self.Mesh.p_num-1:
                K0[Poi,Poi+1]= 0
            K0[Poi,Poi]  = 1
            if Poi != 0:
                F0[Poi-1,0]-=K0[Poi-1,Poi] * self.Bd_Ud[i]
            F0[Poi  ,0]-=K0[Poi,Poi] * self.Bd_Ud[i]
            if Poi != self.Mesh.p_num-1:
                F0[Poi+1,0]-=K0[Poi+1,Poi] * self.Bd_Ud[i]
            F0[Poi,0]=self.Bd_Ud[i]
            if Poi != 0:
                K0[Poi-1,Poi]= 0
            if Poi != self.Mesh.p_num-1:
                K0[Poi+1,Poi]= 0
            K0[Poi,Poi]  = 1
        for i,Poi in enumerate(self.Mesh.rn_con[0, :]):
            F0[Poi,0]+=self.Bd_m[i]
        return K0, F0
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    def solve(self):
        '''
        ___DESCRIPTION________________________________________________________
        Solve PDE using prepared descritization matrices.
        ___OUTPUT_____________________________________________________________
        U0           - is the PDE solution in all mesh nodes
        K            - is the K matrix in PDE form K U0 = F
        '''
        K0, F0 = self._construct_K0F0()
        U0 = spsolve(K0,F0)
        #self.U0 = np.array([U0[i, 0] for i in range(U0.shape[0])])
        return U0, self.K
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=








