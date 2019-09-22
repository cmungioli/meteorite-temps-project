# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 10:41:02 2019

@author: Carlo Mungioli
"""

def MeteoriteTemps():
    import math
    
    
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
        yesno = input("Add another layer? (y/n): ")
        if yesno == "y" or yesno == "yes" or yesno == "Y":
            yesno = True
        elif yesno == "n" or yesno == "no" or yesno == "N":
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
        
    
    if yesno == False:
        #The user can specify where exactly in the meteorite q will be found
        radiusentered = False
        while radiusentered == False:
            try:
                ruser = float(input("Enter the radius to which the heat conduction rate will be found. (m): "))
            except:
                print("Error: unexpected input entered")
                continue
            radiusentered = True
        
        
        #Doing the calculations
        R = sum(radiiList)
        for x in range(1,len(radiiList)):
            kmultrListaddto = [(radiiList[x] * thermcondList[x])]
            kmultrList.extend(kmultrListaddto)
            del kmultrListaddto
        k = (sum(kmultrList)) / (R)
        q = -1 * ((4 * math.pi * k * (Tcold - Thot)) / ((1 / ruser) - (1 / R))) 
        Q = q * t
        
        
        #Printing the values
        print("\nThe rate of heat conduction to the radius specified is:",q,"Joules/sec")
        print("The total heat conducted to the radius specified is:",Q,"Joules")
    

    #This section calculates the mass of ice that would be melted by this level of heat.
    #It then compares this with the mass of ice that could fit within the specified radius.
    #Realistically the mass of ice that would melt under this heat is slightly too high,
    #as only the outer layer of ice is exposed to the heat
    #However all this means is that if the answer is no, then the ice definitely couldn't melt
    m = Q / ((2108 * (273.15 - Tcold) + 334000))
    mice = (917 * (4 / 3) * math.pi * (ruser ** 3))
    if m > mice:
        print("\nThe ice cannot stay frozen within the radius specified")
        return
    else:
        print("\nA clump of ice with mass",m,"kgs would stay frozen at the radius specified")
        
MeteoriteTemps()
