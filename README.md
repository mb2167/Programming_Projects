<p align="center">
  <a href="#project-overview">Project Overview</a> •
  <a href="#high-performance-circle-packing-hpc">Circle Packing (HPC)</a> •
  <a href="#n-body-simulation">N-Body Simulation</a> •
  <a href="#letterboxd-watchlist-comparison-tool">Letterboxd Tool</a>
</p>

# Programming Projects  
Personal programming projects for physics-based simulations and additional tools.

---

## Project Overview  
This repository hosts a collection of personal projects that explore physics through computational simulations and other supporting programming tools.  
Each project is driven by curiosity, a passion for learning, and the goal of combining theoretical physics with computational implementation.

- **High-Performance Circle Packing:** A study on packing fractions using Serial and MPI (Distributed Memory) parallelisation.
- **Fluid Simulation:** Exploring fluid dynamics through computational models.  
- **N-Body Simulation:** Simulating gravitational interactions and orbital mechanics.  
- **Quantum Tunnelling Simulation:** Investigating quantum wavefunction behaviour through numerical methods.  
- **Letterboxd Watchlist Comparison Tool:** A standalone application for analysing shared film interests.

---

## High-Performance Circle Packing (HPC)

<p align="center">
  <a href="#project-overview">Project Overview</a> •
  <a href="#high-performance-circle-packing-hpc">Circle Packing (HPC)</a> •
  <a href="#n-body-simulation">N-Body Simulation</a> •
  <a href="#letterboxd-watchlist-comparison-tool">Letterboxd Tool</a>
</p>

A computational physics project designed to calculate the "Packing Fraction" of hard circles in a 2D domain. This project focuses on the transition from serial algorithms to high-performance parallel computing.

**Key Features:** - **Serial Baseline:** Implementation of a hard-sphere packing algorithm with custom Mersenne Twister RNG and high-resolution timing.
- **MPI Parallelisation:** A distributed memory version that partitions the domain and handles boundary synchronisation between processes.
- **Scalability Analysis:** Evaluated on the **Viking2** supercomputer to analyse performance scaling across multiple MPI tasks.
- **Data Visualisation:** A Jupyter Notebook pipeline to visualise the final packing distribution and process boundaries.

**Technical Stack:** - **Languages:** C++, Python  
- **Parallel Computing:** MPI (Message Passing Interface), OpenMP  
- **Libraries / Tools:** Jupyter Notebook, Matplotlib, HPC Cluster Environments (University of York's Viking 2) 

**Status:** Completed (Scientific Supercomputing Portfolio)  

---

## N-Body Simulation

<p align="center">
  <a href="#project-overview">Project Overview</a> •
  <a href="#high-performance-circle-packing-hpc">Circle Packing (HPC)</a> •
  <a href="#n-body-simulation">N-Body Simulation</a> •
  <a href="#letterboxd-watchlist-comparison-tool">Letterboxd Tool</a>
</p>

**Current Progress:** - Basic gravitational orbit simulation implemented.  
- Fragmentation scoring designed for future collision modelling.

**Goals:** - Add collision and merging logic.  
- Improve performance for large system sizes.  
- Provide richer visualisation of orbital behaviour.

**Technical Stack:** - **Languages:** C++, Python  
- **Libraries / Tools:** VSCode, NumPy, Matplotlib, Jupyter Notebook  

**Status:** Prototype  

---

## Letterboxd Watchlist Comparison Tool

<p align="center">
  <a href="#project-overview">Project Overview</a> •
  <a href="#high-performance-circle-packing-hpc">Circle Packing (HPC)</a> •
  <a href="#n-body-simulation">N-Body Simulation</a> •
  <a href="#letterboxd-watchlist-comparison-tool">Letterboxd Tool</a>
</p>

A desktop tool for scraping multiple Letterboxd users’ watchlists and analysing films in common.

**Features:** - Scrapes one or more users’ Letterboxd watchlists  
- Performs TMDb API lookups for metadata, posters, and watch availability  
- Allows filtering by selected users, runtime, and unseen status  
- Displays detailed film information, including poster and overview  

**Technical Stack:** - **Language:** Python  
- **Libraries / Tools:** Tkinter, Pandas, Requests, BeautifulSoup, Pillow  

**Configuration:** A configurable `config.json` file allows:  
- Adding user groups  
- API key entry  
- Region selection for streaming information  
- Performance tuning of scrape delays  

**Status:** Actively developed  

---

## Highlights & Achievements  
- **Parallel Computing:** Successfully implemented and benchmarked MPI-based simulations for large-scale physics problems.
- Developed early-stage multi-body orbital mechanics simulation.  
- Created a practical application for comparing watchlists and visualising shared interests.  
- Established structure for continued physics simulation development.  
- Hands-on experience across numerical, graphical, and data-driven programming.

---

## Learning Outcomes  
Across these projects:  
- **Distributed Computing:** Managing process communication, data synchronisation, and load balancing in parallel environments.
- Applying numerical physics techniques to real computational simulations.  
- Building interfaces and visualisations for scientific or media data.  
- Improving software design practices and modular organisation.  

---
