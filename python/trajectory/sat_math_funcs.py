import numpy as np
from sgp4.api import Satrec
from sgp4.api import jday
from pathlib import Path
import time
from statistics import mean 


def timerange(startime,interationhours=None):
    year = startime[0]
    month = startime[1]
    day = startime[2]
    hour_i = startime[3]
    minute = startime[4]
    second= startime[5]
    jd_i, fr_i = jday(year, month, day, hour_i, minute, second)
    if interationhours is None:
        timesets = (jd_i, fr_i)
    else:
        hour_f = hour_i + interationhours
        jd_f, fr_f = jday(year, month, day, hour_f, minute, second)
        timesets = [(jd_i, fr_i), (jd_f, fr_f)]
    return timesets

def norm(r):
    return np.linalg.norm(r) 

def norm_array(r):
    r_norm = np.empty([len(r),1])
    for i in range(len(r)):
        r_norm[i] = norm(r[i])
    return r_norm

def cart_to_kep(r,v,doprint,radordeg):

    mu = 3.986004418*10**5
    h = np.cross(r,v)
    e = (np.cross(v,h))/mu - (r/np.linalg.norm(r))
    i = np.arccos(h[2]/np.linalg.norm(h))
    a = 1/((2/np.linalg.norm(r)) - (((np.linalg.norm(v))**2) / mu))
    n = np.cross([0,0,1],h)
    

    omega = np.arctan2(n[1]/np.linalg.norm(n),n[0]/np.linalg.norm(n))

    N_unit = n/np.linalg.norm(n)
    r_unit = r/np.linalg.norm(r)
    e_unit = e/np.linalg.norm(e)
    if np.dot(np.cross(N_unit,e),h)>0:
        wsign = 1
    else:
        wsign = -1
    if np.dot(np.cross(e,r),h)>0:
        tsign = 1
    else:
        tsign = -1    
    
    argper = wsign * np.arccos(np.dot(e_unit,N_unit))
    tanom = tsign* np.arccos(np.dot(r_unit,e_unit))
    
    e_mag = np.linalg.norm(e)
    i_deg = i*(180/np.pi)
    omega_deg =  omega*(180/np.pi)
    tanom_deg = tanom*(180/np.pi)
    argper_deg = argper*(180/np.pi)
    
    if radordeg == "rad":
        kep_elements = [e_mag,i,a,omega,tanom,argper]
    else:
        kep_elements = [e_mag,i_deg,a,omega_deg,tanom_deg,argper_deg]
    if doprint:
        print("e= " + str(kep_elements[0])+"\n"
            "i = " + str(kep_elements[1]) +"\n"
            "a = " + str(kep_elements[2])+ "\n"
            "omega = " + str(kep_elements[3]) +"\n"
            "True anomoly = " + str(kep_elements[4])+ "\n"
            "arg of peri = " + str(kep_elements[5]) +"\n"
    )
    
    
    return  kep_elements  # e[0] i[1] a[2] omega[3] tanom[4] argper[5]

def kep_to_cart(e,i,a,omega,Truanom,argperi):
    w = argperi
    mu = 3.986004418*10**5
 
    #E = 2* np.arctan(np.tan(Truanom/2)* np.sqrt((1-e)/(1+e))) # go and fix the arctan sometime
    E = 2* np.arctan2((np.sin(Truanom/2)*np.sqrt(1-e)),(np.cos(Truanom/2)*np.sqrt(1+e)))
    #print("Eccentric anomly: " + str(E))
    #M = E - e*np.sin(E)
    alt = a*(1-e*np.cos(E))
    h = np.sqrt(mu*alt*(1-e**2))
    p = a*(1-e**2)
    ox = alt * np.cos(Truanom)
    oy = alt * np.sin(Truanom)
    odotx = (np.sqrt(mu*a)/alt) * (-1*np.sin(E)) 
    odoty = (np.sqrt(mu*a)/alt) * (np.sqrt(1-e**2)*np.cos(E))
    
   
    #rx = ox*(np.cos(w)*np.cos(omega) - np.sin(w)*np.cos(i)*np.sin(omega)) - oy*( np.sin(w) * np.sin(omega) + np.cos(w)*np.cos(i)*np.sin(omega))
    rx = alt*(np.cos(omega)*np.cos(Truanom+w) - np.sin(omega)*np.sin(w+Truanom)*np.cos(i)) # I dont know why this one works and the other doesnt 
    ry = ox*(np.cos(w)*np.sin(omega) + np.sin(w)*np.cos(i)*np.cos(omega)) + oy*( np.cos(w) * np.cos(omega)*np.cos(i) - np.sin(w)*np.sin(omega))
    rz = ox*(np.sin(w)*np.sin(i)) + oy*(np.cos(w) * np.sin(i))

    #vx = odotx*(np.cos(w)*np.cos(omega) - np.sin(w)*np.cos(i)*np.sin(omega)) - odoty*( np.sin(w) * np.sin(omega) + np.cos(w)*np.cos(i)*np.sin(omega))
    vx = ((rx*h*e)/(alt*p))*np.sin(Truanom) - h/alt*(np.cos(omega)*np.sin(Truanom+w) + np.sin(omega)*np.cos(w+Truanom)*np.cos(i))
    vy = odotx*(np.cos(w)*np.sin(omega) + np.sin(w)*np.cos(i)*np.cos(omega)) + odoty*( np.cos(w) * np.cos(omega)*np.cos(i) - np.sin(w)*np.sin(omega))
    vz = odotx*(np.sin(w)*np.sin(i)) + odoty*(np.cos(w) * np.sin(i))

    r = [rx,ry,rz]
    v = [vx,vy,vz]
    return r,v

