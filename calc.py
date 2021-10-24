#import cadquery as cq
import pandas as pd
from math import sin, cos, pi, floor
from bisect import bisect_right


#### Functions

def get_s(d,p,rp,k=1.5,sz=1):
    s=3
    ds=100
    
    while(abs(ds)>0.000001 and s > 0. and s <20.):
        
        beta = 2.3 + (0.0325/((s/d)**0.73))
        s_new = (d*p*beta)     / (40* rp/k * sz)
        ds = s_new - s
        s=s_new
        #print("S: {}   beta: {}".format(s, beta))
    return s
        
def get_volume(d, h,s, t = "Klöpperboden"):
    """
        Standard 20 mm Rand oberhalb von Boden
    """
    vol = 0
    if t == "Klöpperboden":
        vol = 0.0607*d**3+ 20*((d-s)/2)**2*pi*1e-9
        

def calculate_vessel(durchmesser_ohne_iso,hoehe_tank, pressure, temp, tanktyp = "warmwasser", bodentyp = "Klöpperboden", material=1.0038,laenge_fuss=150, isolation=160):
        
    ## constants
    K_safety = 1.5
    p_safety = 1.2
    schweisszulage = 1

    ### Define variables
    materialstaerke = [3,4,5,6,8,10,12,15,20]

    ####


    mat_params = pd.read_csv("metal_data.csv", sep=";")
    mat_params = mat_params.rename(columns={"Unnamed: 0": "Typ"})
    mat_params["f(T)"] = -(mat_params["RP50"] - mat_params["RP125"])/75


    pressure_tot = pressure + hoehe_tank*9.81/1e5

    if temp>50:
        mat_params["RP_eff"] = mat_params["RP50"] + (temp-50)*mat_params["f(T)"]
    else: 
        mat_params["RP_eff"] = mat_params["RP50"] 

    RP_mat = mat_params["RP_eff"][mat_params["Typ"]==material][0]



    ### Results s
    theor_boden_oben = get_s(durchmesser_ohne_iso,pressure,RP_mat)
    theor_mantel_oben = (durchmesser_ohne_iso*pressure*p_safety)     / ((20*RP_mat/K_safety*0.85 * schweisszulage)+p_safety)
    theor_mantel_unten = (durchmesser_ohne_iso*pressure_tot*p_safety) / ((20*RP_mat/K_safety*0.85 * schweisszulage)+p_safety)
    theor_boden_unten = get_s(durchmesser_ohne_iso,pressure_tot,RP_mat)

    boden_oben = materialstaerke[bisect_right(materialstaerke,theor_boden_oben)]
    mantel_oben = materialstaerke[bisect_right(materialstaerke,theor_mantel_oben)]
    mantel_unten = materialstaerke[bisect_right(materialstaerke,theor_mantel_unten)]
    boden_unten = materialstaerke[bisect_right(materialstaerke,theor_boden_unten)]
    
    print(boden_oben)
        
        
        
def main():
    
    #import cadquery as cq
    import pandas as pd
    from math import sin, cos, pi, floor
    from bisect import bisect_right
    ### Arguments
    
    tanktyp = "warmwasser"   #selection
    durchmesser_ohne_iso = 1400
    hoehe_tank = 1870
    isolation = 160

    fusstyp = "UNP 140"
    laenge_fuss = 150

    bodentyp = "Klöpperboden"
    bodenfreiheit = 180

    material = 1.0038
    temp = 65
    pressure = 3
    
    calculate_vessel(durchmesser_ohne_iso, hoehe_tank, pressure, temp, tanktyp)
    


if __name__ == "__main__":
    main()