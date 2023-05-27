#import numpy as np
#import pandas as pd

class sfmodel: 

    def __init__(self,Nt):
        
        self.surface_fracture = [0] * Nt
        self.deep_fracture = [0] * Nt
        self.quickflow = [0] * Nt
        self.tree = [0] * Nt
        self.sapflow = [0] * Nt

        self.predicate_precipitation_on = False
        self.tracker_precipitation = [None]*Nt
        self.predicate_recent_rain_on = False
        self.tracker_recent_rain = [None]*Nt

    def simulate(self, precipitation, pet, sf_max, df_max, X, tree_max, wp):
        Nt = len(precipitation)
        q1 = [0] * Nt
        q2 = [0] * Nt

        for n in range(Nt):

            # Update the flag based on rain event
            if precipitation[n] > 0:
                self.predicate_precipitation_on = True
            else: 
                self.predicate_precipitation_on = False
            
            
            # Update the flag based on recent rain 
            if (precipitation[n] == 0) & any(var >= 0.02 for var in precipitation[max(0, n-48):n]):
                self.predicate_recent_rain_on = True 
            else:
                self.predicate_recent_rain_on = False
            
            print(precipitation[n],self.predicate_recent_rain_on)
            

            # Run and update the model
            self.precipitation_mechanism(precipitation, n, sf_max, X, q1, q2)
            #self.soil_fracture_mechanism(precipitation, n, wp, sf_max, df_max, q3)
            if n < (Nt - 1):
                self.surface_fracture[n + 1] = self.surface_fracture[n]
                self.deep_fracture[n + 1] = self.deep_fracture[n]
                self.quickflow[n + 1] = self.quickflow[n]
                self.tree[n + 1] = self.tree[n] 
                self.tracker_recent_rain[n] = self.predicate_recent_rain_on
               


    def precipitation_mechanism(self, precipitation, n, sf_max, X, q1, q2):
        if self.predicate_precipitation_on:
            q1[n] = precipitation[n] * X  # quickflow loss
            q2[n] = precipitation[n] * (1 - X)  # infiltration into soil
            self.surface_fracture[n] += q2[n]
            self.quickflow[n] += q1[n]
   
        elif self.predicate_recent_rain_on:
            q1[n] = 0
            q2[n] = (self.surface_fracture[n]/sf_max)*0.5  # infiltration into deeper f
            self.surface_fracture[n] -= q2[n]
            self.quickflow[n] += q1[n]

        else:
            q1[n] = 0
            q2[n] = 0
            self.surface_fracture[n] += q2[n]
            self.quickflow[n] += q1[n]
    
        
        
            



            # self.soil_fracture_mechanism(precipitation, n, wp, sf_max, df_max, q3)
            # self.fracture_soil_mechanism(precipitation, n, sf_max, q3_1)
            # self.soil_to_quickflow(precipitation, n, sf_max, q3_2)
            # self.fracture_plant_mechanism(precipitation, n, pet, df_max, tree_max, q4, q4_1)
            # self.soil_plant_mechanism(precipitation, n, pet, sf_max, tree_max, q5, q5_1)
            # self.plant_sapflow_transpiration(precipitation, n, pet, tree_max, q6)
            # self.pet_n[n] = (pet[n] - min(pet)) / (max(pet) - min(pet))
            # self.sapfl`ow[n] = pet[n] + (q4_1[n] + q5_1[n] + q6[n])