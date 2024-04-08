# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 16:51:44 2024

@author: ychuang
"""

import SOLPS_set as sps
import matplotlib.pyplot as plt
import SOLPSplotter_contour as spc
import SOLPS_transcoe_adj as sta
import numpy as np

d = sps.Setting_dic()
lex = sps.loadDS_dic(d['DEV'])



xl = spc.PlotContour(DefaultSettings = d, loadDS = lex)

xl.load_mast_dir()
xl.load_solpsgeo()
# xl.calcpsi()
xl.calcpsi_avcr()
xl.calc_RRsep(plotRR= False, plot_psi_dsa_align= False)
fitmastexp_setting_dic = {'writefile': True, 'plot_solps_fit': False, 
                          'plot_exp_and_fit': False, 'plot_shift_compare': False,
                          'data_print': True}
xl.fitmastexp(plot_setting_dic = fitmastexp_setting_dic)
xl.load_vessel()
xl.load_ft44()
xl.set_plot()
xl.load_b2fstate()

xl.calc_sep_dsa()
poloidal_index_list = []
for i in range(10):
    poloidal_index_list.append('{}'.format(28 + i))
    
xl.opacity_data_fit(pol_list = poloidal_index_list)
xl.calc_pol_angle(pol_list = poloidal_index_list, plot_angle= False)

# xl.opacity_poloidal_plot(log_flag = False, save_pdf = False)

xl.neuden_percent()

topic = 'Q3'


"""

('b2tfnb_bxuanax001.dat', False), ('hx.dat', True), ('hy.dat', True), 
('b2npc11_fnax001.dat', False), ('hz.dat', True)