def sgp4iterate(sat,timestep_sec,interationtime_sec):
    
    timestep_jd = timestep_sec/86400
    interation_steps= int(interationtime_sec/timestep_sec)
    frac = np.empty(interation_steps)
    jd = np.empty(interation_steps)
    #jd.fill(timerange(startime)[0])
    jd.fill(sat.jdsatepoch)
    time = sat.jdsatepochF
    for num in range(interation_steps):
        time = time + timestep_jd
        if time<1:
            frac[num] = time
        else: 
            time = time-1
            frac[num] = time-1
            jd[num] = jd[num-1]+1
            #print(jd[num], frac[num])


    e, r, v = sat.sgp4_array(jd, frac)
    iter_range = np.linspace(0, interation_steps, interation_steps)
    return r,v,iter_range

def kep_iterate(sat,intersec,timestep,startime,toarray):
    r,v,iter_range = sgp4iterate(sat,intersec,timestep,startime)
    keparray = np.empty([intersec,6])
    for j in range(intersec):
        keparray[j] = cart_to_kep(r[j],v[j],False,"deg")
    
    e = keparray[:, [0]]
    i = keparray[:, [1]]
    a = keparray[:, [2]]
    RAAN = keparray[:, [3]]
    Truanom = keparray[:, [4]]
    argper = keparray[:, [5]]
    
    if toarray:
        return keparray
    else:
        return e,i,a,RAAN,Truanom,argper

def kep_to_cart(e,i,a,omega,Truanom,argperi):
    w = argperi
    mu = 3.986004418*10**5
 
    #E = 2* np.arctan(np.tan(Truanom/2)* np.sqrt((1-e)/(1+e))) # go and fix the arctan sometime
    E = 2* np.arctan2((np.sin(Truanom/2)*np.sqrt(1-e)),(np.cos(Truanom/2)*np.sqrt(1+e)))
    #print("Eccentric anomly: " + str(E))
    #M = E - e*np.sin(E)
    alt = a*(1-e*np.cos(E))
    h = np.sqrt(mu*alt*(1-e**2))
    p = a*(1-e**2)
    ox = alt * np.cos(Truanom)
    oy = alt * np.sin(Truanom)
    odotx = (np.sqrt(mu*a)/alt) * (-1*np.sin(E)) 
    odoty = (np.sqrt(mu*a)/alt) * (np.sqrt(1-e**2)*np.cos(E))
    
   
    #rx = ox*(np.cos(w)*np.cos(omega) - np.sin(w)*np.cos(i)*np.sin(omega)) - oy*( np.sin(w) * np.sin(omega) + np.cos(w)*np.cos(i)*np.sin(omega))
    rx = alt*(np.cos(omega)*np.cos(Truanom+w) - np.sin(omega)*np.sin(w+Truanom)*np.cos(i)) # I dont know why this one works and the other doesnt 
    ry = ox*(np.cos(w)*np.sin(omega) + np.sin(w)*np.cos(i)*np.cos(omega)) + oy*( np.cos(w) * np.cos(omega)*np.cos(i) - np.sin(w)*np.sin(omega))
    rz = ox*(np.sin(w)*np.sin(i)) + oy*(np.cos(w) * np.sin(i))

    #vx = odotx*(np.cos(w)*np.cos(omega) - np.sin(w)*np.cos(i)*np.sin(omega)) - odoty*( np.sin(w) * np.sin(omega) + np.cos(w)*np.cos(i)*np.sin(omega))
    vx = ((rx*h*e)/(alt*p))*np.sin(Truanom) - h/alt*(np.cos(omega)*np.sin(Truanom+w) + np.sin(omega)*np.cos(w+Truanom)*np.cos(i))
    vy = odotx*(np.cos(w)*np.sin(omega) + np.sin(w)*np.cos(i)*np.cos(omega)) + odoty*( np.cos(w) * np.cos(omega)*np.cos(i) - np.sin(w)*np.sin(omega))
    vz = odotx*(np.sin(w)*np.sin(i)) + odoty*(np.cos(w) * np.sin(i))

    r = [rx,ry,rz]
    v = [vx,vy,vz]
    return r,v

