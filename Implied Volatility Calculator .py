#!/usr/bin/env python
# coding: utf-8

# Note the implied volatility of a call and a put are the same

# In[1]:


from scipy.stats import norm
import numpy as np


# In[2]:


class ImpliedVolatility:
    
    '''
    n    = number of newton-raphson interations
    type = 'put' or 'call'
    v    = option price
    r    = risk free rate
    s    = price of underlying
    k    = strike price
    t    = time to maturity
    '''
    
    def __init__(self,type,v,r,s,k,t):
        self.type = type.strip().lower()
        self.v    = v
        self.r    = r
        self.s    = s
        self.k    = k
        self.t    = t
    
    def vega(self,sigma):
        d1 = (np.log(self.s/self.k)+(self.r-sigma*sigma*0.5)*np.sqrt(self.t))/(sigma*np.sqrt(self.t))
        return self.s*norm.pdf(d1)*np.sqrt(self.t)
    
    def BSCall(self,sigma):
        d1 = (np.log(self.s/self.k)+(self.r-sigma*sigma*0.5)*np.sqrt(self.t))/(sigma*np.sqrt(self.t))
        d2 = d1 - sigma*np.sqrt(self.t)
        return self.s*norm.cdf(d1) - np.exp(-self.r*self.t)*self.k*norm.cdf(d2)
    
    def Put2CallConverter(self):
        '''
        calculates price of equivalent call option via put-call parity
        '''
        self.v    = self.v - self.k*np.exp(-self.r*self.t) + self.s
        self.type ='call'
        
    def NewtonCalculation(self,n=10):
        '''
        n = number of Newton-Raphson iterations
        '''
        if self.type == 'put':
            self.Put2CallConverter()
        
        if n == 0:
            return 1
        return self.NewtonCalculation(n-1) - (self.BSCall(self.NewtonCalculation(n-1)) - self.v)/self.vega(self.NewtonCalculation(n-1))


# Examples

# In[3]:


ImpliedVolatility('put',0.3215,0.05,50,45,1/6).NewtonCalculation()


# In[4]:


ImpliedVolatility('call',1.9982,0.05,75,80,1/3).NewtonCalculation()


# In[ ]:




