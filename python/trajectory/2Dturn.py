import numpy as np
import sat_math_funcs as sm
from scipy.integrate import odeint
from scipy.integrate import solve_ivp

print("hellow")
# T = 20e6# thrust [N]
# ISP = 400 # seconds
# m_prop = 140e3 # [kg]
# M0 = 565e3 # mass [kg]
# psi = T/M0*g #thrust load 



# v0 = 0
# psi0 = 1*np.pi/180
# theta0 = 0
# h0 = 0

# y = [v0,psi0,theta0,h0 ]


# def odes(t,y,m_prop,Thrust,ISP):
    
#     Re = 6800e3 # [m]
#     g0 = 9.81 # [m/s]
#     m_dot = -Thrust/ISP #[kg/s]
#     m_payload = 45e3 #[kg]
#     m0 = m_payload + m_prop
#     tburn = m_prop/m_dot
#     hturn = 1000
#     v = y[0]
#     psi = y[1]
#     theta = y[2]
#     h = y[3]
#     D = 0

#     g = g0/(1+h/Re)**2
#     #rho = rho0 * np.exp(-h / hscale)
#     D = 0
#     if t<tburn:
#         m = m0 - m_dot*t
#         T = Thrust
#     else: 
#         m = m0 - m_dot * tburn
#         T = 0
#     if h <= hturn:
#         psi_dot = 0
#         v_dot = T / m - D/m - g
#         h_dot = v
#     else:
#         phi_dot = g * np.sin(psi) / v
#         v_dot = T/m- D/ m - g *np.cos(psi)
#         h_dot = v*np.cos(psi)
#         theta_dot = v*np.sin(psi) / (Re + h)
#         psi_dot = phi_dot - theta_dot
#     return [v_dot, psi_dot, theta_dot,h_dot]


# #solutions = solve_ivp(odes, [0, 180], [v0,psi0,theta0,h0], args=(m_prop,T,ISP))