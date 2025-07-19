# reflection_wkb.py
import numpy as np
from scipy.optimize import newton
from dataclasses import dataclass

G = 6.67430e-11     # m^3 kg^-1 s^-2
c = 2.99792458e8    # m/s
M_sun = 1.98847e30  # kg

@dataclass
class PeakData:
    r_peak: float
    omega_peak: float
    kappa: float

def V_axial(r, l, M):
    # assumes geometric units
    f = 1 - 2*M/r
    return f * (l*(l+1)/r**2 - 6*M/r**3)

def dV_dr(r, l, M):
    # derivative for Newton solver
    term1 = -2*M/r**2 * (l*(l+1)/r**2 - 6*M/r**3)
    term2 = (1 - 2*M/r) * (-2*l*(l+1)/r**3 + 18*M/r**4)
    return term1 + term2

# def locate_peak(l, M):
#     r0 = 3 * M   # good initial guess
#     r_peak = newton(dV_dr, r0, args=(l, M))
#     Vpp = (dV_dr(r_peak*1.001, l, M) - dV_dr(r_peak*0.999, l, M)) / (0.002*r_peak)
#     omega_peak = np.sqrt(V_axial(r_peak, l, M))
#     kappa = np.sqrt(0.5 * abs(Vpp))
#     return PeakData(r_peak, omega_peak, kappa)

def locate_peak(l, M):
    """
    Analytic peak for axial (Regge–Wheeler) potential:
    r_peak = 3 M  for any l >= 2.
    """
    r_peak = 3.0 * M

    # 2nd derivative of V at the peak for kappa
    # d2V/dr2 evaluated analytically at r=3M
    Vpp = (l*(l+1) - 2) / (81.0 * M**4)    # sign < 0; take abs later
    omega_peak = np.sqrt(l*(l+1) / (27.0 * M**2))
    kappa = np.sqrt(0.5 * abs(Vpp))
    return PeakData(r_peak, omega_peak, kappa)

def R_wkb(freq, l, M_solar):
    M = G*M_solar*M_sun/c**3   # seconds  (geom units)
    peak = locate_peak(l, M)
    omega = 2*np.pi*freq*G*M_sun/c**3     # convert Hz -> geom units
    exponent = -2*np.pi*(omega-peak.omega_peak)/peak.kappa
    return 1.0 / (1.0 + np.exp(exponent))

if __name__ == "__main__":
    import argparse, csv
    p = argparse.ArgumentParser()
    p.add_argument("--mass", type=float, required=True, help="M in solar masses")
    p.add_argument("--l", type=int, default=2)
    p.add_argument("--fmin", type=float, default=20)
    p.add_argument("--fmax", type=float, default=500)
    p.add_argument("--n", type=int, default=1000)
    args = p.parse_args()

    freqs = np.linspace(args.fmin, args.fmax, args.n)
    Rvals = R_wkb(freqs, args.l, args.mass)

    with open("R_curve.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["freq_Hz", "R"])
        w.writerows(zip(freqs, Rvals))
    print("Wrote R_curve.csv")