# -*- coding: utf-8 -*-
"""
Created on Thu Sep 19 23:23:32 2024

@author: ychuang
"""

import SOLPS_set as sps
import SOLPSplotter_EB as spe

d = sps.Setting_dic()
lex = sps.loadDS_dic(d['DEV'])



xl = spe.EB_plot(DefaultSettings = d, loadDS = lex)

xl.load_mast_dir()
xl.load_solpsgeo()
xl.calcpsi_avcr()
xl.calc_RRsep(plotRR= False, plot_psi_dsa_align= False)
fitmastexp_setting_dic = {'writefile': True, 'plot_solps_fit': False, 
                          'plot_exp_and_fit': True, 'plot_shift_compare': False,
                          'data_print': True}
xl.fitmastexp(plot_setting_dic = fitmastexp_setting_dic)
xl.load_b2fstate()
xl.load_ft44()
xl.calc_sep_dsa()


xl.plot_EB(scan_style = 'denscan', dat_size = 'small')