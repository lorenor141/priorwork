# -*- coding: utf-8 -*-
"""
Structural Bioinformatics Exam - 2019/2020.
Protein practical.
"""
#Importing all relevant packages:
#Biopython
from Bio.PDB import *
from Bio.PDB.PDBParser import PDBParser

#numpy
import numpy as np
from numpy import * 
from numpy.linalg import svd, det 

#Matplotlib
import matplotlib.pyplot as plt

#'Random'
from random import *

#I didn't use all functions in every module but I imported everything (*)
# anyway in case of prospective modifications.

#Note: If top500H folder isn't in same directory, then the randint-funciton
# end-value ,len(list), will be equal to 0, and so this code will not run due to
# 'empty range for randrange() (0,0, 0) error


#Borrowed from teacher's solution (distance-histograms assignment) and modified a bit.
if __name__=="__main__":
    '''Iterate through and parse all files in a folder '''
    import glob #Filename pattern matching
    
    # Create a list of protein structures
    structure_list = []
    for index, fname in enumerate(glob.glob("top500H/*")):
        print(f"Parsing {fname}... ")
        p=PDBParser(QUIET=True) #Silences warnings
        try:
            #Extract structure and append to list
            s=p.get_structure("", fname)
            structure_list.append(s)
        except:
            #Skips unparsable files and print error code
            print(f"- ERROR in {fname}, therefor it has been skipped.")



def protein_aalist(s, aa):
    '''Goes through one protein and createst a list of amino acids from it '''
    list_of_aa = []
    for res in s[0].get_residues():
        if is_aa(res): #Tests object identity
            if res.get_resname() == aa:
                list_of_aa.append(res)
    return list_of_aa



def draw_aacid(list_of_aa):
    '''Randomly picks an amino acid from a list of amino acids '''
    aa = list_of_aa[randint(0, len(list_of_aa)-1)]
    return aa

def coordinates(aa):
    '''Extracts a list of amino acid sidechain atoms coordinates and 
    returns matrix of the list  '''
    list_of_coordinates = []
    #Excluding main chain atoms and hydrogens.
    for atom in aa.get_atoms():
        if atom.get_id() == 'N' or atom.get_id() == 'C' or atom.get_id() == 'O':
            continue #if main chain atoms, skip
            
        #The exclusion step was written like this due to Python's need 
        # for complete instructions on both sides of the logical operator
        if atom.element == 'H': 
            continue
         #Only instance H appears in 'Name' column but not H 'Element' in pdb
        #is with OH-atoms which are of 'O' element which is excluded anyway.
        else:
            list_of_coordinates.append(atom.get_coord()) #Coordinates as numpy array
    return matrix(list_of_coordinates).T #Returns the transpose of the matrix


#Following function is also borrowed from teacher's solutions. A combination of
#center and sup functions with slight modifications:
def rmsd(x, y):
    #Calculating center of mass of x and y
    center_of_mass_x = x.sum(1)/x.shape[1] 
    center_of_mass_y = y.sum(1)/y.shape[1] 
    
    #Center x and y
    centered_x = x - center_of_mass_x
    centered_y = y - center_of_mass_y
    
    #Correlation matrix
    x_transposed = centered_x.T
    R = centered_y*x_transposed
    
    #SVD of correlation matrix
    v, s, w_transposed = svd(R) 
    
    #Rotation matrix
    w = w_transposed.T
    v_transposed = v.T
    u = w*v_transposed
    
    #Checking roto-reflection
    if round(det(u)) == -1:
        z = diag((1, 1, -1))
        u = w*z*v_transposed
    
    #Rotating y by applying u
    y_rotated = u*centered_y
    
    #Calculating RMSD from coordinates
    rmsd = sqrt((1/x.shape[1])*np.linalg.norm(centered_x - y_rotated)**2)
    
    return rmsd, u


