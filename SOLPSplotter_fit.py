# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 23:11:05 2024

@author: ychuang
"""

from SOLPSplotter_PRmap import RP_mapping
import fitting_method as fm 
import numpy as np


class profile_fit(RP_mapping):
    
    def __init__(self, DefaultSettings, loadDS):
        RP_mapping.__init__(self, DefaultSettings, loadDS)
    
    
    def opacity_study_unit(self):
        unit = {'efold_length_psiN': 'Neutral penetration length ($\psi_N$)',
                'pedestal_width_psiN': 'Pedestal width ($\psi_N$)',
                  'dimensionless_opaqueness': 'Modeled opaqueness', 
                  'neutral_density': 'Neutral density ${n_D}$ (m$^{-3}$)', 
                  'electron_pedestal_density': 'Electron pedestal density: $n_{ped}$ (m$^{-3}$)',
                  'temperature_pedestal_width': 'Temperature pedestal width: $\Delta T$',
                  'flux_expansion': 'Flux expansion',
                  'efold_length': '$\lambda_{n_D}$ [mm]',
                  'pedestal_width': '$\Delta n_e$ [mm]',
                  
                  }
        return unit
    
    
    
    def opacity_data_fit_method(self, psiN, b2fstate, Neuden, check_ne,
                psi_dsa_ratio, pol_list, itername, data_struc): 
        # i = 0
        ln = len(pol_list)
        efold = np.zeros(ln)
        efold_l = np.zeros(ln)
        delta = np.zeros(ln)
        delta_l = np.zeros(ln)
        opq = np.zeros(ln)
        neu_den = np.zeros(ln)
        ne_ped = np.zeros(ln)
        ne_sep = np.zeros(ln)
        te_ped = np.zeros(ln)
        te_sep = np.zeros(ln)
        tdelta = np.zeros(ln)
        fluxexp = np.zeros(ln)
        
        nx = data_struc['nx']
        ny = data_struc['ny']
        
        if data_struc['size'] == 'full':
            Ne_data = b2fstate['ne'].transpose()
            Te_J = b2fstate['te'].transpose()
        elif data_struc['size'] == 'small':
            Ne_data = b2fstate['ne'][1:nx+1, 1:ny+1].transpose()
            Te_J = b2fstate['te'][1:nx+1, 1:ny+1].transpose()
            # print(Ne_data.shape)
            # print(Te_J.shape)
            
        # print(Neuden.shape)
        
        ev = 1.6021766339999999 * pow(10, -19)
        Te_data = Te_J / ev
        
        
        for k in pol_list:
            
            pol_in = int(k)
            i = pol_list.index(k)
            
            if data_struc['size'] == 'full':
                psi = psiN[:, pol_in]
            
            elif data_struc['size'] == 'small':
                psi = psiN[1:ny+1, pol_in]
                
                
            Nd = Neuden[:, pol_in]
            Ne = Ne_data[:, pol_in]
            Te = Te_data[:, pol_in]
            

            rd = fm.Opacity_calculator(x_coord= psi, ne = Ne, te = Te, 
                                   neuden = Nd, check_ne = check_ne, minor_rad = self.a)
            
            ped_index = rd['sep_index']
            
            
            fit_dic = {'tanh_ne_fit': rd['tanh_ne_fit'], 'tanh_te_fit': rd['tanh_te_fit'],
                       'exp_fit': rd['exp_fit']}
            
            flux_expand = self.calc_flux_expansion(pol_loc = k, ped_index = ped_index, 
                                                   iter_index = itername)

            
            efold[i] = rd['efold_length']
            delta[i] = rd['pedestal_width']
            opq[i] = rd['dimensionless_opaqueness']
            neu_den[i] = rd['n_sep_fit']
            ne_ped[i] = rd['electron_pedestal_density']
            ne_sep[i] = rd['electron_density_separatrix']
            te_ped[i] = rd['electron_pedestal_temperature']
            te_sep[i] = rd['electron_temperature_separatrix']
            tdelta[i] = rd['temperature_pedestal_width']
            fluxexp[i] = flux_expand
            efold_l[i] = rd['efold_length']*psi_dsa_ratio*flux_expand
            delta_l[i] = rd['pedestal_width']*psi_dsa_ratio*flux_expand
            
            
            # pol_loc[i] = int(k)
            # i = i + 1
        
        result = {'efold_length_psiN': efold, 'pedestal_width_psiN': delta,
                  'dimensionless_opaqueness': opq, 
                  'neutral_density': neu_den, 
                  'electron_pedestal_density': ne_ped,
                  'electron_density_separatrix': ne_sep,
                  'electron_pedestal_temperature': te_ped,
                  'electron_temperature_separatrix': te_sep,
                  'temperature_pedestal_width': tdelta,
                  'flux_expansion': fluxexp,
                  'efold_length': efold_l, 'pedestal_width': delta_l,                            
                  }
        
        self.data['poloidal_itemname'] = list(result.keys())
        
        return result
    
    
    
    def opacity_data_fit(self, pol_list, dat_size, check_ne):
        
        # self.load_ft44()
        
        
        if self.withshift == False and self.withseries == False:
            
            
            
            for p in pol_list:
                self.calc_dsa(pol_loc= p)

            
            nx = self.data['b2fgeo']['nx']
            ny = self.data['b2fgeo']['ny']
            
            if dat_size == 'full':
                
                self.load_output_data(param= 'NeuDen')
                Neuden_data = self.data['outputdata']['NeuDen']
                dat_struc = {'size': dat_size, 'nx': nx, 'ny': ny}
            
            elif dat_size == 'small':
                
                data = self.data['ft44']['dab2']
                Neuden_data = np.transpose(data[:, :, 0])
                dat_struc = {'size': dat_size, 'nx': nx, 'ny': ny}
                
            psiN_map = self.data['psi']['psival']
            fstate = self.data['b2fstate']         
            pd = self.data['DefaultSettings']['psi_dsa']
            
            fitresult = self.opacity_data_fit_method(b2fstate = fstate, Neuden = Neuden_data, 
                       psiN = psiN_map, psi_dsa_ratio = pd, pol_list = pol_list, 
                      itername = None, data_struc = dat_struc, check_ne = check_ne)
            
            self.data['opacity_poloidal'] = fitresult
            self.data['poloidal_itemname'] = list(fitresult.keys())
        
        elif self.withshift == True and self.withseries == False:
            
            self.load_output_data(param= 'NeuDen')
            fitresult_dic = {}
            
            for p in pol_list:
                self.calc_dsa(pol_loc= p)
            
            for aa in self.data['dircomp']['multi_shift']:
                
                
                nx = self.data['b2fgeo'][aa]['nx']
                ny = self.data['b2fgeo'][aa]['ny']
                
                
                
                if dat_size == 'full':
                    self.load_output_data(param= 'NeuDen')
                    Neuden_data = self.data['outputdata']['NeuDen'][aa]
                    dat_struc = {'size': dat_size, 'nx': nx, 'ny': ny}
                
                elif dat_size == 'small':
                    data = self.data['ft44'][aa]['dab2']
                    Neuden_data = np.transpose(data[:, :, 0])
                    dat_struc = {'size': dat_size, 'nx': nx, 'ny': ny}
                
                
                fstate = self.data['b2fstate'][aa]
                psiN_map = self.data['psi']['psival'][aa]
                pd = self.data['DefaultSettings']['psi_dsa'][aa]
                
                fitresult = self.opacity_data_fit_method(b2fstate = fstate, Neuden = Neuden_data,
                        psiN = psiN_map, psi_dsa_ratio = pd, pol_list = pol_list,
                       itername = aa, data_struc = dat_struc, check_ne = check_ne)
                
                fitresult_dic[aa] = fitresult
            
            self.data['opacity_poloidal'] = fitresult_dic
            self.data['poloidal_itemname'] = list(fitresult_dic['org'].keys())
        
        elif self.withshift == False and self.withseries == True:
            
            fitresult_dic = {}
            
            for p in pol_list:
                self.calc_dsa(pol_loc= p)
            
            for aa in list(self.data['dircomp']['Attempt'].keys()):
                
                if self.series_flag == 'twin_scan':
                    
                    nf = aa[0]
                    tf = aa[1]
                    
                    nx = self.data['b2fgeo']['nx']
                    ny = self.data['b2fgeo']['ny']
                    
                    if dat_size == 'full':
                        self.load_output_data(param= 'NeuDen')
                        Neuden_data = self.data['outputdata']['NeuDen'][nf][tf]
                        dat_struc = {'size': dat_size, 'nx': nx, 'ny': ny}
                    
                    elif dat_size == 'small':
                        data = self.data['ft44'][nf][tf]['dab2']
                        Neuden_data = np.transpose(data[:, :, 0])
                        dat_struc = {'size': dat_size, 'nx': nx, 'ny': ny}
                        
                    fstate = self.data['b2fstate'][nf][tf]
                
                else:
                    self.load_output_data(param= 'NeuDen')
                    Neuden_data = self.data['outputdata']['NeuDen'][aa]
                    # data = self.data['ft44'][aa]['dab2']
                    # Neuden_data = np.transpose(data[:, :, 0])
                    fstate = self.data['b2fstate'][aa]
                    
                
                psiN_map = self.data['psi']['psival']
                pd = self.data['DefaultSettings']['psi_dsa']
                
                fitresult = self.opacity_data_fit_method(b2fstate = fstate, Neuden = Neuden_data,
                        psiN = psiN_map, psi_dsa_ratio = pd, pol_list = pol_list,
                        itername = None, data_struc = dat_struc, check_ne = check_ne)
                
                fitresult_dic[aa] = fitresult
            
            self.data['opacity_poloidal'] = fitresult_dic
            self.data['poloidal_itemname'] = list(fitresult.keys())
        
        elif self.withshift == True and self.withseries == True:
            print('opacity_data_fit is not there yet!')
        
        
        else:
            print('opacity_data_fit has a bug')
    
    
    def neuden_percent(self):
        
        neu_percent = {}
        
        
        for aa in self.data['dircomp']['multi_shift']:
            if aa == 'org':
                pass
            else:
                neuden = self.data['opacity_poloidal'][aa]['neutral_density']
                neuden_std = self.data['opacity_poloidal']['org']['neutral_density']
                percentage = np.divide((neuden - neuden_std), neuden_std)*100
                neu_percent[aa] = percentage
        
        self.data['neuden_change'] = neu_percent
        
                
    def radial_data_fit_method(self, b2fstate, Neuden, psiN, pol_loc, data_struc, check_ne):
        

        
        nx = data_struc['nx']
        ny = data_struc['ny']
        
        if data_struc['size'] == 'full':
            Ne_data = b2fstate['ne'].transpose()
            Te_J = b2fstate['te'].transpose()
        elif data_struc['size'] == 'small':
            Ne_data = b2fstate['ne'][1:nx+1, 1:ny+1].transpose()
            Te_J = b2fstate['te'][1:nx+1, 1:ny+1].transpose()
        
        
        
        ev = 1.6021766339999999 * pow(10, -19)
        Te_data = Te_J / ev
        pol_in = int(pol_loc)
        
        
        if data_struc['size'] == 'full':
            psi = psiN[:, pol_in]
        
        elif data_struc['size'] == 'small':
            psi = psiN[1:ny+1, pol_in]
            
            
        Nd = Neuden[:, pol_in]
        Ne = Ne_data[:, pol_in]
        Te = Te_data[:, pol_in]
        

        rd = fm.Opacity_calculator(x_coord= psi, ne = Ne, te = Te, 
                               neuden = Nd, check_ne= check_ne, minor_rad = self.a)
             
        fit_dic = {'tanh_ne_fit': rd['tanh_ne_fit'], 'tanh_te_fit': rd['tanh_te_fit'],
             'exp_fit': rd['exp_fit'], 'x_coord_cut': rd['x_coord_cut'],
                     'ne_symmetry_point': rd['ne_symmetry_point'], 
                      'te_symmetry_point': rd['te_symmetry_point'],
               'n_sep_fit': rd['n_sep_fit'], 'NeuDen': Nd, 'Ne': Ne, 'Te': Te}
        
        return fit_dic
    
    
    def radial_data_fit(self, pol_loc, dat_size, check_ne):
        
        
        if self.withshift == False and self.withseries == False:
            
            
            nx = self.data['b2fgeo']['nx']
            ny = self.data['b2fgeo']['ny']
            
            if dat_size == 'full':
                
                self.load_output_data(param= 'NeuDen')
                Neuden_data = self.data['outputdata']['NeuDen']
                dat_struc = {'size': dat_size, 'nx': nx, 'ny': ny}
            
            elif dat_size == 'small':
                
                data = self.data['ft44']['dab2']
                Neuden_data = np.transpose(data[:, :, 0])
                dat_struc = {'size': dat_size, 'nx': nx, 'ny': ny}
            
            
            fstate = self.data['b2fstate']
            psiN_map = self.data['psi']['psival']
            
            fitresult = self.radial_data_fit_method(b2fstate = fstate, 
                        Neuden = Neuden_data, psiN = psiN_map, 
                        pol_loc = pol_loc, data_struc = dat_struc, check_ne = check_ne)
            
            self.data['radial_fit_data'] = fitresult
        
        elif self.withshift == True and self.withseries == False:
            
            self.load_output_data(param= 'NeuDen')
            fitresult_dic = {}
            
            for aa in self.data['dircomp']['multi_shift']:
                
                
                nx = self.data['b2fgeo'][aa]['nx']
                ny = self.data['b2fgeo'][aa]['ny']
                
                
                if dat_size == 'full':
                    
                    self.load_output_data(param= 'NeuDen')
                    
                    Neuden_data = self.data['outputdata']['NeuDen'][aa]
                    dat_struc = {'size': dat_size, 'nx': nx, 'ny': ny}
                
                elif dat_size == 'small':
                    data = self.data['ft44'][aa]['dab2']
                    Neuden_data = np.transpose(data[:, :, 0])
                    dat_struc = {'size': dat_size, 'nx': nx, 'ny': ny}
                
                    
                # Neuden_data = self.data['outputdata']['NeuDen'][aa]
                fstate = self.data['b2fstate'][aa]
                psiN_map = self.data['psi']['psival'][aa]
                
                                  
                fitresult = self.radial_data_fit_method(b2fstate = fstate, 
                            Neuden = Neuden_data, psiN = psiN_map, 
                pol_loc = pol_loc, data_struc = dat_struc, check_ne = check_ne)
                
                print('this is {}'.format(aa))
                    
                
                fitresult_dic[aa] = fitresult
            
            self.data['radial_fit_data'] = fitresult_dic
        
        elif self.withshift == False and self.withseries == True:
            
            fitresult_dic = {}
            
            for aa in list(self.data['dircomp']['Attempt'].keys()):
                
                if self.series_flag == 'twin_scan':
                    
                    nf = aa[0]
                    tf = aa[1]
                    
                    
                    nx = self.data['b2fgeo']['nx']
                    ny = self.data['b2fgeo']['ny']
                    
                    if dat_size == 'full':
                        
                        self.load_output_data(param= 'NeuDen')
                        
                        Neuden_data = self.data['outputdata']['NeuDen'][nf][tf]
                        dat_struc = {'size': dat_size, 'nx': nx, 'ny': ny}
                    
                    elif dat_size == 'small':
                        data = self.data['ft44'][nf][tf]['dab2']
                        Neuden_data = np.transpose(data[:, :, 0])
                        dat_struc = {'size': dat_size, 'nx': nx, 'ny': ny}
                
                    fstate = self.data['b2fstate'][nf][tf]
                
                
                else:
                    
                    self.load_output_data(param= 'NeuDen')
                    
                    Neuden_data = self.data['outputdata']['NeuDen'][aa]
                    fstate = self.data['b2fstate'][aa]
                    
                
                psiN_map = self.data['psi']['psival']
                
                fitresult = self.radial_data_fit_method(b2fstate = fstate, 
                    Neuden = Neuden_data, psiN = psiN_map, pol_loc = pol_loc,
                    data_struc = dat_struc, check_ne = check_ne)
            
                fitresult_dic[aa] = fitresult
            
            self.data['radial_fit_data'] = fitresult_dic
        
        elif self.withshift == True and self.withseries == True:
            print('radial_data_fit is not there yet!')
        
        
        else:
            print('radial_data_fit has a bug')
    
    
    
    def multirad_data_fit(self, pol_list, dat_size, check_ne):
        
        # self.load_output_data(param= 'NeuDen')
        
        self.load_ft44()
        self.load_output_data(param= 'NeuDen')
        
        if self.withshift == False and self.withseries == False:
            
            data = self.data['ft44']['dab2']
            Neuden_data = np.transpose(data[:, :, 0])
            # Neuden_data = self.data['outputdata']['NeuDen']
            fstate = self.data['b2fstate']
            psiN_map = self.data['psi']['psival']
            
            fitresult = self.radial_data_fit_method(b2fstate = fstate, 
                        Neuden = Neuden_data, psiN = psiN_map, pol_list = pol_list)
            
            self.data['radial_fit_data'] = fitresult
        
        elif self.withshift == True and self.withseries == False:
            
            fitresult_dic = {}
            
            for aa in self.data['dircomp']['multi_shift']:
                
                ind_fitresult_dic = {}
                
                for ind in pol_list:
                    
                    
                    nx = self.data['b2fgeo'][aa]['nx']
                    ny = self.data['b2fgeo'][aa]['ny']
                    
                    
                    if dat_size == 'full':
                        
                        self.load_output_data(param= 'NeuDen')
                        
                        Neuden_data = self.data['outputdata']['NeuDen'][aa]
                        dat_struc = {'size': dat_size, 'nx': nx, 'ny': ny}
                    
                    elif dat_size == 'small':
                        data = self.data['ft44'][aa]['dab2']
                        Neuden_data = np.transpose(data[:, :, 0])
                        dat_struc = {'size': dat_size, 'nx': nx, 'ny': ny}
                    
                    
                    
                    # Neuden_data = self.data['outputdata']['NeuDen'][aa]
                    fstate = self.data['b2fstate'][aa]
                    psiN_map = self.data['psi']['psival'][aa]
                    
                    fitresult = self.radial_data_fit_method(b2fstate = fstate, 
                                Neuden = Neuden_data, psiN = psiN_map, pol_loc = ind,
                                data_struc = dat_struc, check_ne = check_ne)
                    
                    ind_fitresult_dic[ind] = fitresult
                
                fitresult_dic[aa] = ind_fitresult_dic
            
            self.data['radial_fit_data'] = fitresult_dic
        
        elif self.withshift == False and self.withseries == True:
            
            fitresult_dic = {}
            
            for aa in list(self.data['dircomp']['Attempt'].keys()):
                           
                ind_fitresult_dic = {}
                
                for ind in pol_list:
                
                
                    Neuden_data = self.data['outputdata']['NeuDen'][aa]
                    fstate = self.data['b2fstate'][aa]
                    psiN_map = self.data['psi']['psival']
                    
                    fitresult = self.radial_data_fit_method(b2fstate = fstate, 
                                Neuden = Neuden_data, psiN = psiN_map, pol_loc = ind)
                    
                    ind_fitresult_dic[ind] = fitresult
            
                fitresult_dic[aa] = ind_fitresult_dic
            
            self.data['radial_fit_data'] = fitresult_dic
            
            
            
            
            
            
            
        
        elif self.withshift == True and self.withseries == True:
            print('radial_data_fit is not there yet!')
        
        
        else:
            print('radial_data_fit has a bug')
    
    

        
        
            
# ----------------------------------------------------------------------------           
    
    """



    """