def gravity_accel(r):
    mu = 3.986004418*10**5
    r_norm = norm(r)
    r = np.array(r)
    A = (-mu/r_norm**3)*r
    A_mag = norm(A)
    return A,A_mag

def J2_accel(r):

    x = r[0]
    y = r[1]
    z = r[2]
    r_norm = norm(r)
    R = 6378.1370
    mu = 3.986004418*10**5  
    J2 =  1.083*10**-3
    f = np.zeros(3)
    f[0] = (-3*mu*J2/2 )*(R**2/r_norm**5)*x*(1-5*z**2/r_norm**2)
    f[1] = (-3*mu*J2/2 )*(R**2/r_norm**5)*y*(1-5*z**2/r_norm**2)
    f[2] = (-3*mu*J2/2 )*(R**2/r_norm**5)*z*(1-5*z**2/r_norm**2)
    return f


def Euler_integrator(r0,v0,timestep,stop_time):
     
  
    interation_steps = int(stop_time/timestep)
    
    r = np.zeros([interation_steps,3])
    v = np.zeros([interation_steps,3])
    r[0] = r0
    v[0] = v0
    for i in range (0,interation_steps-1):
       r[i+1] = r[i]  + [x*timestep for x in v[i]]
       v[i+1] = v[i] + [x*timestep for x in gravity_accel(r[i])[0]]
    return r,v

def Euler_integrator_timed(r0,v0,timestep,stop_time):
    
    total_time = time.process_time()
    interation_steps = int(stop_time/timestep)
    
    r = np.zeros([interation_steps,3])
    v = np.zeros([interation_steps,3])
    t = np.zeros(interation_steps)
    r[0] = r0
    v[0] = v0
    for i in range (0,int(stop_time/timestep)-1):
       start_time = time.process_time()
       r[i+1] = r[i]  + [x*timestep for x in v[i]]
       v[i+1] = v[i] + [x*timestep for x in gravity_accel(r[i])[0]] + [x*timestep for x in J2_accel(r[i])]
       t[i] = (time.process_time() - start_time)*1000
    total_time = time.process_time()-total_time
    return r,v,mean(list(t)),total_time

def RMS(data):
    sum = 0
    
    for i in range(len(data)):
       sum += data[i]**2 
    
    result = np.sqrt(sum/len(data))
    return result

def to_meters_list(input_tuple):
    
    list1 = list(tuple(i * 1000 for i in input_tuple))
    list1 = [float(i) for i in list1]
    return list1


def differance_data(a,b):
    c = a-b
    return c



def SRP_accel(r):
    r_esun = [ -3.224662310827732*10**7, -1.319105127190110*10**8, -5.718142004737785*10**7]
    #r_esun = r_sun
    r_esat = np.array(r)
    fa = 1
    Re = 6378.1370 #km 
    Rsun = 696340 #km
    e_s = r_esun/norm(r_esun)
    c = 299792458 # m/s
    Br = 0.02 #m**2/kg
    W = 1361 # W/m**2
    pe = W*e_s/c
    r_sunsat = r_esat - r_esun
    r_ps = e_s*(np.dot(e_s,r_esat))
    r_ep = r_esat - r_ps
    hg = norm(r_ep) - Re
    Rp = norm(r_ps)*Rsun/norm(r_sunsat)
    eta = hg/Rp

    fg = 1 - np.arccos(eta)/np.pi + eta*np.sqrt(1-eta**2)/np.pi
    
    if eta < -1:
        f = [0,0,0]
    elif -1<= eta < 1:
        f = -fg*fa*Br*pe*e_s
    elif 1<= eta:
        f = -Br*pe
    return f

