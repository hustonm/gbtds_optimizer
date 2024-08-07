import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import argparse
import sys
import pickle
import matplotlib.cm as cm
from scipy.ndimage import zoom,gaussian_filter


from fields import fov,fovHandler,slewOptimizer
from yieldMap import yieldMap


parser = argparse.ArgumentParser(description="Optimizer for the Roman Galactic Bulge Time Domain Survey")

parser.add_argument('--input-root',default='test',
                    help='Filename root for output')
parser.add_argument('--contour-resolution',default=1,type=float,
                    help='Zoom factor for increasing contour resolution')
parser.add_argument('--smoothing',default=0,type=float,
                    help='Sigma for Gaussian smoothing prior to contouring')
parser.add_argument('--lrange',nargs=2,default=[5.0,-5.0],type=float,
                    help='Range of l in the grid')
parser.add_argument('--brange',nargs=2,default=[-5.0,5.0],type=float,
                    help='Range of b in the grid')
parser.add_argument('--plot-fields-off',action='store_true',
                    help='Turn off plotting best field locations?')
parser.add_argument('--save',default=False,
                    help='If provided with a file extension, saves the figure')
parser.add_argument('--no-show',action='store_true',
                    help='Show the figure in an interactive window')
parser.add_argument('--save-root',default='',type=str,
                    help='Filename root to save the figure with. figure goes to root_plot.<ext> where ext is set using the --save argument')
parser.add_argument('--plot-cadence',action='store_true',
                    help='Turn on plotting cadence contours instead of yield')
parser.add_argument('--plot-texp',action='store_true',
                    help='Turn on plotting texp contours instead of yield')



args = parser.parse_args()

#Open the pickle
with open(args.input_root + "_results.pkl",'rb') as pklhandle:
    lgrid,bgrid,nreadgrid,cadencegrid,yieldgrid,handler = pickle.load(pklhandle)


#Zoom if needed

lgrid_z = lgrid
bgrid_z = bgrid
ygrid_z = yieldgrid
cgrid_z = cadencegrid
ngrid_z = nreadgrid

if args.contour_resolution > 1:
    print("Increasing resolution")
    lgrid_z = zoom(lgrid,args.contour_resolution)
    bgrid_z = zoom(bgrid,args.contour_resolution)
    ygrid_z = zoom(yieldgrid,args.contour_resolution)
    cgrid_z = zoom(cadencegrid,args.contour_resolution)
    ngrid_z = zoom(nreadgrid,args.contour_resolution)
    
if args.smoothing > 0:
    print("Smoothing")
    lgrid_z = gaussian_filter(lgrid_z,args.smoothing)
    bgrid_z = gaussian_filter(bgrid_z,args.smoothing)
    ygrid_z = gaussian_filter(ygrid_z,args.smoothing)
    cgrid_z = gaussian_filter(cgrid_z,args.smoothing)
    ngrid_z = gaussian_filter(ngrid_z,args.smoothing)

fig, ax = plt.subplots()
ymap = handler.yieldMap.plotMap(ax=ax,pcolormesh_kwargs={'cmap':cm.gray})

if not args.plot_cadence and not args.plot_texp:
    contour_set = ax.contour(lgrid_z,bgrid_z,ygrid_z)
elif args.plot_cadence:
    contour_set = ax.contour(lgrid_z,bgrid_z,cgrid_z)
elif args.plot_texp:
    print(ngrid_z)
    contour_set = ax.contour(lgrid_z,bgrid_z,ngrid_z)
    
if not args.plot_fields_off:
    handler.plotFields(ax=ax,plot_kwargs={'color':'r','linestyle':'-','lw':0.5})

ax.set_xlabel('l (deg)')
ax.set_ylabel('b (deg)')

ax.set_xlim([args.lrange[0],args.lrange[1]])
ax.set_ylim([args.brange[0],args.brange[1]])

ax.set_aspect('equal')
ax.clabel(contour_set)

plt.colorbar(ymap,ax=ax,label='Yield per map tile')

if not args.no_show:
    plt.show()
if not args.save==False:
    save_root = args.save_root
    if save_root=='':
        save_root=args.input_root
    savename=save_root + '_plot.' + args.save
    print("Saving to",savename)
    plt.savefig(savename)