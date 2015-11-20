import numpy as np

from ..particle_src.particle import Particles
from ..grid_src.grid import grid
from .LoadSnap import load_snap
from .analysis import Analysis


class Profile:

    def __init__(self,particles=None, type=None, center=False, mq=98,  Ngrid=512, xmin=None, xmax=None, kind='log',**kwargs):

        #Check input
        if 'filename' in kwargs: p=load_snap(kwargs['filename'])
        elif isinstance(particles,Particles): p=particles
        else: raise IOError('Incorrect particles or filename')

        #center
        if center==True:
            a=Analysis(p,safe=False)
            a.center(mq=mq, single=True)
        else:
            p.setrad()
            p.setvelt()

        #extract arrays
        if type is None:
            self.pos=p.Pos[:]
            self.vel=p.Vel[:]
            self.rad=p.Radius[:]
            self.vel_tot=p.Vel_tot[:]
            self.mass=p.Mass[:]

        elif isinstance(type,int):
            if p.header['Nall'][type]!=0: idx_type=p.Type==type
            else:   raise ValueError('Type %i not present in particles'%type)

            self.pos=p.Pos[idx_type]
            self.vel=p.Vel[idx_type]
            self.rad=p.Radius[idx_type]
            self.vel_tot=p.Vel_tot[idx_type]
            self.mass=p.Mass[idx_type]

        else: raise ValueError('type need to be None or an integer')

        #define grid
        self.Ngrid=Ngrid
        if xmin is None: self.xmin=np.min(self.rad)
        else: self.xmin=xmin
        if xmax is None: self.xmax=np.max(self.rad)
        else: self.xmax=xmax
        self.kind=kind
        self.grid=grid(N=self.Ngrid, type=self.kind, min=self.xmin, max=self.xmax )
        self.grid.setvol()
        self.grid.setsup()

        self.massbin=np.histogram(self.rad,bins=self.grid.gedge,weights=self.mass)[0]
        self.masscum=self.massbin.cumsum()
        self.dens=self.massbin/self.grid.g_vol


'''
R,mass_t,dens_t,pot_t=np.loadtxt('stellarcomp.txt',unpack=True,comments='#')
mms=GeneralModel(R,dens_t,rc=0.6,G='(kpc km2)/(M_sun s2)',Mmax=1e7)
mmdm=GeneralModel(R,dens_t,rc=5,G='(kpc km2)/(M_sun s2)',Mmax=1e8)



s={'type':2,'model':mms, 'npart':int(1e5)}
dm={'type':1, 'model':mmdm,'npart':int(5e6)}
N=int(1e6)

a=NbodyModel([dm])

p=a.generate()
a=Analysis(p, safe=False, auto_centre=False)

prof=Profile(p,Ngrid=512,xmin=0.01,xmax=200,kind='log',type=1)
dspline_prof=UnivariateSpline(prof.grid.gx,prof.dens,k=1,s=0)
dspline_true=UnivariateSpline(R,dens_t,k=1,s=0)
plt.plot(prof.grid.gx,dspline_prof(prof.grid.gx)/dspline_prof(5))
plt.plot(R*5,dspline_true(R)/dspline_true(1))
plt.xlim(0,10)
plt.ylim(-5,5)
plt.show()
'''

'''
prof=Profile(p,Ngrid=512,xmin=0.2,xmax=20,kind='lin',type=1)
plt.plot(prof.grid.gx,np.log10(prof.dens))
prof=Profile(p,Ngrid=512,xmin=0.2,xmax=20,kind='lin',type=2)
plt.plot(prof.grid.gx,np.log10(prof.dens))
prof=Profile(p,Ngrid=512,xmin=0.2,xmax=20,kind='lin')
plt.plot(prof.grid.gx,np.log10(prof.dens))
plt.show()

prof=Profile(p,Ngrid=512,xmin=0.2,xmax=20,kind='lin',type=1)
plt.plot(prof.grid.gx,prof.masscum/(1e8+1e7))
prof=Profile(p,Ngrid=512,xmin=0.2,xmax=20,kind='lin',type=2)
plt.plot(prof.grid.gx,prof.masscum/(1e8+1e7))
prof=Profile(p,Ngrid=512,xmin=0.2,xmax=20,kind='lin')
plt.plot(prof.grid.gx,prof.masscum/(1e8+1e7))
plt.show()
'''