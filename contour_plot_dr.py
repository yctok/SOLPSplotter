# -*- coding: utf-8 -*-
"""
Created on Wed Apr 16 18:27:05 2025

@author: ychuang
"""



from SOLPS_input.input_setting import Setting_dic, loadDS_dic
from module_load_for_plot.module_load import *
from twscan_module.twinscan_prepare import twscan_assist
from contour_plot.twscan_eirene_contour import Eirene_contour
from contour_plot.geo_contour_plot import fluxexpansion_contour
from contour_plot.contourplot_toolbox import contour_plot_method_collect
from contour_plot.target_contour import target_contour_plot
from contour_plot.twscan_contour_plot import twscan_contour
from contour_plot.vesselshift_contour import shiftvessel_contour
from contour_plot.twscan_binfocus_eirene_contour import eirene_binfocus_contour
from contour_plot.Eirene_contour import eirene_contour





class contour_datapipline:
    
       
    def __init__(self):
        # self.publish = 'b2plottersetting'
        
        DefaultSettings = Setting_dic()
        
        self.DF = DefaultSettings
        
        
        "Useful data"
        self.data = {'dircomp':{}, 'grid':{}, 'dirdata':{}, 'ExpDict': {}, 'dsa':{},
                     'gfile':{}, 'gridsettings': {}, 'psi':{}, 'DefaultSettings': {}, 
                     'outputdata':{}, 'iout_data':{}}

    def run_contour_plot(self):
        
        
        xta = twscan_assist(DF = self.DF, data = self.data)
        xlp = load_prepare_module(DF = self.DF, data = self.data)
        xps = plot_setting(DF = self.DF, data = self.data)
        xfm = fit_method_collection(DF = self.DF, data = self.data)
        xlc = load_coordgeo_method(DF = self.DF, data = self.data)
        xrp = RP_mapping(DF = self.DF, data = self.data, lcm = xlc, fmc= xfm)       
        xcpm = contour_plot_method_collect(DF = self.DF, data = self.data)
        xec = Eirene_contour(DF = self.DF, data = self.data, twa = xta, cpmc = xcpm)
        xfc = fluxexpansion_contour(DF = self.DF, data = self.data, fmc = xfm, cpmc = xcpm, rp = xrp)
        xtc = target_contour_plot(DF = self.DF, data = self.data, cpmc = xcpm)
        xtwc = twscan_contour(DF = self.DF, data = self.data)
        xsc = shiftvessel_contour(DF = self.DF, data = self.data)
        xebc = eirene_binfocus_contour(DF = self.DF, data = self.data, twa = xta, cpmc = xcpm)
        xec2 = eirene_contour(DF = self.DF, data = self.data)                         
        
        
        if self.DF.DEV == 'mast':
            
            
            poloidal_index_list = xlp.prepare_for_plots(plot_type = 'contour')
            
            
            
            """
            geo_contour_theme = ['fluxexpansion', 'shift_vessel']
            
            
            """
            
            
            geo_contour_theme = 'None'
            
            if geo_contour_theme == 'fluxexpansion':
                
                xfc.flux_expansion_contour_plot()
            
            elif geo_contour_theme == 'shift_vessel':
                
                xsc.shift_vessel_in_one()
            
            
            else:
                pass
                       
            
            withshift = self.DF.withshift
            withseries = self.DF.withseries
            
            
            if withshift == False and withseries == True:
                
                
                contour_theme = 'twscan_contour'
                
                if contour_theme == 'tw_eirene_contour':
                    
                    xec.twscan_eirene_contourplot(scan_style = 'tempscan', plot_option = 'atomic energyden', 
                                                  format_option = '1x1', norm_type = 'natural')
                
                elif contour_theme == 'twscan_contour':
                    
                    xtwc.twscan_contour_plot(scan_style = 'denscan')
                
                
                elif contour_theme == 'twscan_binfocus_contour':
                    
                    xebc.twscan_binfocus_eirene_contourplot(scan_style = 'tempscan', plot_option = 'Neuden contour')
                
                              
                
                else:
                    pass
                    
                    
       
            elif withshift == True and withseries == False:
                
                
                geo_contour_theme = 'None'
                
                if geo_contour_theme == 'shift_vessel':
                    
                    xsc.shift_vessel_in_one()
                
                
                else:
                    pass
                
                contour_theme = 'eirene_contour'
                
                if contour_theme == 'iout_paper':
                    
                    dat_list = ['neutral density', 'Poloidal flux', 'Source', 'hx']

                    xtc.iout_paper_plot(plotstyle = 'paper', dataname = 'Source', sideswitch = 'both')
                
                elif contour_theme == 'eirene_contour':
                    
                    xec2.plot_eireneoutput()

                    xec2.eirene_contour()
                
                
                
                
                
            
            
                
                
            
            


if __name__ == "__main__":
    dpl = contour_datapipline()
    dpl.run_contour_plot()