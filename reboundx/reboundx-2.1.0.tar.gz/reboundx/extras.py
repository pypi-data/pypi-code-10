from . import clibreboundx
from ctypes import *
import rebound
import numpy as np
c_default = 10064.915

class rebx_param(Structure): # need to define fields afterward because of circular ref in linked list
    pass    
rebx_param._fields_ = [("valPtr", c_void_p),
            ("param", c_int),
            ("next", POINTER(rebx_param))]

class rebx_param_to_be_freed(Structure):
    pass
rebx_param_to_be_freed._fields_ = [("param", POINTER(rebx_param)),
            ("next", POINTER(rebx_param_to_be_freed))]

class rebx_params_modify_orbits(Structure):
    _fields_ = [("p", c_double),
                ("coordinates", c_int)]

class rebx_params_gr(Structure):
    _fields_ = [("c", c_double)]

class rebx_params_radiation_forces(Structure):
    _fields_ = [("L", c_double),
                ("c", c_double)]

class Extras(Structure):
    def __init__(self, sim):
        clibreboundx.rebx_initialize(byref(sim), byref(self)) # Use memory address ctypes allocated for rebx Structure in C
        self.add_Particle_props()
        self.coordinates = {"JACOBI":0, "BARYCENTRIC":1, "HELIOCENTRIC":2} # to use C version's REBX_COORDINATES enum

    def __del__(self):
        if self._b_needsfree_ == 1:
            clibreboundx.rebx_free_pointers(byref(self))

    def add_modify_orbits_direct(self):
        clibreboundx.rebx_add_modify_orbits_direct(byref(self))
    
    def add_modify_orbits_forces(self):
        clibreboundx.rebx_add_modify_orbits_forces(byref(self))

    def check_c(self, c):
        if c is not None: # user passed c explicitly
            return c
      
        # c was not passed by user
         
        if self.sim.contents.G == 1: # if G = 1 (default) return default c
            return c_default
            
        u = self.sim.contents.units
        if not None in u.values(): # units are set
            c = rebound.units.convert_vel(c_default, 'au', 'yr2pi', u['length'], u['time'])
            return c
        else:
            raise ValueError("If you change G, you must pass c (speed of light) in appropriate units to add_gr, add_gr_potential, and add_gr_implicit.  Alternatively, set the units for the simulation.  See ipython_examples/GeneralRelativity.ipynb")
              
        return c_default
    def add_gr(self, c=None):
        c = self.check_c(c)
        clibreboundx.rebx_add_gr(byref(self), c_double(c))
    
    def add_gr_single_mass(self, c=None):
        c = self.check_c(c)
        clibreboundx.rebx_add_gr_single_mass(byref(self), c_double(c))

    def add_gr_potential(self, c=None):
        c = self.check_c(c)
        clibreboundx.rebx_add_gr_potential(byref(self), c_double(c))
    
    def add_radiation_forces(self, c, L):
        clibreboundx.rebx_add_radiation_forces(byref(self), c_double(c), c_double(L))

    def add_Particle_props(self):
        @property
        def tau_a(self):
            clibreboundx.rebx_get_tau_a.restype = c_double
            return clibreboundx.rebx_get_tau_a(byref(self))
        @tau_a.setter
        def tau_a(self, value):
            clibreboundx.rebx_set_tau_a(byref(self), c_double(value))
        @property
        def tau_e(self):
            clibreboundx.rebx_get_tau_e.restype = c_double
            return clibreboundx.rebx_get_tau_e(byref(self))
        @tau_e.setter
        def tau_e(self, value):
            clibreboundx.rebx_set_tau_e(byref(self), c_double(value))
        @property
        def tau_inc(self):
            clibreboundx.rebx_get_tau_inc.restype = c_double
            return clibreboundx.rebx_get_tau_inc(byref(self))
        @tau_inc.setter
        def tau_inc(self, value):
            clibreboundx.rebx_set_tau_inc(byref(self), c_double(value))
        @property
        def tau_omega(self):
            clibreboundx.rebx_get_tau_omega.restype = c_double
            return clibreboundx.rebx_get_tau_omega(byref(self))
        @tau_omega.setter
        def tau_omega(self, value):
            clibreboundx.rebx_set_tau_omega(byref(self), c_double(value))
        @property
        def tau_Omega(self):
            clibreboundx.rebx_get_tau_Omega.restype = c_double
            return clibreboundx.rebx_get_tau_Omega(byref(self))
        @tau_Omega.setter
        def tau_Omega(self, value):
            clibreboundx.rebx_set_tau_Omega(byref(self), c_double(value))
        @property
        def Q_pr(self):
            clibreboundx.rebx_get_Q_pr.restype = c_double
            return clibreboundx.rebx_get_Q_pr(byref(self))
        @Q_pr.setter
        def Q_pr(self, value):
            clibreboundx.rebx_set_Q_pr(byref(self), c_double(value))

        rebound.Particle.tau_a = tau_a
        rebound.Particle.tau_e = tau_e
        rebound.Particle.tau_inc = tau_inc
        rebound.Particle.tau_omega = tau_omega
        rebound.Particle.tau_Omega = tau_Omega
        rebound.Particle.Q_pr = Q_pr

    def rad_calc_mass(self, density, radius):
        clibreboundx.rebx_rad_calc_mass.restype = c_double
        return clibreboundx.rebx_rad_calc_mass(c_double(density), c_double(radius))
    def rad_calc_beta(self, particle):
        clibreboundx.rebx_rad_calc_beta.restype = c_double
        return clibreboundx.rebx_rad_calc_beta(byref(self), byref(particle))
    def rad_calc_particle_radius(self, beta, density, Q_pr):
        clibreboundx.rebx_rad_calc_particle_radius.restype = c_double
        return clibreboundx.rebx_rad_calc_particle_radius(byref(self), c_double(beta), c_double(density), c_double(Q_pr))


# Need to put fields after class definition because of self-referencing
Extras._fields_ = [("sim", POINTER(rebound.Simulation)),
                ("params_to_be_freed", POINTER(rebx_param_to_be_freed)),
                ("forces", POINTER(CFUNCTYPE(None, POINTER(rebound.Simulation)))),
                ("ptm", POINTER(CFUNCTYPE(None, POINTER(rebound.Simulation)))),
                ("Nptm", c_int),
                ("Nforces", c_int),
                ("modify_orbits_forces", rebx_params_modify_orbits),
                ("modify_orbits_direct", rebx_params_modify_orbits),
                ("gr", rebx_params_gr),
                ("radiation_forces", rebx_params_radiation_forces)]