def Euler_integrator_J2(r0,v0,timestep,stop_time):
     
  
    interation_steps = int(stop_time/timestep)
    
    r = np.zeros([interation_steps,3])
    v = np.zeros([interation_steps,3])
    r[0] = r0
    v[0] = v0
    for i in range (0,interation_steps-1):
       r[i+1] = r[i]  + [x*timestep for x in v[i]] 
       v[i+1] = v[i] + [x*timestep for x in gravity_accel(r[i])[0]] + [x*timestep for x in J2_accel(r[i])] 
    return r,v

def Euler_integrator_SRP(r0,v0,timestep,stop_time):
     
  
    interation_steps = int(stop_time/timestep)
    
    r = np.zeros([interation_steps,3])
    v = np.zeros([interation_steps,3])
    r[0] = r0
    v[0] = v0
    for i in range (0,interation_steps-1):
       r[i+1] = r[i]  + [x*timestep for x in v[i]] 
       v[i+1] = v[i] + [x*timestep for x in gravity_accel(r[i])[0]] + [x*timestep for x in SRP_accel(r[i])] 
    return r,v

def cart_to_latlon(r):
    x = r[0]
    y = r[1]
    z = r[2]
    r_xy = np.sqrt(x**2 + y**2)
    # r_rot  - r


    
    lon = np.arctan2(y/r_xy,x/r_xy) * 180/np.pi
    # if lon > np.pi:
    #     lon = np.arctan2(y,x) - 2*np.pi

    lat = np.arcsin(z/norm(r)) * 180/np.pi
    #array = np.array[norm(r),lon,lat]
    return norm(r),lon,lat

def cart_to_latlon_array(r):
    r_lat = np.empty([len(r),3])
    for i in range(len(r)):
        r_lat[i] = cart_to_latlon(r[i])
    
    # print(r_lat[:, [1]])
    # print("unwrapped")
    # r_lat[:, [1]] = np.degrees(np.unwrap(np.radians(r_lat[:, [1]])))
    # print(r_lat[:, [1]])

    return r_lat

def J2_Mag(r0,v0,timestep,stop_time):
     
    interation_steps = int(stop_time/timestep)
    
    r = np.zeros([interation_steps,3])
    v = np.zeros([interation_steps,3])
    j_mag = np.zeros([interation_steps,1]) 
    r[0] = r0
    v[0] = v0
    j_mag[0] = norm(J2_accel(r0))
    for i in range (0,interation_steps-1):
       j_mag[i+1] = norm(J2_accel(r[i]))
       r[i+1] = r[i]  + [x*timestep for x in v[i]] 
       v[i+1] = v[i] + [x*timestep for x in gravity_accel(r[i])[0]] + [x*timestep for x in J2_accel(r[i])] 
    return j_mag

def SRP_Mag(r0,v0,timestep,stop_time):
     
    interation_steps = int(stop_time/timestep)
    
    r = np.zeros([interation_steps,3])
    v = np.zeros([interation_steps,3])
    srp_mag = np.zeros([interation_steps,1]) 
    r[0] = r0
    v[0] = v0
    srp_mag[0] = norm(SRP_accel(r0))
    for i in range (0,interation_steps-1):
       srp_mag[i+1] = norm(SRP_accel(r[i]))
       r[i+1] = r[i]  + [x*timestep for x in v[i]] 
       v[i+1] = v[i] + [x*timestep for x in gravity_accel(r[i])[0]] + [x*timestep for x in SRP_accel(r[i])] 
    return srp_mag

def latlonhtoxyzwgs84(lat,lon,h):


    a=6378137.0             #radius a of earth in meters cfr WGS84
    b=6356752.3             #radius b of earth in meters cfr WGS84
    e2=1-(b**2/a**2)
    latr=lat/90*0.5*np.pi      #latitude in radians
    lonr=lon/180*np.pi         #longituede in radians
    Nphi=a/(1-e2*np.sin(latr)**2)**0.5
    x=(Nphi+h)*np.cos(latr)*np.cos(lonr)
    y=(Nphi+h)*np.cos(latr)*np.sin(lonr)
    z=(b**2/a**2*Nphi+h)*np.sin(latr)
    return([x,y,z])