# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 10:41:02 2019

@author: Carlo Mungioli
"""
import math
import sys


def input_data():
    #This section creates lists for the radii and thermal conductivities of each layer.
    #It also specifies necessary values such as temperatures and lengths of time.
    #We have multiple try/except blocks so we can retry inputting values if the initial entry is invalid
    radiusentered = False
    thermcondentered = False
    thotentered = False
    tcoldentered = False
    timeentered = False
    while radiusentered == False:
        try:
            radiiList = [float(input("Radius of first layer (m): "))]
        except:
            print("Error: unexpected input entered")
            continue
        radiusentered = True
    while thermcondentered == False:
        try:
            thermcondList = [float(input("Thermal conductivity of first layer (W m^-1 K^-1): "))]
        except:
            print("Error: unexpected input entered")
            continue
        thermcondentered = True
    while thotentered == False:
        try:
            Thot = float(input("Temperature of outer surface (K): "))
        except:
            print("Error: unexpected input entered")
            continue
        thotentered = True
    while tcoldentered == False:
        try:
            Tcold = float(input("Temperature of core (K): "))
        except:
            print("Error: unexpected input entered")
            continue
        tcoldentered = True
    while timeentered == False:
        try:
            t = float(input("Length of time of heat pulse (s): "))
        except:
            print("Error: unexpected input entered")
            continue
        timeentered = True
    kmultrList = [(radiiList[0] * thermcondList[0])]

    yesnoentered = False
    while yesnoentered == False:
        yesnostr = input("Add another layer? (y/n): ")
        if yesnostr == "y" or yesnostr == "yes" or yesnostr == "Y":
            yesno = True
        elif yesnostr == "n" or yesnostr == "no" or yesnostr == "N":
            yesno = False
        else:
            print("Error: please enter yes or no")
            continue
        yesnoentered = True
    while yesno == True:
        #If the user wants to add another layer, it creates a new list to extend the old list with, then deletes them.
        #This is the case with both the radii list and the thermal conductivity lists.
        #This is because floating point numbers cannot be appended to lists directly.
        #At the end, it asks again if the user would like to add another layer.
        #This allows the user to add as many layers as possible.
        radiusentered = False
        thermcondentered = False
        while radiusentered == False:
            try:
                radiiListaddto = [float(input("Radius of the next layer (m): "))]
            except:
                print("Error: unexpected input entered")
                continue
            radiusentered = True
        while thermcondentered == False:
            try:
                thermcondListaddto = [float(input("Thermal conductivity of next layer (W m^-1 K^-1): "))]
            except:
                print("Error: unexpected input entered")
                continue
            thermcondentered = True
        radiiList.extend(radiiListaddto)
        thermcondList.extend(thermcondListaddto)
        del radiiListaddto
        del thermcondListaddto
        yesnoentered = False
        while yesnoentered == False:
            yesno = input("Add another layer? (y/n): ")
            if yesno == "y" or yesno == "yes" or yesno == "Y":
                yesno = True
            elif yesno == "n" or yesno == "no" or yesno == "N":
                yesno = False
            else:
                print("Error: please enter yes or no")
                continue
            yesnoentered = True

    ruser = input("Enter the radius to which the heat conduction rate will be found. (m): ")
    
    return radiiList, thermcondList, kmultrList, Tcold, Thot, float(ruser), t



def test_dataset():
    radiiList
    thermcondList
    kmultrList
    Tcold = 200.0
    Thot = 2500.0
    ruser
    t
    
    return radiiList, thermcondList, kmultrList, Tcold, Thot, float(ruser), t
def file_data( fname):
    """read data from file. file format is csv:
    #comment first line
    4 fields, giving k, Tcold, Thot, ruser
    n lines of 3 fields, giving radii, thermcond, kmultr 
    """
    with open( fname, 'rt') as fp:
        ln = fp.readline() #comment line, ignore
        k, Tcold, Thot, ruser, t = fp.readline().split(',')
        radiiList, thermcondList, kmultrList = [],[],[]
        for ln in fp.readlines():
            lin = ln.split(',')
            radiiList.append( lin[0].strip() )
            thermcondList.append( lin[1].strip() )
            kmultrList.append( lin[2].strip() )

    return radiiList, thermcondList, kmultrList, Tcold, Thot, float(ruser), t
def do_calc(radiiList, thermcondList, kmultrList, Tcold, Thot, ruser, t):
    """Doing the calculations"""
    R = sum(radiiList)
    
    for x in range(1,len(radiiList)):
        kmultrListaddto = [(radiiList[x] * thermcondList[x])]
        kmultrList.extend( kmultrListaddto)
        
    k = (sum(kmultrList)) / R
    q = -1 * ((4 * math.pi * k * (Tcold - Thot)) / ((1 / ruser) - (1 / R))) 
    Q = q * t
    return q, Q, k
def print_results(q, Q):
    #Printing the values
    print("The rate of heat conduction to the radius specified is: {} Joules/sec".format(q) )
    print("The total heat conducted to the radius specified is: {} Joules".format(Q) )

def ice_compare( Q, Tcold, ruser):
    """calculate the mass of ice that would be melted by this level of heat.
    It then compares this with the mass of ice that could fit within the
    specified radius. Realistically the mass of ice that would melt under this
    heat is slightly too high, as only the outer layer of ice is exposed to
    the heat. However all this means is that if the answer is no, then the ice
    definitely couldn't melt"""
    m = Q / ((2108.0 * (273.15 - Tcold) + 334000.0))
    mice = (917.0 * (4.0 / 3.0) * math.pi * (ruser ** 3.0))
    if m > mice:
        print("The ice cannot stay frozen within the radius specified")
    else:
        print("Ice with mass {} kgs would stay frozen at the radius specified"
              .format(m) )

if __name__ == '__main__':
    
    if len(sys.argv) > 1:
        if os.path.isfile( sys.argv[1]):
            radiiList, thermcondList, kmultrList, Tcold, Thot, ruser, t = file_data()
        elif sys.argv[1] == '-t':
            radiiList, thermcondList, kmultrList, Tcold, Thot, ruser, t = test_dataset()
        else:
            exit()
    else:
        radiiList, thermcondList, kmultrList, Tcold, Thot, ruser, t = input_data()

    q, Q, k = do_calc( radiiList, thermcondList, kmultrList, Tcold, Thot, ruser, t)
    
    print_results( q, Q)
    
    ice_compare( Q, Tcold, ruser)


