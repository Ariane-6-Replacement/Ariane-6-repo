import numpy as np
import sat_math_funcs as sm
import plotting_functions as pf
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt


g = 9.81 # [m/s^2]
T = 1370e3# thrust [N]
ISP = 400 # seconds
m_prop = 140e3 # [kg]
#M0 = 565e3 # mass [kg]
#psi = T/M0*g #thrust load 
Re = 6800e3 # [m]


v0 = 100
psi0 = 1*np.pi/180 # pitchover angle 
theta0 = 0
h0 = 0

y = [v0,psi0,theta0,h0 ]


def odes(t,y,m_prop,Thrust,ISP):
    T = 2*Thrust
    Re = 6800e3 # [m]
    g0 = 9.81 # [m/s]
    m_dot = -Thrust/ISP #[kg/s]
    m_payload = 45e3 #[kg]
    m0 = m_payload + m_prop
    TWR = T/m0

    tburn = -(m_prop/m_dot)

    hturn = 1
    v = y[0]
 
    psi = y[1]
    theta = y[2]
    h = y[3]
    D = 0

    # g = g0/(1+h/Re)**2
    g = 9.81
    #rho = rho0 * np.exp(-h / hscale)
    D = 0
    # if t<tburn:
    #     m = m0 - m_dot*t
    #     T = Thrust
    # else: 
    #     print("burn over")
    #     m = m0 - m_dot * tburn
    #     T = 0
    # if h <= hturn:
    #     psi_dot = 0
    #     v_dot = T / m - D/m - g
    #     h_dot = v
    #     theta_dot = 0
        
    # else:
    #     ("turning")
    #     phi_dot = g * np.sin(psi) / v
    #     v_dot = T/m- D/ m - g *np.cos(psi)
    #     h_dot = v*np.cos(psi)
    #     theta_dot = v*np.sin(psi) / (Re + h)
    #     psi_dot = phi_dot - theta_dot
    m = m0 #+ m_dot*t
    print(m)

    
    phi_dot = g * np.sin(psi) / v
    v_dot = T/m - g *np.cos(psi)
    #print(T/m)
    h_dot = v*np.cos(psi)
    theta_dot = v*np.sin(psi) / (Re + h)
    psi_dot = phi_dot - theta_dot
    
    
    return [v_dot, psi_dot, theta_dot,h_dot]


sol = solve_ivp(odes, [0, 480], [v0,psi0,theta0,h0], args=(m_prop,T,ISP),max_step=1)

print(sol)

theta = sol.y[2]
dr = theta*Re/1000 #[km] downrange
h = sol.y[3]/1000 # [km] donwrange distance 
# print(dr)
# print(h)

def plot1():
    fig, axs = pf.creatfig(1,1,(20,6))
    axs.plot(dr,h)
    plt.show()
plot1()
