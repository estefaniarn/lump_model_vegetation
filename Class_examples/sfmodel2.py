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

  

    def simulate(self, precipitation, pet, sf_max, df_max, X, tree_max, wp):
        Nt = len(precipitation)
        q1 = [0] * Nt
        q2 = [0] * Nt
        q3 = [0] * Nt
        q3_1 = [0] * Nt
        q3_2 = [0] * Nt
        q4 = [0] * Nt
        q4_1 = [0] * Nt
        q5 = [0] * Nt
        q5_1 = [0] * Nt
        q6 = [0] * Nt
        

        for n in range(Nt):
            self.precipitation_mechanism(precipitation, n, sf_max, X, q1, q2)
            self.soil_fracture_mechanism(precipitation, n, wp, sf_max, df_max, q3)
            # self.fracture_soil_mechanism(precipitation, n, sf_max, q3_1)
            # self.soil_to_quickflow(precipitation, n, sf_max, q3_2)
            # self.fracture_plant_mechanism(precipitation, n, pet, df_max, tree_max, q4, q4_1)
            # self.soil_plant_mechanism(precipitation, n, pet, sf_max, tree_max, q5, q5_1)
            # self.plant_sapflow_transpiration(precipitation, n, pet, tree_max, q6)
            # self.pet_n[n] = (pet[n] - min(pet)) / (max(pet) - min(pet))
            # self.sapfl`ow[n] = pet[n] + (q4_1[n] + q5_1[n] + q6[n])

            if n < (Nt - 1):
                self.surface_fracture[n + 1] = self.surface_fracture[n]
                self.deep_fracture[n + 1] = self.deep_fracture[n]
                self.quickflow[n + 1] = self.quickflow[n]
                self.tree[n + 1] = self.tree[n]

    def precipitation_mechanism(self, precipitation, n, sf_max, X, q1, q2):
        if precipitation[n] > 0:
            if self.surface_fracture[n] < sf_max:
                q1[n] = precipitation[n] * X  # quickflow loss
                q2[n] = precipitation[n] * (1 - X)  # infiltration into soil
                self.surface_fracture[n] += q2[n]
                self.quickflow[n] += q1[n]
            else:
                q1[n] = precipitation[n]*0.5 #assume 50 goes to quickflow and 50 to overflow
                q2[n] = 0
                self.quickflow[n] += q1[n]
                self.surface_fracture[n] += q2[n]     
        else:
            q1[n] = 0
            q2[n] = 0

    def soil_fracture_mechanism(self, precipitation, n, wp, sf_max, df_max, q3):
        #rain pushes pre-existing water in the soil into the deep fracture
        if precipitation[n] > 0:
            if self.surface_fracture[n]>wp: #wilting point 
                if (self.surface_fracture[n] > self.deep_fracture[n])&(self.deep_fracture[n]<df_max): 
                    q3[n] = 0.2*(self.surface_fracture[n]/sf_max) #infiltration (****should add up when I include evaporation and water uptake under same conditions)
                    self.deep_fracture[n] += q3[n]
                    self.surface_fracture[n] -= q3[n]
                else: 
                    q3[n] = 0
                    # self.deep_fracture[n] += q3[n] #may be redundant
                    # self.surface_fracture[n] -= q3[n]
            else:
                q3[n] = 0
        
        # with recent rain water moves from surface to deep fracture slower
        elif (precipitation[n] == 0) & any(var >= 0.02 for var in precipitation[n-48:n-1]):
            if self.surface_fracture[n]>wp:
                if (self.surface_fracture[n] > self.deep_fracture[n])&(self.deep_fracture[n]<df_max): #the above step makes deep>surface so this wont run
                    q3[n] = 0.1*(self.surface_fracture[n]/sf_max) #infiltration (****should add up when I include evaporation and water uptake under same conditions)
                    self.deep_fracture[n] += q3[n]
                    self.surface_fracture[n] -= q3[n]
                else: 
                    q3[n] = 0
                    # self.deep_fracture[n] += q3[n] #may be redundant
                    # self.surface_fracture[n] -= q3[n]
            else:
                q3[n] = 0

        else:
            q3[n] = 0 #maybe add here evaporation and water uptake




      # #self.pet = [0] * Nt
        # self.surface_fracture = [None] * Nt
        # self.deep_fracture = [None] * Nt
        # self.quickflow = [None] * Nt
        # self.tree = [None] * Nt
        # self.sapflow = [None] * Nt
        # #self.pet_n = [None] * Nt


        # Initial conditions
        # self.surface_fracture[0] = 0.7
        # self.deep_fracture[0] = 0.3
        # self.quickflow[0] = 0.001
        # self.tree[0] = 0.1

        # Nt = len(precipitation)
        # q1 = [None] * Nt
        # q2 = [None] * Nt
        # q3 = [None] * Nt
        # q3_1 = [None] * Nt
        # q3_2 = [None] * Nt
        # q4 = [None] * Nt
        # q4_1 = [None] * Nt
        # q5 = [None] * Nt
        # q5_1 = [None] * Nt
        # q6 = [None] * Nt