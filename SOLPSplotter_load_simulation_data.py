# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 14:11:08 2024

@author: ychuang
"""


from SOLPSplotter_load_expdata import load_expdata
import load_B2_data_method as lbdm
import numpy as np



class load_simu_data(load_expdata):
    
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

    
    def load_output_data_method(self, param, itername):
        if self.withshift == False and self.withseries == False:
            BASEDRT = self.data['dirdata']['outputdir']['Output']
            Attempt = self.data['dircomp']['Attempt']
            XGrid = int(self.data['b2fgeo']['nx'])
            # X = self.data['gridsettings']['X']
            # YSurf = int(self.data['b2fgeo']['ny'])
            # Y = self.data['gridsettings']['Y']
            XMin= 1
            XMax= XGrid
            # print(XGrid)
            XDIM = int(self.data['DefaultSettings']['XDIM'])
            YDIM = int(self.data['DefaultSettings']['YDIM'])
        elif self.withshift == True and self.withseries == False:
            BASEDRT = self.data['dirdata']['infolderdir'][itername]['outputdir']['Output']
            Attempt = self.data['dircomp']['Attempt'][itername]
            XGrid = int(self.data['b2fgeo'][itername]['nx'])
            # print(XGrid)
            XDIM = int(self.data['DefaultSettings']['XDIM'][itername])
            YDIM = int(self.data['DefaultSettings']['YDIM'][itername])
            
        elif self.withshift == False and self.withseries == True:
            BASEDRT = self.data['dirdata']['outputdir'][itername]['Output']
            Attempt = self.data['dircomp']['Attempt'][itername]
            XGrid = int(self.data['b2fgeo']['nx'])
            # print(XGrid)
            XDIM = int(self.data['DefaultSettings']['XDIM'])
            YDIM = int(self.data['DefaultSettings']['YDIM'])
        
        # DRT = '{}/Attempt{}'.format(BASEDRT, str(Attempt))   #Generate path
        # self.data['outputdata'][param] = xr.DataArray(np.zeros((YSurf,XGrid,N)), 
        #                                  coords=[Y,X,Attempts], 
        # dims=['Radial_Location','Poloidal_Location','Attempt'], name = param)
        
        n = 0
        output_data = np.zeros([YDIM, XDIM], dtype= np.float32)
        test = param in self.Parameters.keys()       
        if test:
            # print('yes, {} is in parameter'.format(param))
            RawData = np.loadtxt('{}/{}{}'.format(BASEDRT, param, str(Attempt)),usecols = (3))
            # temp_dic = {param: RawData}
            # self.data['temp'] = temp_dic
        elif test == False:
            print('no, {} is not in parameter'.format(param))
        else:
            print('there might be a bug')
            
            
        if len(RawData) > 0:        
            if RawData.size == XDIM*YDIM:
                # self.data['outputdata'][param].values[:,:,n] = RawData.reshape((YDIM,XDIM))[1:YDIM-1,XMin:XMax+1]
                output_data = RawData.reshape((YDIM,XDIM))
            elif RawData.size == XDIM*YDIM*2:
                raw_split = np.array_split(RawData, 2)
                param_dic = {'D_0': raw_split[0].reshape((YDIM,XDIM)), 
                             'D_1': raw_split[1].reshape((YDIM,XDIM))}
                output_data = param_dic
                # print('let work on it')
                
                
            elif RawData.size != XDIM*YDIM:
                print('rawdata size is not equal to {}, it is {}'.format(str(XDIM*YDIM), str(RawData.size)))
            # elif RawData.size == XDIM*YDIM*2:
            #     self.data['outputdata'][param].values[:,:,n] = RawData.reshape((2*YDIM,XDIM))[1+YDIM:2*YDIM-1,XMin:XMax+1]
        else:
            print('we have a problem loading rawdata')
        
        return output_data
    
       
    def load_output_data(self, param):
        if self.withshift == False and self.withseries == False:
            output = self.load_output_data_method(param = param, itername = None)
            self.data['outputdata'][param] = output
            
            
        elif self.withshift == True and self.withseries == False:
            param_data_dic = {}
            for aa in self.data['dircomp']['multi_shift']:
                param_data_dic[aa] = self.load_output_data_method(param = param, itername = aa)
                      
            self.data['outputdata'][param] = param_data_dic
            
            
        elif self.withshift == False and self.withseries == True:
            param_data_dic = {}
            for aa in self.data['dircomp']['Attempt'].keys():
                param_data_dic[aa] = self.load_output_data_method(param = param, itername = aa)
        
            self.data['outputdata'][param] = param_data_dic
        
        elif self.withshift == True and self.withseries == True:
            print('load_output_data is not there yet, to be continue...')
        
        else:
            print('There is a bug')
    
    
    def load_b2fstate(self):
        if self.withshift == False and self.withseries == False:
            file_loc = '{}/{}'.format(self.data['dirdata']['simudir'], 'b2fstate')
            state, dim = lbdm.read_b2fstate(b2fstateLoc = file_loc)
            state_dic = vars(state)
            dim_dic = {'nx': dim[0], 'ny': dim[1], 'ns': dim[2]}
            self.data['b2fstate'] = state_dic
            self.data['DefaultSettings']['dims'] = dim_dic
            # self.b2fstate = state
        
        elif self.withshift == True and self.withseries == False:
            state_dic = {}
            dim_dic = {}
            
            for aa in self.data['dircomp']['multi_shift']:
                file_loc = '{}/{}'.format(self.data['dirdata']['simudir'][aa], 'b2fstate')
                state, dim = lbdm.read_b2fstate(b2fstateLoc = file_loc)
                state_dic[aa] = vars(state)
                dim_dic[aa] = {'nx': dim[0], 'ny': dim[1], 'ns': dim[2]}

            self.data['b2fstate'] = state_dic
            self.data['DefaultSettings']['dims'] = dim_dic
            # self.b2fstate = state
        
        else:
            print('load_b2fstate function is not there yet!')
    
    
    
    
    def load_b2fplasmf(self):
        if self.withshift == False and self.withseries == False:
            file_loc = '{}/{}'.format(self.data['dirdata']['simudir'], 'b2fplasmf')
            dim_dic = self.data['DefaultSettings']['dims']
            n_pol = dim_dic['nx']
            n_rad = dim_dic['ny']
            n_sp = dim_dic['ns']
            fplasma = lbdm.read_b2fplasmf(fileName = file_loc, nx = n_pol, 
                                          ny = n_rad, ns = n_sp)
            fplasma_dic = vars(fplasma)
            self.data['b2fplasmf'] = fplasma_dic
            # print('the next line is b2fplasmf')
            # print(type(k))
        
        elif self.withshift == True and self.withseries == False:
            fplasma_dic = {}
            
            for aa in self.data['dircomp']['multi_shift']:
                file_loc = '{}/{}'.format(self.data['dirdata']['simudir'][aa], 'b2fplasmf')
                dim_dic = self.data['DefaultSettings']['dims']
                n_pol = dim_dic[aa]['nx']
                n_rad = dim_dic[aa]['ny']
                n_sp = dim_dic[aa]['ns']
                fplasma = lbdm.read_b2fplasmf(fileName = file_loc, nx = n_pol, 
                                              ny = n_rad, ns = n_sp)
                fplasma_dic[aa] = vars(fplasma)
                
                
            self.data['b2fplasmf'] = fplasma_dic
            
        
        
        else:
            print('load_b2fplasmf function is not there yet!')
    
    
    """
    
    This is the first version of filter, we can later isolate a 
    general function from it so that can be used for b2fstate
    
    """
    
    
    
    
    def b2fplasmf_filter_method(self, datafile, dim_setting):
        nxny_list = []
        zero_nxny_list = []
               
        nxnyns_list = []
        zero_nxnyns_list = []
        
        nxny_corner_list = []
        zero_nxnycorner_list = []
        
        fluxdim_ns_list = []
        zero_fluxdimns_list = []
        
        nxny_corner_ns_list = []
        zero_nxnycornerns_list = []
        
        rest_list = []
        
        nx = dim_setting['nx']
        ny = dim_setting['ny']
        ns = dim_setting['ns']
        nc = 4
               
        # b2plasmf = datafile
        for plasmf_k in list(datafile.keys()):
            if np.shape(datafile[plasmf_k]) == (nx+2, ny+2):
                if np.all(datafile[plasmf_k] == 0):
                    zero_nxny_list.append(plasmf_k)
                
                else:
                    nxny_list.append(plasmf_k)
            
            elif np.shape(datafile[plasmf_k]) == (nx+2, ny+2, ns):
                for ns_a in range(ns):
                    if np.all(datafile[plasmf_k][:, :, ns_a] == 0):
                        zero_nxnyns_list.append('{}_{}'.format(plasmf_k, ns_a))
                    
                    else:
                        nxnyns_list.append('{}_{}'.format(plasmf_k, ns_a))
                    
                
            
            elif np.shape(datafile[plasmf_k]) == (nx+2, ny+2, nc):
                
                for nc_a in range(4):
                    if np.all(datafile[plasmf_k][:, :, nc_a] == 0):
                        zero_nxnycorner_list.append('{}_{}'.format(plasmf_k, nc_a))
                    
                    else:
                        nxny_corner_list.append('{}_{}'.format(plasmf_k, nc_a))
            
            
            
            elif np.shape(datafile[plasmf_k]) == (nx+2, ny+2, 2, 2):
                
                for ns_b in range(ns):
                    for nf_a in range(2):
                        if np.all(datafile[plasmf_k][:, :, nf_a, ns_b] == 0):
                            zero_fluxdimns_list.append('{}_{}_ns{}'.format(plasmf_k, 
                                                                    nf_a, ns_b))
                        
                        else:
                            fluxdim_ns_list.append('{}_{}_ns{}'.format(plasmf_k, 
                                                                    nf_a, ns_b))
                          
            elif np.shape(datafile[plasmf_k]) == (nx+2, ny+2, nc, ns):
                for ns_c in range(ns):
                    for nc_b in range(nc):
                        if np.all(datafile[plasmf_k][:, :, nc_b, ns_c] == 0):
                            zero_nxnycornerns_list.append('{}_nc{}_ns{}'.format(plasmf_k, 
                                                                    nc_b, ns_c))
                        
                        else:
                            nxny_corner_ns_list.append('{}_nc{}_ns{}'.format(plasmf_k, 
                                                                    nc_b, ns_c))
                           
            
            else:
                rest_list.append(plasmf_k)
                
                    
        
        key_order_dic = {'nxny': nxny_list, 'zero_nxny': zero_nxny_list, 
                         'nxnyns': nxnyns_list, 'zero_nxnyns': zero_nxnyns_list,
                         'nxnycorner': nxny_corner_list, 'zero_nxnycorner': zero_nxnycorner_list,
                         'fluxdim_ns': fluxdim_ns_list, 'zero_fluxdimns': zero_fluxdimns_list, 
                         'nxny_corner_ns': nxny_corner_ns_list, 
                         'zero_nxnycornerns': zero_nxnycornerns_list, 'the_rest': rest_list}
        
        
        return key_order_dic
    
                    
    
    
                    
    def b2fplasmf_filter(self):
        if self.withshift == False and self.withseries == False:
            print('single case: b2fplasmf_filter function is not there yet!')
            
        if self.withshift == True and self.withseries == False:
            key_order_dic = {}
            
            for aa in self.data['dircomp']['multi_shift']:
                                
                b2plasmf = self.data['b2fplasmf'][aa]
                dim = self.data['DefaultSettings']['dims'][aa]
                key_order_dic[aa] = self.b2fplasmf_filter_method(datafile = b2plasmf, 
                                                                 dim_setting = dim)
                
                
            self.data['b2fplasmf_key'] = key_order_dic
                
                
            

                    
                
                
            
        
    
    
    