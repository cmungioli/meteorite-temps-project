<?xml version="1.0" encoding="utf-8"?>
<!-- Created by Leo: http://leoeditor.com/leo_toc.html -->
<leo_file xmlns:leo="http://leoeditor.com/namespaces/leo-python-editor/1.1" >
<leo_header file_format="2"/>
<globals/>
<preferences/>
<find_panel_settings/>
<vnodes>
<v t="martin.20191008111119.1"><vh>main code</vh>
<v t="martin.20191008111119.2"><vh>@clean ./Meteorite_Temps_Project.py</vh>
<v t="martin.20191008112746.1"><vh>docs</vh></v>
<v t="martin.20191008111119.3"><vh>Declarations</vh></v>
<v t="martin.20191008111119.4"><vh>input data</vh></v>
<v t="martin.20191008112508.1"><vh>do calc</vh></v>
<v t="martin.20191008112519.1"><vh>print results</vh></v>
<v t="martin.20191008112511.1"><vh>ice compare</vh></v>
<v t="martin.20191008111245.1"><vh>main</vh></v>
</v>
</v>
</vnodes>
<tnodes>
<t tx="martin.20191008111119.1"></t>
<t tx="martin.20191008111119.2"># -*- coding: utf-8 -*-
@others


@language python
@tabwidth -4
</t>
<t tx="martin.20191008111119.3">import math


</t>
<t tx="martin.20191008111119.4">def input_data():
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

    ruser = input("Enter the radius to which the heat conduction rate will be found. (m): ")
    
    return radiiList, thermcondList, kmultrList, k, Tcold, Thot, float(ruser), t



</t>
<t tx="martin.20191008111245.1">if __name__ == '__main__':
 
    radiiList, thermcondList, kmultrList, k, Tcold, Thot, ruser, t = input_data()

    q, Q, k = do_calc( radiiList, thermcondList, kmultrList, k, Tcold, Thot, ruser, t)
    
    print_results( q, Q)
    
    ice_compare( Q, Tcold, ruser)</t>
<t tx="martin.20191008112508.1">def do_calc(radiiList, thermcondList, kmultrList, k, Tcold, Thot, ruser, t):
    #Doing the calculations
    R = sum(radiiList)
    
    for x in range(1,len(radiiList)):
        kmultrListaddto = [(radiiList[x] * thermcondList[x])]
        kmultrList.extend( kmultrListaddto)
        
    k = (sum(kmultrList)) / R
    q = -1 * ((4 * math.pi * k * (Tcold - Thot)) / ((1 / ruser) - (1 / R))) 
    Q = q * t
    return q, Q, k</t>
<t tx="martin.20191008112511.1">def ice_compare( Q, Tcold, ruser):
    """calculate the mass of ice that would be melted by this level of heat.
    It then compares this with the mass of ice that could fit within the
    specified radius. Realistically the mass of ice that would melt under this
    heat is slightly too high, as only the outer layer of ice is exposed to
    the heat. However all this means is that if the answer is no, then the ice
    definitely couldn't melt"""
    m = Q / ((2108.0 * (273.15 - Tcold) + 334000.0))
    mice = (917.0 * (4.0 / 3.0) * math.pi * (ruser ** 3.0))
    if m &gt; mice:
        print("The ice cannot stay frozen within the radius specified")
    else:
        print("Ice with mass {} kgs would stay frozen at the radius specified"
              .format(m) )

</t>
<t tx="martin.20191008112519.1">def print_results(q, Q):
    #Printing the values
    print("The rate of heat conduction to the radius specified is: {} Joules/sec".format(q) )
    print("The total heat conducted to the radius specified is: {} Joules".format(Q) )

</t>
<t tx="martin.20191008112746.1">"""
Created on Thu Aug 15 10:41:02 2019

@author: Carlo Mungioli
"""
</t>
</tnodes>
</leo_file>
