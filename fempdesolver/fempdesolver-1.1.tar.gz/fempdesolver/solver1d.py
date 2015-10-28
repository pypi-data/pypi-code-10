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
    PDE: - div(c(x)*grad(u(x)))+b(x)*grad(u(x))+a(x)*u(x)=f(x),
                 b(x) = [b1(x)]       , x = [x1]    (1D) ,
                 b(x) = [b1(x),b2(x)] , x = [x1,x2] (2D) ,
                 Border 0:    u(x) = d(x) ,
                 Border 1:    c(x)*grad(u(x))*NormVect(x) + s(x)*u(x)= m(x)
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
        ___DESCRIPTION________________________________________________________
        Init parameters of calculation by None values.
        ___INPUT______________________________________________________________
        Mesh         - is the constructed mesh in the X-domain
                       type: Mesh1D
        '''
        self.Mesh = Mesh
        self.K = None
        self.F = None
        self.H = None
        self.G = None
        self.Ud = None
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    def Calc_fe_int(self):
        return
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    def Calc_N(self):
        return
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    def Calc_K(self, cf_a=0., cf_b=0., cf_c=0.):
        if isinstance(cf_a, (int, float)):
            cf_a = cf_a * np.ones(len(self.Mesh.VolFE))
        a0 = cf_a * self.Mesh.VolFE / 6.
        ad = a0 * 2 # 1*diag elem
        if isinstance(cf_c, (int, float)):
            cf_c = cf_c * np.ones(len(self.Mesh.VolFE))
        c0 =-Cf_c / self.Mesh.VolFE
        cd =-c0 # 1*diag elem
        k12 = c0 + a0
        self.K =          csr_matrix((k12,    (self.Mesh.FEI1,self.Mesh.FEI2)), shape=(self.Mesh.NumPoi,self.Mesh.NumPoi))
        self.K = self.K + self.K.T
        self.K = self.K + csr_matrix((ad + cd,(self.Mesh.FEI1,self.Mesh.FEI1)), shape=(self.Mesh.NumPoi,self.Mesh.NumPoi))
        self.K = self.K + csr_matrix((ad + cd,(self.Mesh.FEI2,self.Mesh.FEI2)), shape=(self.Mesh.NumPoi,self.Mesh.NumPoi))
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    def Calc_F(self,Cf_f=0.):
        if isinstance(Cf_f,(int,float)):
            Cf_f = Cf_f * np.ones(len(self.Mesh.VolFE))
        k = Cf_f * self.Mesh.VolFE / 2.
        self.F =          csr_matrix((k,(self.Mesh.FEI1,np.zeros(len(k)))), shape=(self.Mesh.NumPoi,1))
        self.F = self.F + csr_matrix((k,(self.Mesh.FEI2,np.zeros(len(k)))), shape=(self.Mesh.NumPoi,1))
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    def Calc_H(self,Bd_s=0.):
        return
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    def Calc_G(self,Bd_m=0.):
        if isinstance(Bd_m,(int,float)):
            Bd_m = Bd_m * np.ones(len(self.Mesh.VolEn))
        self.Bd_m = Bd_m
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    def Calc_Ud(self,Bd_Ud=0.):
        if isinstance(Bd_Ud,(int,float)):
            Bd_Ud = Bd_Ud * np.ones(len(self.Mesh.PdNums))   
        self.Bd_Ud = Bd_Ud
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    def ConstructK0F0(self,OutType='KF'):
        '''
        ___DESCRIPTION________________________________________________________
        (Inner function) Calculate K0 and F0 matrices.
        ___INPUT______________________________________________________________
        OutType      - (optional) is a type of output
                       type: str :
                           'K', 'KF'
        ___OUTPUT_____________________________________________________________
           if OutType=='K'
        K0           - is the K0 matrix
           if OutType=='KF'
        K0,FO        - are K0 and F0 matrices
        '''
        K0 = self.K.copy()
        F0 = self.F.copy() 
        for i,Poi in enumerate(self.Mesh.PdNums):
            if Poi != 0:
                K0[Poi,Poi-1]= 0
            if Poi != self.Mesh.NumPoi-1:
                K0[Poi,Poi+1]= 0
            K0[Poi,Poi]  = 1
            if Poi != 0:
                F0[Poi-1,0]-=K0[Poi-1,Poi] * self.Bd_Ud[i]
            F0[Poi  ,0]-=K0[Poi,Poi] * self.Bd_Ud[i]
            if Poi != self.Mesh.NumPoi-1:
                F0[Poi+1,0]-=K0[Poi+1,Poi] * self.Bd_Ud[i]
            F0[Poi,0]=self.Bd_Ud[i]
            if Poi != 0:
                K0[Poi-1,Poi]= 0
            if Poi != self.Mesh.NumPoi-1:
                K0[Poi+1,Poi]= 0
            K0[Poi,Poi]  = 1
        for i,Poi in enumerate(self.Mesh.EnI1):
            F0[Poi,0]+=self.Bd_m[i]
        return K0,F0
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
    def SolveMatrix(self):
        '''
        ___DESCRIPTION________________________________________________________
        Solve PDE using prepared descritization matrices.
        ___OUTPUT_____________________________________________________________
        U0           - is the PDE solution in all mesh nodes
        K            - is the K matrix in PDE form K U0 = F
        '''
        K0,F0 = self.ConstructK0F0(OutType='KF')
        U0    = spsolve(K0,F0)
        return U0.reshape((-1,1)),K0
    #=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=








