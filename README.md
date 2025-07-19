# Dimensional Collapse Theory (DCT)

**A Covariant Framework for Dynamic Spacetime Dimensionality**

**Author:** Marek Hubka  
**Version:** 1.0 (June 2025)  

[![DOI](https://zenodo.org/badge/1022554057.svg)](https://doi.org/10.5281/zenodo.16152610)
![Code License](https://img.shields.io/badge/code-MIT-blue.svg)
![Dcos License](https://img.shields.io/badge/docs-CC--BY--NC--ND%204.0-lightgrey.svg)

> This repository contains the full manuscript and supplementary materials for Dimensional Collapse Theory (DCT), a novel theoretical framework proposing that spacetime dimensionality is a dynamic field that changes in response to local entropy density.

---

## Overview

**Dimensional Collapse Theory (DCT)**, is a novel theoretical physics framework. DCT proposes that spacetime dimensionality is not a fixed constant, but a dynamical field $D(x)$ that changes in response to local physical conditions - specifically, entropy density.

The core idea of DCT is that when the local entropy density reaches a critical holographic bound ($1/\ell_P^2$), the dimensionality of spacetime irreversibly collapses in discrete steps of two ($D \to D-2$). This provides a physical mechanism that offers potential resolutions to several long-standing problems in fundamental physics.

**This thesis primarily establishes the *what* and *where* of dimensional collapse, defining the conditions for the transition and describing the resulting structures. The *how* - the detailed microscopic mechanism driving the transition (such as the conjectured "null-pair removal" process) is the subject of ongoing research and dedicated future work.**

## What Problems Does DCT Address?

DCT offers a unified perspective on several major puzzles by introducing a single new fundamental concept: the dynamic nature of dimension.

1.  **Black Hole Singularities:** The classical singularity of infinite density is replaced by a finite, 2-dimensional physical "ledger surface" at an inner core radius of $R_{\text{core}} \approx 0.60 R_s$. This resolves the infinity while providing a concrete physical structure to store information.

2.  **The Information Paradox:** Information that falls into a black hole is not destroyed. It is losslessly encoded on the 2D ledger surface. DCT predicts that Hawking radiation is subtly correlated with the state of this ledger, allowing for unitary evolution and the eventual recovery of all information.

3.  **The Arrow of Time:** The theory formulates a **Law of Transdimensional Thermodynamics (TDT)**, where the information-carrying capacity of spacetime *grows* by a factor of $1/\alpha_H = 4\ln 2 \approx 2.773$ with each dimensional collapse. Because an "un-collapse" is thermodynamically forbidden, this provides a fundamental, geometric origin for the arrow of time.

4.  **Dark Matter Candidates:** DCT predicts that black hole evaporation halts, leaving stable, universal Planck-mass remnants ($M_{\text{rem}} \approx 1.1 M_P$). Primordial black holes that formed in the early universe would have evaporated by now, populating the cosmos with these remnants, which are natural dark matter candidates without requiring new particle physics.

5.  **Quantum Measurement Problem:** DCT offers a potential physical mechanism for quantum state reduction ("collapse of the wavefunction"), where a measurement is an entropy-generating process that triggers a local, objective dimensional collapse, "freezing" a single outcome into reality.

## Repository Contents

*   `manuscript/`: Contains the primary thesis document.
    *   `dct.pdf`: The complete, compiled PDF of the manuscript.
*   `dct.tex`: The full LaTeX source code for the manuscript.
*   `dct.bib`: The BibTeX library of cited resources.
*   `figures/`: Source files for figures and plots used in the manuscript.
*   `scripts/`:
    *   `micro_collapse_sim.ipynb`: A Python Jupyter notebook containing a **demonstrative simulation** of the entropy-triggered collapse mechanism and a **numerical testbed** for verifying the theory's key calculations.
    *   `figs/`: Scripts used to generate figures.
    *   `wkb/`: Files related to the WKB approximation for echo reflection coefficients.
*   `README.md`: This file.
*   `LICENSE`: The MIT License.
*   `LICENSE-MANUSCRIPT`: The CC BY 4.0 License

## Getting Started

1.  **Read the Manuscript:** The best place to start for a comprehensive overview of the theory, its postulates, derivations, and predictions is `manuscript/dct.pdf`.

2.  **Explore the Notebook:** To see the calculations in action and verify the numbers, open and run `scripts/micro_collapse_sim.ipynb`.

## Citing this Work

If you use the concepts, code, or text from this work in your own research, please cite the repository using its DOI.

A suggested BibTeX entry:
```bibtex
@misc{Hubka2025,
  author       = {Marek Hubka},
  title        = {Dimensional Collapse Theory and the Law of Transdimensional Thermodynamics},
  year         = {2025},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.16152610},
  url          = {https://doi.org/10.5281/zenodo.16152610}
}
```

## License

The contents of this repository are provided under two licenses:

*   **Source Code:** All source code, including Python scripts and Jupyter notebooks (`/scripts/`), is licensed under the **MIT License**. See the `LICENSE` file for details.
*   **Manuscript & Figures:** The manuscript text and figures (`/manuscript/`, `/figures/`) are licensed under the **Creative Commons Attribution 4.0 International License (`CC BY 4.0`)**. You are free to share and adapt this work for any purpose, provided you give appropriate credit.

## Status & Support

This is a work of independent research. The theory is presented here as a complete, self-consistent framework, but many avenues for further development and more rigorous mathematical proofs remain. Corrections, feedback, and collaboration are highly welcome.

If you find this work valuable and wish to support its continued development, please feel free to reach out.

## Contact

For any questions, feedback, or collaboration inquiries, you can open an issue on this GitHub repository or contact me directly at **marek@tidesofuncertainty.com**.
