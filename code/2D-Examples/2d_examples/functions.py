import numpy as np

def dG(x,y, gamma=0.1, p=1/3, q=2/3):
  gamma, p, q = np.array([0.1]), np.array([1/3]), np.array([2/3])
  rows = np.empty((1,2), dtype=np.float64)
  xR = 2*(np.power(x,p) - np.power(y,q))*(p*np.power(x,p)*(gamma - 1/8*np.cos(4*x) + 1/8) - 1/4*x*(np.power(x,p) - np.power(y,q))*np.sin(4*x))/(x*(gamma - 1/8*np.cos(4*x) + 1/8)*(gamma + (np.power(x,p) - np.power(y,q))**2 - 1/8*np.cos(4*x) + 1/8))
  yR = -2*q*y**(q - 1)*(np.power(x,p) - np.power(y,q))/(gamma + (np.power(x,p) - np.power(y,q))**2 - 1/8*np.cos(4*x) + 1/8)
  return rows

def G(x,y, gamma=0.1, p=1/3, q=2/3):
  
  gamma, p, q = np.array([0.1]), np.array([1/3]), np.array([2/3])
  
  res = np.empty((1,1), dtype=np.float64)
  Y = np.cos(x)*np.sin(x)
  A = (np.power(x,p) - np.power(y,q))
  B = gamma + Y*Y
  res = np.log(1+A*A/B)
  return res

def h(x,y):
  res = np.empty((1,1), dtype=np.float64)
  res = x**2/(1+np.exp(1+y)) + y**4/(1+np.exp(1+x))
  return res

def dh(x,y):
  rows = np.empty((1,2), dtype=np.float64)
  xR = (
      2*x*(np.exp(x+ 1) + 1)**2
      - y**4*(np.exp(y + 1) + 1)*np.exp(x+ 1)
    )/(
      (np.exp(x+ 1) + 1)**2*(np.exp(y + 1) + 1)
      )
  
  yR = (
      -x**2*(np.exp(x+ 1) + 1)*np.exp(y + 1)
      + 4*y**3*(np.exp(y + 1) + 1)**2
    )/(
      
      (np.exp(x+ 1) + 1)*(np.exp(y + 1) + 1)**2
      )
  return rows