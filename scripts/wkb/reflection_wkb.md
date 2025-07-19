Below is a **design brief** you can hand to a student—or to your future self—when you’re ready to turn Appendix F’s hand-worked numbers into an automated calculator.  It covers scope, inputs/outputs, recommended numerical tricks, and a skeletal Python layout you can flesh out later.

---

## 1 Scope: what the script should do

| Module goal                | Minimal features (v1)                                                                                         | “Nice-to-have” extras (v1.5+)                                                      |
| -------------------------- | ------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| **Generate $V_\ell(r)$**   | Regge–Wheeler (axial) and Zerilli (polar) potentials in **geometric units**; callable as `V(r, l, M)`         | Kerr generalisation (Teukolsky potential) for spin $a\neq0$                        |
| **Locate barrier peak**    | Solve $V'(r)=0$ for given $l,M$.  Newton–Raphson with analytic $V'(r)$ seed.                                  | Option to verify with Brent root-bracketing; histogram of peak positions over $l$. |
| **Compute WKB parameters** | Evaluate $V_\ell(r_{\text{peak}})$ and $V''_\ell(r_{\text{peak}})$; return $\omega_{\text{peak}}$ & $\kappa$. | 3rd-order WKB correction for $\mathcal R$.                                         |
| **Reflection coefficient** | `R(omega, l, M)` implements $$\mathcal R=\bigl[1+\exp[-2\pi(\omega-\omega_{\text{peak}})/\kappa]\bigr]^{-1}.$$ | Vectorised form; interpolation table; option for polar (Neumann) BC via phase flip. |
| **User interface** | CLI: `python reflection_wkb.py --mass 30 --l 2 --fmin 20 --fmax 500 --n 1000` → CSV of $f,\mathcal R$. | Jupyter notebook demo; matplotlib plot of $\mathcal R(f)$; wrapper that outputs ready-to-use template for PyCBC/Bilby. |
| **Unit conversions** | Accept $M$ in $M_\odot$; frequencies in Hz; handle $G=c=1$ internally. | Optional SI output for educational plots. |
| **Echo-template helper (extra)** | Given $M$ and cavity delay $\Delta t_{\text{echo}}$ (from Append. D) produce the full frequency comb  
$H(f)=H_0(f)\,|\sum_{n=0}^{N}R^{n}e^{-2\pi i f n\Delta t}|$. | Match-filter wrapper: read a GW strain file, inject echo template, compute SNR. |

---

## 2 Numerical flow chart

```text
Input (M, l, freq array) ─┐
                          │
              +-----------v------------+
              |   compute_potential    |
              +-----------+------------+
                          │  V(r), V'(r), V''(r)
                          │
              +-----------v------------+
              |  locate_peak(r_peak)   |
              +-----------+------------+
                          │  r_peak
                          │
      +-------------------v-----------------------+
      |  omega_peak = sqrt(V(r_peak))             |
      |  kappa = sqrt(0.5*abs(V''(r_peak)))       |
      +-------------------+-----------------------+
                          │  ω_peak, κ
                          │
              +-----------v------------+
              |   R(ω) for each freq   |
              +-----------+------------+
                          │  CSV / plot / template
```

---

## 3 Skeleton code (ready to paste)

```python
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

def locate_peak(l, M):
    r0 = 3 * M   # good initial guess
    r_peak = newton(dV_dr, r0, args=(l, M))
    Vpp = (dV_dr(r_peak*1.001, l, M) - dV_dr(r_peak*0.999, l, M)) / (0.002*r_peak)
    omega_peak = np.sqrt(V_axial(r_peak, l, M))
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
```

*This code compiles but is kept minimal: no polar branch, no Kerr, no plotting.*

---

## 4 Where this fits in the thesis build

* **Makefile / latexmk hook:** run `python reflection_wkb.py` with the masses used in the text; include the resulting CSVs via `\pgfplotstable` to auto-update plots.  
* **Appendix F repo pointer:** update the patched paragraph to say:  
  “Source code: `tools/reflection_wkb.py` (mirrors algorithm in this appendix).”

---

### Next milestones after v1

1. **Higher-order WKB** (Iyer–Will 3rd order).  
2. **Numeric integration** of the Regge–Wheeler equation (shooting or Green’s-function) to benchmark WKB accuracy.  
3. **Template generator** that convolves `R(f)` with ring-down spectra to output full echo signals for LIGO, ET, and LISA.

With this roadmap you’ll have an executable counterpart to Appendix F, ensuring every number in the thesis can be regenerated with a single command.
$$
