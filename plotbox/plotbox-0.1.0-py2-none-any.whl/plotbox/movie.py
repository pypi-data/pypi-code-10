# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as path
import matplotlib.animation as animation

from tempfile import NamedTemporaryFile
from IPython.display import HTML

def to_html(anim, fps = 15):
    '''
    Given a matplotlib FuncAnimation object, returns a movie clip of the animation embedded in HTML. To be used when running iPython Notebook with pylab inline.

    Parameters
    ----------
    anim : matplotlib FuncAnimation object
            animation object storing all frames of the movie

    Returns
    -------
    html : HTML object
            returns animation as a movie clip embedded in HTML

    '''
    
    plt.close(anim._fig)
    VIDEO_TAG = """<video controls> <source src="data:video/x-m4v;base64,{0}" type="video/mp4"> 
    Your browser does not support the video tag. </video>"""
    
    if not hasattr(anim, '_encoded_video'):
        with NamedTemporaryFile(suffix = '.mp4') as f:
            anim.save(f.name, fps = fps, extra_args = ['-vcodec', 'libx264'])
            video = open(f.name, "rb").read()
        anim._encoded_video = video.encode("base64")
    
    return HTML(VIDEO_TAG.format(anim._encoded_video))