def list_of_rmsd(list_of_protein, length_of_list, aa):
    '''Outputs a list of RMSDs given a randomly-chosen amino acid from 
    different proteins '''    
    list_of_rmsd = []
    i = 0
    #The 'length_of_list' parameter could have been replaced with just 1000 as 
    #per task but this is to make the function more general and applicable to 
    #other sets of data of same format.    
    while i < length_of_list: #Could have been 'while i<=1000'
        #Picks 2 proteins by random from list of proteins        
        random_variable1 = randint(0, len(list_of_protein)-1)
        random_variable2 = randint(0, len(list_of_protein)-1)
        
        #Checks protein origin
        if random_variable1 != random_variable2: #if from different proteins, then move on
            random_protein1 = list_of_protein[random_variable1]
            random_protein2 = list_of_protein[random_variable2]
            
        #Initiates lists for amino acid
        aa_list1 = protein_aalist(random_protein1, aa)
        aa_list2 = protein_aalist(random_protein2, aa)
        
        #If any list is empty, then 'empty range' error
        if len(aa_list1)==0 or len(aa_list2)==0:
            continue
        
        #Picks random amino acid from lists
        aa1 = draw_aacid(aa_list1)
        aa2 = draw_aacid(aa_list2)
        
        #Extracts coordinates
        aa1_coords = coordinates(aa1)
        aa2_coords = coordinates(aa2)
        
        if shape(aa1_coords) != shape(aa2_coords): #If similar, list will not output anything
            continue
        
        #Calculates RMSD from coordinates and appends to list of RMSD
        rmsd_calculated = rmsd(aa1_coords, aa2_coords)[0]
        list_of_rmsd.append(rmsd_calculated)
        
        i+=1    
    return list_of_rmsd


#Borrowed from teacher's solutions, distance histogram exercise
def hist(rlist, aa):
    '''Creates and saves histograms as .png-file '''
    #Histogram of the data
    n, bins, patches = plt.hist(rlist, 20, density=True, 
        facecolor='b')

    #Labels, if density=TRUE then y-axis ='Probability), otherwise 'Frequency'
    plt.xlabel('RMSD (in Angstroms)')
    plt.ylabel('Probability')
    plt.title('Distance histogram of %s' % aa)
    
    #x and y limits of plot
    plt.xlim(0, 1.5)
    plt.ylim(0, 40)
    plt.grid(True)
    
    #Save as .png file
    plt.savefig("dist_hist_"+aa+".png")
    
    #Clear canvas for next plot
    plt.clf()

#Finally, we calculate RSMD and print out histograms for all of the 18 amino 
# acids, 'ALA' and 'GLY' excluded becauase they're too small, as per task:
amino_acids = ['ARG', 'ASN', 'ASP', 'CYS', 'GLN', 'GLU', 'HIS', 'ILE', 'LEU', 
               'LYS', 'MET', 'PHE', 'PRO', 'SER', 'THR', 'TRP', 'TYR', 'VAL']
for aa in amino_acids:
    final_list = list_of_rmsd(structure_list, 1000, aa) #1000 pairs as per task
    hist(final_list, aa )#Plotting histogram of RMSDs
    #Calculate Mean and Standard Deviation (std)
    #This part was also taken from teacher's solutions without any modifications.
    print("\n")
    l = len(final_list)
    print("Count for %s: %i" % (aa, l))
    m = np.mean(final_list) #Unsure about difference between np.mean and mean
    print("Mean for %s: %.2f" % (aa, m))
    sd = np.std(final_list) #Same for this
    print("Std. dev.  for %s: %.2f" % (aa, sd))
    m2 = max(final_list)
    print("Maximum rmsd for %s: %.2f" % (aa, m2))
    #So, I get different results when using 'np.mean' and 'mean', same for Std.
    # and I'm unsure of the difference, but I chose to go with np.mean/np.std
    # because the teacher's solutions did so, as well.
    #The calculation part was basically copied from teacher but I tried 
    # experimenting with it without luck.
