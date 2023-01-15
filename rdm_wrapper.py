import pandas as pd

#filler code, takes an outlet parameter list specified as a .csv file and turns it into the appropriate
#file type for running hec ras
def preprocess_dss(outlet_file):
    print("turning "+outlet_file+"into csv")

#filler code for running hec ras once the appropriate dss files have been written
def run_hec_ras():
    print("running hec-ras on temp outlet file")

#rdm_wrapper that takes in an outlet file, preprocesses it to get a specific configuration for a given
#uncertainty state and then sets the values for specific outlets chosen to be levers
#takes 2 inputs specific inputs:
#   *outlet_uncertainty_path is the path to a .csv file containing a list of outlets and their parameterizations
#   under different uncertainity scenarios (see file Outlet_treated_as_uncertainies.csv for example)
#   *outlet_uncertainty_configuration selects which column in outlet_uncertainty_path to use for parameterizing
#   this assumes that uncertainties will be more about configurations (leaky vs. non-leaky) instead of ranges of values
#it also takes an arbitrary number of named lever inputs, which overwrite the parameters for the named outlet
def rdm_wrapper(outlet_uncertainty_path, outlet_uncertainty_configuration, **levers):
    #reads in the preprocessed data - i think eventually we will want to connect this to air table
    outlet_uncertainty_data = pd.read_csv(outlet_uncertainty_path, index_col=0)[outlet_uncertainty_configuration]
    
    #loops through provided level arguments
    for key, value in levers.items():
        if(key in outlet_uncertainty_data):
            #overwrites the parameter for the specified outlet
            #currently only works for constant flow style outlet
            #additional preprocessing will be needed for later weirs and rating curves
            param_strings=outlet_uncertainty_data.at[key].split("; ")
            if param_strings[0]=="off":
                outlet_uncertainty_data.at[key]="off"
            elif param_strings[0]=="constant_flow_rate":
                outlet_uncertainty_data.at[key]=param_strings[0]+"; "+str(value)
            elif param_strings[0]=="rating_curve":
                if len(value)==len(param_strings[2].split(", ")):
                    outlet_uncertainty_data.at[key]=param_strings[0]+"; "+param_strings[1]+"; "+str(value)
                else:
                    outlet_uncertainty_data.at[key]="off"
            elif param_strings[0]=="lateral_weir":
                outlet_uncertainty_data.at[key]=param_strings[0]+"; "+param_strings[1]+"; "+str(value)+"; "+param_strings[3]+"; "+param_strings[4]
            
    #writes the processed data to a file
    outlet_uncertainty_data.to_csv("temp.csv")
    #reads the processed data file and turns it into the appropriate hec ras file type
    #the handoff doesn't necessairly need to involve a temp file I just thought it was a helpful demo
    preprocess_dss("temp.csv")
    #run hec-ras using the preprocessed file
    run_hec_ras()

    

x=rdm_wrapper("Outlet_treated_as_uncertainties.csv", "Uncertainty_2", Outlet_1=4, Outlet_7=15)
