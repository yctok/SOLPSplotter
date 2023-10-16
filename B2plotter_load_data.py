# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 21:54:40 2023

@author: user
"""
from B2plotter_class import B2plotter
import opacity_plot_method as opm
import matplotlib.pyplot as plt
import load_mast_expdata_method as lmem
import load_coord_method as lcm
import fitting_method as fm 
from scipy import interpolate
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit
import numpy as np
import xarray as xr
import math


class load_expdata(B2plotter):
    
    def __init__(self, DEV, withshift, withseries, DefaultSettings, loadDS):
        B2plotter.__init__(self, DEV, withshift, withseries, DefaultSettings)
        # Employee.__init__(self, first, last, pay)
        self.loadDS = loadDS
        
    def loadmastdata(self, EXP, fit):
        if EXP:
            mastloc = '{}/{}/{}'.format(self.data['dirdata']['basedrt'], 
                                    self.DEV, self.loadDS['expfilename'])
            expdic = lmem.read_mastfile(mastloc)
            self.data['ExpDict'] = expdic
            self.data['dirdata']['mastloc'] = mastloc
        
        if fit:
            fitloc = '{}/{}/{}'.format(self.data['dirdata']['basedrt'], 
                                    self.DEV, self.loadDS['fitfname'])
            fitdic = lmem.read_fitfile(fitloc)
            self.data['fitprofile'] = fitdic
            self.data['dirdata']['fitloc'] = fitloc
            
    def fitmastexp(self):
        n_tot = 200
        # solps_psi = 1.09145489
        solps_psi = 1.1
        p0 = [0.97, 0.6, 0.01, 0.01, 3/14]
        p1 = [0.95, 0.2, 0.02, 0.01, 6/7]
        self.loadmastdata(EXP= True, fit= False)
        mast_dat_dict = self.data['ExpDict']
        psi = mast_dat_dict['psi_normal']
        ne = mast_dat_dict['electron_density(10^20/m^3)']
        ne_er = mast_dat_dict['density error(10^20/m^3)']
        te = mast_dat_dict['electron_temperature(KeV)']
        te_er = mast_dat_dict['temperature error(10^20/m^3)']
        
        popt_ne, pcov_ne = curve_fit(fm.tanh, psi, ne, p0)
        print(popt_ne)
        popt_te, pcov_te = curve_fit(fm.tanh, psi, te, p1)
        print(popt_te)
          
        x_model = np.linspace(min(psi), max(psi), n_tot)
        tanh_ne_fit = fm.tanh(x_model, popt_ne[0], popt_ne[1], popt_ne[2], popt_ne[3], popt_ne[4])
        tanh_te_fit = fm.tanh(x_model, popt_te[0], popt_te[1], popt_te[2], popt_te[3], popt_te[4])
        
        shift = 0.002
        psi_sh = psi + shift
        
        sh_opt_ne, sh_cov_ne = curve_fit(fm.tanh, psi_sh, ne, p0)
        print(sh_opt_ne)
        sh_opt_te, sh_cov_te = curve_fit(fm.tanh, psi_sh, te, p1)
        print(sh_opt_te)
        
        
        x_sh = np.linspace(min(psi_sh), max(psi_sh), n_tot)
        sh_ne_fit = fm.tanh(x_sh, sh_opt_ne[0], sh_opt_ne[1], sh_opt_ne[2], sh_opt_ne[3], sh_opt_ne[4])
        sh_te_fit = fm.tanh(x_sh, sh_opt_te[0], sh_opt_te[1], sh_opt_te[2], sh_opt_te[3], sh_opt_te[4])
        
        
        gnexp = np.gradient(tanh_ne_fit)
        
        "experimental data and tanh fit"
        "electron density"
        plt.figure(figsize=(7,7))
        plt.plot(x_model, tanh_ne_fit, color='r', label= 'electron density fit')
        plt.errorbar(psi, ne, ne_er,fmt="o", label= 'electron density experiment data')
        
        plt.xlabel('Magnetic flux coordinate: ${\psi_N}$')
        plt.ylabel('Electron density: ${n_e}$ (10$^{20}$*m$^{-3}$)')
        plt.title('Electron density')
        plt.legend()
        
        
        "electron temperature"
        
        plt.figure(figsize=(7,7))
        plt.plot(x_model, tanh_te_fit, color='r', label= 'electron temperature fit')
        plt.errorbar(psi, te, te_er, fmt= "o", label= 'electron temperature experiment data')
        
        plt.xlabel('Magnetic flux coordinate: ${\psi_N}$')
        plt.ylabel('Electron temperature: ${T_e}$ (KeV)')
        plt.title('Electron temperature')
        plt.legend()
        
        
        "fit profile and shift profile"
        "electron density"
        
        # plt.figure(figsize=(7,7))
        # plt.plot(x_sh, sh_ne_fit,'-o', color='r', label= 'electron density fit with shift')
        # plt.plot(x_model, tanh_ne_fit,'-o', color='b', label= 'electron density fit')
        
        # plt.xlabel('Magnetic flux coordinate: ${\psi_N}$')
        # plt.ylabel('Electron density: ${n_e}$ (10$^{20}$*m$^{-3}$)')
        # plt.title('Electron density')
        # plt.legend()
        
        "electron tempurature"
        
        # plt.figure(figsize=(7,7))
        # plt.plot(x_sh, sh_te_fit,'-o', color='r', label= 'electron temperature fit with shift')
        # plt.plot(x_model, tanh_te_fit,'-o', color='b', label= 'electron temperature fit')
        
        # plt.xlabel('Magnetic flux coordinate: ${\psi_N}$')
        # plt.ylabel('Electron temperature: ${T_e}$ (KeV)')
        # plt.title('Electron temperature')
        # plt.legend()
        
        
        plt.show()
        
        
        w_datalist = []
        filename = 'wsh_027205_275.dat'
        fdir = '{}/{}/{}'.format(self.data['dirdata']['basedrt'], 
                                self.DEV, self.loadDS['fitfname'])
        for j in range(n_tot):
            w_list =[]
            w_list.append("{: .6f}".format(x_sh[j]))
            w_list.append("{: .6f}".format(sh_ne_fit[j]))
            w_list.append("{: .6f}".format(sh_te_fit[j]))
            w_writelist = ' '.join(str(y)+ "\t" for y in w_list)
            w_datalist.append(w_writelist)
       
        with open(fdir, 'w') as f:
            for l,w_line in enumerate(w_datalist):   
                f.writelines(w_line + "\n")
        
            
            
class load_data(load_expdata):
    
    def __init__(self, DEV, withshift, withseries, DefaultSettings, loadDS, Parameters):
        load_expdata.__init__(self, DEV, withshift, withseries, DefaultSettings, loadDS)
        # Employee.__init__(self, first, last, pay)
        
        "Parameters"
        if isinstance(Parameters, dict):
            self.Parameters = Parameters
        else:
            print('parameter has to be a dictionary')
            
        if Parameters is None:
            print('There is no parameters input')
        else:
            self.Parameters = Parameters
            
        Plist = []
        for pkey, pvalue in self.Parameters.items():
            Plist.append(pkey)
        
        self.data['paramkey'] = Plist
        self.data['Parameter'] = Parameters
        
    "Add and remove elements from parameter or defaultsettings"
    def add_dic(self, new_set, assign='default'):
        if assign == 'param':
            self.Parameters = new_set | self.Parameters
            Plist = []
            for pkey, pvalue in self.Parameters.items():
                Plist.append(pkey)
        
        # elif assign == 'default':
        #     self.DefaultSettings = new_set | self.DefaultSettings
        #     keylist = []
        #     for key, value in self.DefaultSettings.items():
        #         keylist.append(key)
        else:
            print('assign parameter is incorrect')
            
        
    def remove_dic(self, new_set, assign='param'):
        if assign == 'param':
            if new_set.keys() in self.data['defaultkey']:
                del self.Parameters[new_set.keys()]
            Plist = []
            for pkey, pvalue in self.Parameters.items():
                Plist.append(pkey)
                
        # elif assign == 'default':
        #     if new_set.keys() in self.data['defaultkey']:
        #         del self.DefaultSettings[new_set.keys()]
        #     keylist = []
        #     for key, value in self.DefaultSettings.items():
        #         keylist.append(key)
        else:
            print('assign parameter incorrect')

    
    def load_output_data(self, param):
        if self.withshift == False and self.withseries == False:
            BASEDRT = self.data['dirdata']['outputdir']['Output']
            Attempt = self.data['dircomp']['Attempt']
            # Attempts = len([self.data['dircomp']['a_shift']])
            # N = len(self.data['dircomp']['a_shift'])
            XGrid = int(self.data['b2fgeo']['nx'])
            # X = self.data['gridsettings']['X']
            XMin= 1
            XMax= XGrid
            # print(XGrid)
            XDIM = int(self.data['DefaultSettings']['XDIM'])
            # YSurf = int(self.data['b2fgeo']['ny'])
            # Y = self.data['gridsettings']['Y']
            YDIM = int(self.data['DefaultSettings']['YDIM'])
            n = 0
            
            
            # DRT = '{}/Attempt{}'.format(BASEDRT, str(Attempt))   #Generate path
            test = param in self.Parameters.keys()
            self.data['outputdata'][param] = np.zeros([YDIM, XDIM], dtype= np.float32)
            # self.data['outputdata'][param] = xr.DataArray(np.zeros((YSurf,XGrid,N)), 
            #                                  coords=[Y,X,Attempts], 
            # dims=['Radial_Location','Poloidal_Location','Attempt'], name = param)
            if test:
                print('yes, {} is in parameter'.format(param))
                RawData = np.loadtxt('{}/{}{}'.format(BASEDRT, param, str(Attempt)),usecols = (3))
            elif test == False:
                print('no, {} is not in parameter'.format(param))
            else:
                print('there might be a bug')
            
            if len(RawData) > 0:        
                if RawData.size == XDIM*YDIM:
                    # self.data['outputdata'][param].values[:,:,n] = RawData.reshape((YDIM,XDIM))[1:YDIM-1,XMin:XMax+1]
                    self.data['outputdata'][param] = RawData.reshape((YDIM,XDIM))
                elif RawData.size != XDIM*YDIM:
                    print('rawdata size is not equal to {}'.format(str(XDIM*YDIM)))
                # elif RawData.size == XDIM*YDIM*2:
                #     self.data['outputdata'][param].values[:,:,n] = RawData.reshape((2*YDIM,XDIM))[1+YDIM:2*YDIM-1,XMin:XMax+1]
            else:
                print('we have a problem loading rawdata')
        
        
        elif self.withshift == True and self.withseries == False:
            param_data_dic = {}
            for aa in self.data['dircomp']['multi_shift']:
                BASEDRT = self.data['dirdata']['infolderdir'][aa]['outputdir']['Output']
                Attempt = self.data['dircomp']['Attempt'][aa]
                XGrid = int(self.data['b2fgeo'][aa]['nx'])
                # print(XGrid)
                XDIM = int(self.data['DefaultSettings']['XDIM'][aa])
                YDIM = int(self.data['DefaultSettings']['YDIM'][aa])
            
            
                # DRT = '{}/Attempt{}'.format(BASEDRT, str(Attempt))   #Generate path
                test = param in self.Parameters.keys()
                param_data_dic[aa] = np.zeros([YDIM, XDIM], dtype= np.float32)
                # self.data['outputdata'][param] = xr.DataArray(np.zeros((YSurf,XGrid,N)), 
                #                                  coords=[Y,X,Attempts], 
                # dims=['Radial_Location','Poloidal_Location','Attempt'], name = param)
                if test:
                    # print('yes, {} is in parameter'.format(param))
                    RawData = np.loadtxt('{}/{}{}'.format(BASEDRT, param, str(Attempt)),usecols = (3))
                elif test == False:
                    print('no, {} is not in parameter'.format(param))
                else:
                    print('there might be a bug')
                
                if len(RawData) > 0:        
                    if RawData.size == XDIM*YDIM:
                        # self.data['outputdata'][param].values[:,:,n] = RawData.reshape((YDIM,XDIM))[1:YDIM-1,XMin:XMax+1]
                        param_data_dic[aa] = RawData.reshape((YDIM,XDIM))
                    elif RawData.size != XDIM*YDIM:
                        print('rawdata size is not equal to {}'.format(str(XDIM*YDIM)))
                    # elif RawData.size == XDIM*YDIM*2:
                    #     self.data['outputdata'][param].values[:,:,n] = RawData.reshape((2*YDIM,XDIM))[1+YDIM:2*YDIM-1,XMin:XMax+1]
                else:
                    print('we have a problem loading rawdata')
        
            self.data['outputdata'][param] = param_data_dic
            
            
        elif self.withshift == False and self.withseries == True:
            param_data_dic = {}
            for aa in self.data['dircomp']['Attempt'].keys():
                BASEDRT = self.data['dirdata']['outputdir'][aa]['Output']
                Attempt = self.data['dircomp']['Attempt'][aa]
                XGrid = int(self.data['b2fgeo']['nx'])
                # print(XGrid)
                XDIM = int(self.data['DefaultSettings']['XDIM'])
                YDIM = int(self.data['DefaultSettings']['YDIM'])
            
            
                # DRT = '{}/Attempt{}'.format(BASEDRT, str(Attempt))   #Generate path
                test = param in self.Parameters.keys()
                param_data_dic[aa] = np.zeros([YDIM, XDIM], dtype= np.float32)
                # self.data['outputdata'][param] = xr.DataArray(np.zeros((YSurf,XGrid,N)), 
                #                                  coords=[Y,X,Attempts], 
                # dims=['Radial_Location','Poloidal_Location','Attempt'], name = param)
                if test:
                    # print('yes, {} is in parameter'.format(param))
                    RawData = np.loadtxt('{}/{}{}'.format(BASEDRT, param, str(Attempt)),usecols = (3))
                elif test == False:
                    print('no, {} is not in parameter'.format(param))
                else:
                    print('there might be a bug')
                
                if len(RawData) > 0:        
                    if RawData.size == XDIM*YDIM:
                        # self.data['outputdata'][param].values[:,:,n] = RawData.reshape((YDIM,XDIM))[1:YDIM-1,XMin:XMax+1]
                        param_data_dic[aa] = RawData.reshape((YDIM,XDIM))
                    elif RawData.size != XDIM*YDIM:
                        print('rawdata size is not equal to {}'.format(str(XDIM*YDIM)))
                    # elif RawData.size == XDIM*YDIM*2:
                    #     self.data['outputdata'][param].values[:,:,n] = RawData.reshape((2*YDIM,XDIM))[1+YDIM:2*YDIM-1,XMin:XMax+1]
                else:
                    print('we have a problem loading rawdata')
        
            self.data['outputdata'][param] = param_data_dic
        
        elif self.withshift == True and self.withseries == True:
            print('load_output_data is not there yet, to be continue...')
        
        else:
            print('There is a bug')