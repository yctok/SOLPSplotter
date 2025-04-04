# -*- coding: utf-8 -*-
"""
Created on Thu Apr  3 02:38:15 2025

@author: ychuang
"""

"""
This code is set for twinscan series
This code plot the poloidal angle bin

"""

import SOLPS_set as sps
import twscan_bin_plot as tbp
import SOLPS_transcoe_adj as sta


d = sps.Setting_dic()
lex = sps.loadDS_dic(d['DEV'])



xl = tbp.bin_plot(DefaultSettings = d, loadDS = lex)

xl.load_mast_dir()
xl.load_solpsgeo()
# xl.calcpsi()
xl.calcpsi_avcr()
xl.calc_RRsep(plotRR= False, plot_psi_dsa_align= False)
fitmastexp_setting_dic = {'writefile': True, 'plot_solps_fit': False, 
                          'plot_exp_and_fit': True, 'plot_shift_compare': False,
                          'data_print': True}
xl.fitmastexp(plot_setting_dic = fitmastexp_setting_dic)
xl.load_b2fstate()
xl.load_ft44()
# xl.load_b2fplasmf()
# xl.b2fplasmf_filter()
# xl.load_output_data(param= 'Te')
xl.calc_sep_dsa()

xl.load_vessel()

xl.set_plot()

# poloidal_index_list = ['59']
xl.calc_dsa(pol_loc= '59')

poloidal_index_list = []
for i in range(40):
    poloidal_index_list.append('{}'.format(28 + i))

xl.opacity_data_fit(pol_list = poloidal_index_list, dat_size = 'small', check_ne = False)
# xl.calc_pol_angle(pol_list = poloidal_index_list, plot_angle= False)
xl.radial_data_fit(pol_loc = poloidal_index_list[0], dat_size = 'small', check_ne = False)
xl.calc_pol_angle(pol_list = poloidal_index_list, plot_angle= False)

# xl.load_fluxes_iout()
xl.load_b2wdat()

xl.bin_check(pol_list = poloidal_index_list)

xl.pol_bin_plot(pol_list = poloidal_index_list)
