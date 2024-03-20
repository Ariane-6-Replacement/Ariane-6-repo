import numpy as np
import trajectory.sat_math_funcs as sm
import plotting_functions as pf
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

g = 9.81 # [m/s^2]
T = 8e6# thrust [N]
ISP = 400 # seconds
#m_prop = 565e3 # [kg]
initial_prop = 565e3
landing_fraction = 0
m_prop = (1-landing_fraction)*initial_prop
#M0 = 565e3 # mass [kg]
#psi = T/M0*g #thrust load 
Re = 6800e3 # [m]


v0 = 0.1
psi0 = 10*np.pi/180 # pitchover angle 
theta0 = 0
h0 = 0

y = [v0,psi0,theta0,h0 ]
    
def pressure(h):
        #Taken from https://www.grc.nasa.gov/www/k-12/airplane/atmosmet.html
        
        if h < 11000:
            T = 15.04 - 0.00649 * h
            p = 101.29 * ((T+273.1)/288.08)**5.256
        
        if h > 25000:
            T = -131.21 + 0.00299 * h
            p = 2.488 * ((T+273.1)/216.6)**(-11.388)
            
        else:
            T = -56.46
            p = 22.65 * np.exp(1.73 - 0.000157 * h)

           
        rho = p / (0.2869 * (T + 273.1))
       
        return rho



def odes(t,y,m_prop,Thrust,ISP,lf):
    #T = Thrust
    rho0 = 1 # [kg/m^3]
    Re = 6800e3 # [m]
    g0 = 9.81 # [m/s]
    m_dot = Thrust/(ISP*9.81) #[kg/s]
   
    # m_dot = -5656
    m_payload = 45e3 #[kg]
    m0 = m_payload + m_prop + lf*initial_prop
    TWR = 1.5 
    #Thrust = m0*9.81*TWR
    #print(Thrust)
    #TWR = Thrust/(m0*9.81)
    #print(TWR)
    tburn = (m_prop/m_dot)
    print(tburn)
    hturn = 10e3
    v = y[0]
 
    psi = y[1]
    theta = y[2]
    h = y[3]
    

    #g = g0/(1+h/Re)**2
    g = 9.81
    rho = pressure(h)
    Diamater = 5.4
    A = np.pi*(Diamater/4)**2
    Cd = 0.2
    D = 0.5 * rho * v**2 * A * Cd
    


    if t<tburn:
        m = m0 - m_dot*t
        T = Thrust
    else: 
        #print("burn over")
        m = m0 - m_dot * tburn
        T = 0
    if h <= hturn:
        psi_dot = 0
        #print(TWR,(T/(m*9.81)))
        v_dot = T / m - D/m - g
        h_dot = v
        theta_dot = 0
        
    else:
       
        
        #print("turning")
        phi_dot = g * np.sin(psi) / v
        v_dot = T/m- D/ m - g *np.cos(psi)
        h_dot = v*np.cos(psi)
        theta_dot = v*np.sin(psi) / (Re + h)
        psi_dot = phi_dot - theta_dot
    
    
    # m = m0 + m_dot*t
    # print(m)

    

    # phi_dot = g * np.sin(psi) / v
    # v_dot = T/m - g *np.cos(psi)
    # #print(T/m)
    # h_dot = v*np.cos(psi)
    # theta_dot = v*np.sin(psi) / (Re + h)
    # psi_dot = phi_dot - theta_dot
    
    
    return [v_dot, psi_dot, theta_dot,h_dot]


sol = solve_ivp(odes, [0, 1800], [v0,psi0,theta0,h0], args=(m_prop,T,ISP,landing_fraction),max_step=1,method='DOP853' )
print(sol)

theta = sol.y[2]
dr = theta*Re/1000 #[km] downrange
h = sol.y[3]/1000 # [km] altitude distance 
vel = sol.y[0]/1000
# print(dr)
# print(h)


def plot1():
    fig, axs = pf.creatfig(1,2,(20,5))
    axs[0].plot(dr,h)
    axs[0].set_xlabel("downrange [km]")
    axs[0].set_ylabel("altitude [km]")
    
    axs[1].plot(dr,vel)
    axs[1].set_xlabel("downrange [km]")
    axs[1].set_ylabel("velocity [km/s]")

    plt.show()
plot1()
