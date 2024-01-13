# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 15:50:05 2024

@author: user
"""

"""
The following functions (load_transcoefile_method,  comes from B2TransportParser code written by 
Richard Reksoatmodjo and Jameson Crouse
"""
import re
import numpy as np
import matplotlib.pyplot as plt

def load_transcoefile_method(file ='b2.transport.inputfile', plot=False):
    
    Coefficients = {'1':'Particle density-driven diffusivity',
                    '2': 'Particle pressure-driven diffusivity',
                    '3': 'Ion thermal anomalous diffusivity',
                    '4': 'Electron thermal anomalous diffusivity',
                    '5': 'Poloidal-component of the anomalous ”pinch” velocity',
                    '6': 'Radial-component of the anomalous ”pinch” velocity',
                    '7': 'Anomalous viscosity',
                    '8': 'Anomalous radial electrical conductivity',
                    '9': 'Anomalous radial thermo-electric coefficient'}    
    
    with open(file) as f:
        dataList=f.readlines()
    
    Points={}
    ii=1

    while ii<len(dataList)-2: 
        ndata = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", dataList[ii])
        CoeffID = ndata[1]
        PtNo = int(ndata[3])
        XList = []
        YList = []
        for mm in range(PtNo):
            XList.append(float(re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?",dataList[mm+ii+1])[4]))
            YList.append(float(re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?",dataList[mm+ii+1])[9]))
        Points[CoeffID] = np.array([XList,YList])
        ii=ii+ PtNo + 1
        
    if plot:
        dd=len(Points.keys())
        fig1,ax1=plt.subplots(nrows= dd,ncols=1,sharex=True)
        for ii, jj in enumerate(Points.keys()):
            ax1[ii].plot(Points[jj][0],Points[jj][1])
            ax1[ii].set_ylabel(r'{} $[m^2/s]$'.format(Coefficients[jj]))
        
        ax1[0].set_title(file)    
        ax1[-1].set_xlabel(r'$R-R_{sep}$')
        
    return Points

def Generate_transcoefile_method(trans_pts, CoeffID = 1, SpeciesID = 1, M=[1]):
    '''
    Function that is used to turn the radial points into a readable
    b2.transport.inputfile

    Parameters
    ----------
    trans_pts : nx2 array, x coordinates being r-r_sep and
    y coordinates the coefficient value at that point

    CoeffID : int, integer specifier of transport coefficient 
    type according to SOLPS manual (1 by default)
    
    SpeciesID : int, integer index of transport species (1 by default)
    
    M : float or list, factor to multiply all transport coefficient values by.
    If list, creates a separate multiplied string block for each listed factor

    Returns a formatted string block for use in the b2.transport.inputfile
    -------
    '''
    if type(M) is not list:
        M=[M]
        
    n = len(trans_pts)
    m = 0
    i = CoeffID
    j = SpeciesID
    r = trans_pts
    inputfile={}
    
    for MM in M:
        inputfile[MM] = ' ndata(1, {0}, {1})= {2},\n'.format(i,j,n)
        for m in range(n):
            inputfile[MM] = inputfile[MM] + ' tdata(1, {0}, {1}, {2})= {3}, tdata(2, {0}, {1}, {2})= {4},\n'.format(m+1,i,j,np.round(r[m][0],5),np.round(r[m][1]*MM,5))
            
    return inputfile

def Write_transcoefile_method(file='b2.transport.inputfile', points={},M_1 = True, M=[1]):
    inputfile={}
    if points:
        for k in points.keys():
            inputfile[k] = Generate_transcoefile_method(points[k].T,CoeffID=int(k),M=M)
    else:
        points = load_transcoefile_method(file)
        for k in points.keys():
            inputfile[k] = Generate_transcoefile_method(points[k].T,CoeffID=int(k),M=M)
    if M_1 == True:
        for MM in M:
            with open('{}'.format(file),'w') as f:
                f.write(' &TRANSPORT\n')
                for k in inputfile.keys():
                    f.writelines(inputfile[k][MM])
                f.write(' no_pflux=.false.\n /\n')
    else:
        for MM in M:
            with open('{}.f{}'.format(file,MM),'w') as f:
                f.write(' &TRANSPORT\n')
                for k in inputfile.keys():
                    f.writelines(inputfile[k][MM])
                f.write(' no_pflux=.false.\n /\n')