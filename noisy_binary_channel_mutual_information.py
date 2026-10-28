import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from numpy import log2 as l

def avg_mutual_inf_uniform_source(a,b,c,d,epsilon=1e-10):
    """
    Calculates the average mutual information for a noisy binary channel, with channel probabilities defined as:
             a
    X1 ----------- Y1
     b \          /
        \        /
         \      /
          \    /
            \ /
             X
           /   \
          /     \
         /       \
        /         \
     c /           \
    X0 -------------Y0
             d
    Python will have issues for channel probs that are 0, so will replace with an epsilon.
    ASSUMES A UNIFORM SOURCE!
    Known bug- singularity when a=c or b=d. Add a small epsilon to make them different and there's no problem/the actual solution is well-behaved at this point.
    """
    chan_probs = [a,b,c,d]
    new_probs = [epsilon if i==0 else i for i in chan_probs]
    an,bn,cn,dn = new_probs

    mi = 0.5*(an*(1-np.log2(1+cn/an)) + bn*(1-np.log2(1+dn/bn)) +cn*(1-np.log2(1+an/cn)) + dn*(1-np.log2(1+bn/dn)))
    return mi

def avg_mi_arb_p(a,b,c,d,px1,epsilon=1e-10):
    """
    Calculates the average mutual information for a noisy binary channel, with channel probabilities defined as:
             a
    X1 ----------- Y1
     b \          /
        \        /
         \      /
          \    /
            \ /
             X
           /   \
          /     \
         /       \
        /         \
     c /           \
    X0 -------------Y0
             d
    And the probability of X1 being px1.
    Python will have issues for channel probs that are 0, so will replace with an epsilon.
    Known bug- singularity when a=c or b=d. Add a small epsilon to make them different and there's no problem/the actual solution is well-behaved at this point.
    """
    px0=1-px1
    chan_probs = [a,b,c,d]
    new_probs = [epsilon if i==0 else i for i in chan_probs]
    an,bn,cn,dn = new_probs
    py1 = (px1*an + px0*cn)
    py0 = 1-py1
    mi = (px1*(an*l(an/py1) + bn*l(bn/py0)) + px0*(cn*l(cn/py1) + dn*l(dn/py0)))
    return mi

def find_capacity_and_p(a,b,c,d,num_samples=1000,epsilon=1e-15):
    """"Given channel probabilities a,b,c and d 
    (a,d: 1 and 0 fidelity rates respectively, 
    b,c:1->0 and 0->1 error respectively)
    calculates the central capacity and
    capacity-achieving priors."""
    test_ps = np.linspace(epsilon,1-epsilon,num_samples)
    mis = avg_mi_arb_p(a,b,c,d,test_ps,epsilon=epsilon)

    capacity = np.max(mis)
    capacity_achieving_p = test_ps[np.argmax(mis)]
    return capacity, capacity_achieving_p

def capacity_and_capacity_achieving_p_with_err(b,berr,c,cerr,num_samples=1000,epsilon=1e-15):
    """"Given the 1->0 crossover rate (b) and its error,
    the 0->1 crossover rate (c) and its error,
    calculates the capacity of the channel, the capacity-achieving prior
    and the error in both (both above and below the mean)"""
    central_cap, central_p = find_capacity_and_p(1-b,b,c,1-c,num_samples,epsilon)
    cap_b_plus, p_b_plus = find_capacity_and_p(1-(b+berr),b+berr,c,1-c)
    cap_b_min, p_b_min = find_capacity_and_p(1-(b-berr),b-berr,c,1-c)
    cap_c_plus, p_c_plus = find_capacity_and_p(1-b,b,c+cerr,1-(c+cerr))
    cap_c_min, p_c_min = find_capacity_and_p(1-b,b,c-cerr,1-(c-cerr))
    
    delta_cap_above = np.sqrt((central_cap-cap_b_min)**2 + (central_cap-cap_c_min)**2)
    delta_cap_below = np.sqrt((central_cap-cap_b_plus)**2 + (central_cap-cap_c_plus)**2)
    delta_p_above = np.sqrt((np.max([p_b_plus,p_b_min])-central_p)**2 + (np.max([p_c_plus,p_c_min])-central_p)**2)
    delta_p_below = np.sqrt((np.min([p_b_plus,p_b_min])-central_p)**2 + (np.min([p_c_plus,p_c_min])-central_p)**2)

    return (central_cap,central_p), [(delta_cap_above,delta_cap_below),(delta_p_above,delta_p_below)]


if __name__ == "__main__":
    font = {'family' : 'Apple SD Gothic Neo',
        'weight' : 'regular',
        'size'   : 10}
    mpl.rc('font',**font)
    mpl.rcParams['pdf.fonttype'] = 42
    mpl.rcParams['ps.fonttype'] = 42
    mpl.rcParams['svg.fonttype'] = 'none'
    mpl.rcParams['figure.constrained_layout.use'] = True
    mpl.rcParams['axes.unicode_minus'] = False
    a1=0.5
    b1=0.5
    c1=0
    d1=1
    px1 = 0.5
    print(avg_mi_arb_p(a1,b1,c1,d1,px1))

    ps = np.linspace(1e-10,1-1e-10,1000)
    mis = avg_mi_arb_p(a1,b1,c1,d1,ps,epsilon=1e-20)

    fig,ax=plt.subplots()
    ax.plot(ps,mis)
    cap_achieving_p = ps[np.argmax(mis)]
    cap = np.max(mis)
    ax.axvline(cap_achieving_p,c='r',ls='--')
    ax.axhline(cap,c='r',ls='--')
    print(f"Capacity: {cap}, Prior: {cap_achieving_p}")

    print(capacity_and_capacity_achieving_p_with_err(b1,0.05,c1,0.05))
    plt.show()