"""

if topic == 'Q1-1':
    f_tuple1 = [('b2npco_sna000.dat', 'g_source_0'), ('vol.dat', 'sqrt_g')]
    f_tuple2 = [('b2npc11_sna001.dat', 'g_source_1'), ('vol.dat', 'sqrt_g')]
    f_tuple3 = [('b2npco_dnadt000.dat', 'g_dnadt_0'), ('vol.dat', 'sqrt_g')]
    f_tuple4 = [('b2npc11_dnadt001.dat', 'g_dnadt_1'), ('vol.dat', 'sqrt_g')]
    
    f_list1 = [f_tuple1, f_tuple2, f_tuple3, f_tuple4]
    single = False
    f_spc_list = [f_tuple3]
    
    
    if single:
        for tuples in f_spc_list:
            qu = xl.load_iout_ratio(file_tuple = tuples)
            print(qu)
            
            xl.iout_contour_plot(quant = qu, log_bar = False)
            xl.iout_contour_plot(quant = qu, log_bar = True)
            
    else:
        for tuples in f_list1:
            qu = xl.load_iout_ratio(file_tuple = tuples)
            print(qu)
            
            xl.iout_contour_plot(quant = qu, log_bar = False)
            xl.iout_contour_plot(quant = qu, log_bar = True)
    
    
    # f_tuple1 = [('b2npco_sna000.dat', 'g_source_0'), ('b2npco_dnadt000.dat', 'g_dnadt_0')]
    f_tuple2 = [('b2npc11_sna001.dat', 'g_source_1'), ('b2npc11_dnadt001.dat', 'g_dnadt_1')]
    
    f_list1 = [f_tuple2]

   
    for tuples in f_list1:
        qu = xl.load_iout_ratio(file_tuple = tuples)
        print(qu)
        
        xl.iout_contour_plot(quant = qu, log_bar = False)
        xl.iout_contour_plot(quant = qu, log_bar = True)

elif topic == 'Q1-2':
    
    f_tuple5 = [('hx.dat', 'hx'),('vol.dat', 'sqrt_g')]
    f_tuple6 = [('hy.dat', 'hy'), ('vol.dat', 'sqrt_g')]
    
    flux_tuple = [('b2npco_fnax000.dat', 'flux_x_0'), ('b2npc11_fnax001.dat', 'flux_x_1'),
                ('b2npco_fnay000.dat', 'flux_y_0'), ('b2npc11_fnay001.dat', 'flux_y_1')]
    
    
    f_list2 = [f_tuple5, f_tuple6]
    fcoe_list = []
    
    
    for tuples in f_list2:
        qu = xl.load_iout_ratio(file_tuple = tuples)
        print(qu)
        fcoe_list.append(qu)
    
    # print(fcoe_list)
    
    flux_qu_list = []
    
    for flux_tpl in flux_tuple:
        
        flux_qu = xl.load_iout(filename = flux_tpl[0], simple_quant = flux_tpl[1])
        print(flux_qu)
        # print(flux_qu.split('_'))
        flux_qu_list.append(flux_qu)
    
    plot_flux_ratio = False
    
    if plot_flux_ratio:
        print(flux_qu_list)
        
        for i in range(2):
            qu = xl.load_iout_name_ratio(name1 = flux_qu_list[i], name2 = flux_qu_list[i + 2])
            print(qu)
            
            xl.iout_contour_plot(quant = qu, log_bar = False)
            xl.iout_contour_plot(quant = qu, log_bar = True)
    else:
        pass
        
    
    
    
    
    res_qu_list = []
    
    for item in flux_qu_list:
        if item.split('_')[1] == 'x':
            res_qu = xl.load_iout_multi(name1 = fcoe_list[0], name2 = item)
            print(res_qu)
            res_qu_list.append(res_qu)

            xl.iout_contour_plot(quant = res_qu, log_bar = False)
            xl.iout_contour_plot(quant = res_qu, log_bar = True)
        
        elif item.split('_')[1] == 'y':
            res_qu = xl.load_iout_multi(name1 = fcoe_list[1], name2 = item)
            print(res_qu)
            res_qu_list.append(res_qu)

            xl.iout_contour_plot(quant = res_qu, log_bar = False)
            xl.iout_contour_plot(quant = res_qu, log_bar = True)
        
        else:
            print('a bug! flag is {}'.format(item.split('_')[1]))

    print(res_qu_list)
    
    for i in range(2):
        qu = xl.load_iout_name_ratio(name1 = res_qu_list[i], name2 = res_qu_list[i + 2])
        print(qu)
        
        xl.iout_contour_plot(quant = qu, log_bar = False)
        xl.iout_contour_plot(quant = qu, log_bar = True)
        
    
elif topic == 'Q2':
    
    if xl.withshift == True and xl.withseries == False:
        
        
        gcoe_tuple = [('hx.dat', 'hx'), ('hy.dat', 'hy'), ('hz.dat', 'hz')]
        
        for item in gcoe_tuple:
            
            qu = xl.load_iout(filename = item[0], simple_quant = item[1])
            print(qu)
        
        gcoe_list = ['hx', 'hy', 'hz']
        for coe in gcoe_list:
            for aa in xl.data['dircomp']['multi_shift']:
                if aa == 'org':
                    pass
                else:
                    dif_qu = xl.load_iout_differ(name = coe, itername1 = aa, itername2 = 'org')
                    print(dif_qu)
                    
                    data, per_qu = xl.load_iout_name_ratio(name1 = dif_qu, name2 = coe,
                                stdname = 'org', itername = aa)
                    print(per_qu)
                    
                    xl.plot_change_data(data = data, log_bar = False, 
                             itername = aa, quant = per_qu, ma100 = True)
                    
elif topic == 'Q3':
    
    if xl.withshift == True and xl.withseries == False:
        
        
        f_tuple5 = [('hx.dat', 'hx'),('vol.dat', 'sqrt_g')]
        f_tuple6 = [('hy.dat', 'hy'), ('vol.dat', 'sqrt_g')]
        
        flux_tuple = [('b2npc11_fnax001.dat', 'flux_x_0'), ('b2npc11_fnay001.dat', 'flux_y_0')]
        
        # flux_tuple = [('b2npc11_fnax001.dat', 'flux_x_0'), ('b2npc11_fnay001.dat', 'flux_y_0')]
        
        
        f_list2 = [f_tuple5, f_tuple6]
        fcoe_list = []
        
        
        for tuples in f_list2:
            
            qu_dic = {}
            for aa in xl.data['dircomp']['multi_shift']:
                data, qu = xl.load_iout_ratio(file_tuple = tuples, itername = aa)
                qu_dic[aa] = data
            
            xl.data['iout_data'][qu] = qu_dic
                
            print(qu)
            fcoe_list.append(qu)
            
            
        print(fcoe_list)
        
        flux_qu_list = []
        
        for flux_tpl in flux_tuple:
            
            flux_qu = xl.load_iout(filename = flux_tpl[0], simple_quant = flux_tpl[1])
            print(flux_qu)
            # print(flux_qu.split('_'))
            flux_qu_list.append(flux_qu)
        
        res_qu_list = []
        
        for item in flux_qu_list:
            
            res_qu_dic = {}
            for aa in xl.data['dircomp']['multi_shift']:
                if item.split('_')[1] == 'x':
                    data, res_qu = xl.load_iout_multi(name1 = fcoe_list[0], name2 = item, 
                                        input_name= 'poloidal_flux', itername = aa)
                    
                    res_qu_dic[aa] = data
                
                elif item.split('_')[1] == 'y':
                    data, res_qu = xl.load_iout_multi(name1 = fcoe_list[1], name2 = item,
                                        input_name= 'radial_flux', itername = aa)
                    
                    res_qu_dic[aa] = data
          
                else:
                    print('a bug! flag is {}'.format(item.split('_')[1]))
            
            xl.data['iout_data'][res_qu] = res_qu_dic
            
        
            print(res_qu)
            res_qu_list.append(res_qu)
        
        
        print(res_qu_list)
        
        # for rqu in res_qu_list:
            
        #     xl.iout_contour_plot(quant = rqu, log_bar= True, ma100= False, bounds = {})
        
        
        for resqu in res_qu_list:
            
            resqu_per_dic = {}
            std_cp = 'org'
            for aa in xl.data['dircomp']['multi_shift']:
                if aa == std_cp:
                    pass
                else:
                    dif_qu = xl.load_differ(name = resqu, itername1 = aa, 
                                            itername2 = std_cp, setname = 'iout_data')
                    print(dif_qu)
                    
                    data, per_qu = xl.load_iout_name_ratio(name1 = dif_qu, name2 = resqu,
                                    stdname = std_cp, itername = aa, setname = 'iout_data')
                    print(per_qu)
                    resqu_per_dic[aa] = data
                    bon = {'max': 100, 'min': -100}
                    xl.plot_change_data(data = data, log_bar = False, bounds = bon,
                                         itername = aa, quant = per_qu, ma100 = True)
                
            xl.data['iout_data'][per_qu] = resqu_per_dic
        
        
        
        plt.figure(figsize=(7,7))

        for aa in xl.data['dircomp']['multi_shift']:
            color_dic = {'org': 'red', 'dot3': 'orange', 'dot5': 'green',
                         'dot7': 'blue', 'one': 'purple'}
            A_dic = {'org': '1.4', 'dot3': '2.0', 'dot5': '2.4',
                      'dot7': '2.8', 'one': '3.4'}
            st = int(poloidal_index_list[0]) -1
            ed = int(poloidal_index_list[-1])
            sol_pol_flux = xl.data['iout_data']['poloidal_flux'][aa][20:, st:ed]
            mean_pol_flux = np.mean(sol_pol_flux, axis=0)
            std_pol_flux = np.std(sol_pol_flux, axis=0)
            
            norm_pol_flux = mean_pol_flux/ max(mean_pol_flux)
            neuden_d = xl.data['opacity_poloidal'][aa]['neutral_density']
            y = np.transpose(neuden_d)/ max(neuden_d)
            plt.errorbar(mean_pol_flux, y, xerr= std_pol_flux, fmt = '-', 
                         color = color_dic[aa], label= 'aspect ratio = {}'.format(A_dic[aa]))
            plt.title('neutral density and ion poloidal flux ')
            plt.xlabel('ion poloidal flux')
            plt.legend()


        plt.figure(figsize=(7,7))

        for aa in xl.data['dircomp']['multi_shift']:
            color_dic = {'org': 'red', 'dot3': 'orange', 'dot5': 'green',
                         'dot7': 'blue', 'one': 'purple'}
            A_dic = {'org': '1.4', 'dot3': '2.0', 'dot5': '2.4',
                      'dot7': '2.8', 'one': '3.4'}
            st = int(poloidal_index_list[0]) -1
            ed = int(poloidal_index_list[-1])
            sol_pol_flux = xl.data['iout_data']['radial_flux'][aa][20:, st:ed]
            mean_pol_flux = np.mean(sol_pol_flux, axis=0)
            std_pol_flux = np.std(sol_pol_flux, axis=0)
            norm_pol_flux = mean_pol_flux/ max(mean_pol_flux)
            
            
            neuden_d = xl.data['opacity_poloidal'][aa]['neutral_density']
            y = np.transpose(neuden_d)/ max(neuden_d)
            plt.errorbar(mean_pol_flux, y, xerr= std_pol_flux, fmt = '-', 
                        color = color_dic[aa], label= 'aspect ratio = {}'.format(A_dic[aa]))
            plt.title('neutral density and ion radial flux correlation')
            plt.xlabel('ion radial flux')
            plt.legend()
        
        
        
    
        
        
        
        anglemean_pol_flux = []
        cv_pol_flux = []
        std_pol_flux = []
        neuden_list = []
        cv_neuden = []
        std_neuden = []
        anglemean_rad_flux = []
        std_rad_flux = []
        st = int(poloidal_index_list[0]) -1
        ed = int(poloidal_index_list[-1])
        one_angle = False
        ind = st + 6
        for aa in xl.data['dircomp']['multi_shift']:
            A_dic = {'org': '1.4', 'dot3': '2.0', 'dot5': '2.4',
                      'dot7': '2.8', 'one': '3.4'}
            
            if one_angle:
                sol_pol_flux = xl.data['iout_data']['poloidal_flux'][aa][20:, ind]
                anglemean_pol_flux.append(-1*np.mean(sol_pol_flux, axis=0))
                std_pol_flux.append(np.std(sol_pol_flux, axis=0))
                cv_pol_flux.append(-1*np.std(sol_pol_flux, axis=0) / np.mean(sol_pol_flux, axis=0))
                
                neuden_d = xl.data['ft44'][aa]['dab2'][ind, 20:, 0]
                neuden_list.append(np.mean(neuden_d, axis=0))
                # mean_neuden = np.mean(neuden_d, axis=0)
                cv_neuden.append(np.std(neuden_d, axis=0) / np.mean(neuden_d, axis=0))
                std_neuden.append(np.std(neuden_d, axis=0))
                
                sol_rad_flux = xl.data['iout_data']['radial_flux'][aa][20:, ind]
                anglemean_rad_flux.append(np.mean(sol_rad_flux, axis=0))
                std_rad_flux.append(np.std(sol_rad_flux, axis=0))
            
            else:
                sol_pol_flux = xl.data['iout_data']['poloidal_flux'][aa][20:, st:ed]
                mean_pol_flux = np.mean(sol_pol_flux, axis=0)
                anglemean_pol_flux.append(-1*np.mean(mean_pol_flux, axis=0))
                
                cv_pol_flux.append(-1*np.std(mean_pol_flux, axis=0) / np.mean(mean_pol_flux, axis=0))
                std_pol_flux.append(np.std(mean_pol_flux, axis=0))
                
                neuden_d = xl.data['opacity_poloidal'][aa]['neutral_density']
                neuden_list.append(np.mean(neuden_d, axis=0))
                # mean_neuden = np.mean(neuden_d, axis=0)
                cv_neuden.append(np.std(neuden_d, axis=0) / np.mean(neuden_d, axis=0))
                std_neuden.append(np.std(neuden_d, axis=0))
                
                sol_rad_flux = xl.data['iout_data']['radial_flux'][aa][20:, st:ed]
                mean_rad_flux = np.mean(sol_rad_flux, axis=0)
                anglemean_rad_flux.append(np.mean(mean_rad_flux, axis=0))
                std_rad_flux.append(np.std(mean_rad_flux, axis=0))
                
                
            
        fig, ax1 = plt.subplots()
        aspect_list = [1.4, 2.0, 2.4, 2.8]
        color = 'tab:red'
        
        print(cv_pol_flux)
        print(cv_neuden)
        
        ax1.errorbar(aspect_list, anglemean_pol_flux, yerr= std_pol_flux, 
                      fmt = '-', color= color)
        # ax1.scatter(aspect_list, anglemean_pol_flux, color= color)
        ax1.set_ylabel('poloidal flux', color= color)
        ax1.tick_params(axis='y', labelcolor = color)
        
        ax2 = ax1.twinx()
        
        color2 = 'tab:blue'
        
        ax2.errorbar(aspect_list, neuden_list, yerr= std_neuden, 
                    fmt = '-', color= color2)
        # ax2.scatter(aspect_list, neuden_list, color= color2)
        ax2.tick_params(axis='y', labelcolor = color2)
        
        ax2.set_ylabel('neutral density', color= color2)
        
        ax1.set_title('neutral density and ion poloidal flux ')
        ax1.set_xlabel('aspect ratio')
            
        
        
        # fig, ax1 = plt.subplots()
        # aspect_list = [1.4, 2.0, 2.4, 2.8]
        # color = 'tab:red'
        
        
        # ax1.scatter(aspect_list, anglemean_pol_flux, color= color)
        # # ax1.scatter(aspect_list, anglemean_pol_flux, color= color)
        # ax1.set_ylabel('poloidal flux', color= color)
        # ax1.tick_params(axis='y', labelcolor = color)
        
        # ax2 = ax1.twinx()
        
        # color2 = 'tab:blue'
        
        # ax2.scatter(aspect_list, neuden_list, color= color2)
        # # ax2.scatter(aspect_list, neuden_list, color= color2)
        # ax2.tick_params(axis='y', labelcolor = color2)
        
        # ax2.set_ylabel('neutral density', color= color2)
        
        # ax1.set_title('neutral density and ion poloidal flux ')
        # ax1.set_xlabel('aspect ratio')
            
            
            
        fig, ax1 = plt.subplots()
        
        # color = 'tab:red'
        
        ax1.errorbar(aspect_list, anglemean_rad_flux, yerr= std_rad_flux, 
                      fmt = '-', color= color)
        # ax1.scatter(aspect_list, anglemean_rad_flux, color= 'red')
        ax1.set_ylabel('radial flux', color= color)
        ax1.tick_params(axis='y', labelcolor = color)
        
        ax2 = ax1.twinx()
        
        ax2.errorbar(aspect_list, neuden_list, yerr= std_neuden, 
                    fmt = '-', color= color2)
        ax2.set_ylabel('neutral density', color= color2)
        ax2.tick_params(axis='y', labelcolor = color2)
        
        
        ax1.set_title('neutral density and ion radial flux ')
        ax1.set_xlabel('aspect ratio')
        # ax1.legend()
        
            
            

            

                    
elif topic == 'Q3-1':
    
    
    coe = 'dab2'
    
    
    for aa in xl.data['dircomp']['multi_shift']:
        if aa == 'org':
            pass
        else:
            dif_qu = xl.load_differ(name = coe, itername1 = aa, 
                                itername2 = 'org', setname = 'ft44')
            print(dif_qu)
            
            data, per_qu = xl.load_iout_name_ratio(name1 = dif_qu, name2 = coe,
                        stdname = 'org', itername = aa, setname = 'ft44')
            print(per_qu)
            
            neuden_data = np.transpose(data[:, :, 0])
            print(np.shape(neuden_data))
            
            bon = {'max': 100, 'min': -100}
            
            xl.plot_change_data(data = neuden_data, log_bar = True, bounds = bon, 
                     itername = aa, quant = 'neutral density increase percentage', ma100 = True)
    
    for aa in xl.data['dircomp']['multi_shift']:
        
        data = xl.data['ft44'][aa][coe]
        neuden_data = np.transpose(data[:, :, 0])
        
        xl.plot_change_data(data = neuden_data, log_bar = True, bounds = {}, 
                 itername = aa, quant = 'neutral density', ma100 = False)
    
        
elif topic == 'Q3-2':
    
    for rqu in res_qu_list:
        
        xl.iout_contour_plot(quant = rqu, log_bar= False, ma100= False, bounds = {})
    

    
elif topic == 'Q5': 
    
    f_tuple1 = [('b2npco_sna000.dat', 'g_source_0'), ('vol.dat', 'sqrt_g')]
    f_tuple2 = [('b2npc11_sna001.dat', 'g_source_1'), ('vol.dat', 'sqrt_g')]
    f_tuple3 = [('b2npco_dnadt000.dat', 'g_dnadt_0'), ('vol.dat', 'sqrt_g')]
    f_tuple4 = [('b2npc11_dnadt001.dat', 'g_dnadt_1'), ('vol.dat', 'sqrt_g')]
    
    f_list1 = [f_tuple1, f_tuple2, f_tuple3, f_tuple4]
    single = False
    f_spc_list = [f_tuple3]
    
    
    if single:
        for tuples in f_spc_list:
            qu = xl.load_iout_ratio(file_tuple = tuples)
            print(qu)
            
            xl.iout_contour_plot(quant = qu, log_bar = False)
            xl.iout_contour_plot(quant = qu, log_bar = True)
            
    else:
        for tuples in f_list1:
            qu = xl.load_iout_ratio(file_tuple = tuples)
            print(qu)
            
            xl.iout_contour_plot(quant = qu, log_bar = False)
            xl.iout_contour_plot(quant = qu, log_bar = True)
    
    
    

elif topic == 'test':
    
    iout_quant = [ ('b2npco_sna000.dat', False), ('b2npc11_sna001.dat', False), 
                  ('b2stel_sna_ion000.dat', False), ('b2stbr_sna_eir001.dat', False), 
                  ('b2stcx_sna_001.dat', False), ('b2npc11_dnadt001.dat', False), ('b2stel_sna_rec000.dat', False)]



    for item in iout_quant:
        
        qu = xl.load_iout(filename = item[0], simple_quant = item[1])
        print(qu)

        xl.iout_contour_plot(quant = qu)
        

else:
    print('no topic!')





# for aa in xl.data['dircomp']['multi_shift']:
#     if aa == 'org':
#         pass
#     else:
#         plt.figure(figsize=(7,7))
#         st = int(poloidal_index_list[0]) -1
#         ed = int(poloidal_index_list[-1])
#         x = xl.data['iout_data']['poloidal_flux_change_percent'][aa][19, st:ed]
#         y = xl.data['neuden_change'][aa]
#         plt.scatter(x, y)
#         plt.title('{} percent change correlation'.format(aa))












    


