# Programming Projects  
A collection of personal projects exploring computational physics simulations, high-performance computing, and digital signal processing.

<p align="left">
  <a href="#high-performance-circle-packing-hpc">Circle Packing (HPC)</a> •
  <a href="#digital-communications-simulator-dsp">Digital Communications Simulator</a> •
  <a href="#n-body-simulation">N-Body Simulation</a> •
  <a href="#letterboxd-watchlist-comparison-tool">Letterboxd Tool</a>
</p>

---

## 🛠️ Featured Projects

### High-Performance Circle Packing (HPC)
📂 [View Code](./circle-packing)

A computational physics project designed to calculate the packing fraction of hard circles in a 2D domain, transitioning from a serial baseline to high-performance parallel computing.

* **Key Features:**
  * **Parallel Scale:** Implemented a distributed memory version using MPI that partitions the 2D domain and handles boundary synchronization between processes.
  * **Performance Benchmarking:** Evaluated scalability on the University of York's **Viking2** supercomputer to analyze performance scaling across multiple MPI tasks.
  * **Data Pipeline:** Utilizes a custom Mersenne Twister RNG in C++ coupled with a Jupyter Notebook pipeline to visualize the final packing distribution and process boundaries.
* **Tech Stack:** C++, MPI, OpenMP, Python, Jupyter Notebook, Matplotlib
* **Status:** Completed (Scientific Supercomputing Portfolio)

---

### Digital Communications Simulator (DSP)
📂 [View Code](./telecom-sim)

A discrete-time software radio simulator that models data transmission over a noisy channel, demonstrating the physics of wave modulation, pulse shaping, and signal recovery.

* **Key Features:**
  * **End-to-End Pipeline:** Simulates the complete physical layer sequence: Random Bit Generation $\rightarrow$ BPSK Modulation $\rightarrow$ TX Pulse Shaping $\rightarrow$ AWGN Channel Noise $\rightarrow$ RX Matched Filtering $\rightarrow$ Signal Downsampling $\rightarrow$ Bit Detection.
  * **Custom Pulse Shaping:** Designed a Root-Raised Cosine (RRC) filter from scratch, carefully managing mathematical edge cases (such as center peaks and intercept points) to minimize Inter-Symbol Interference (ISI).
  * **Empirical Verification:** Sweeps across a user-defined Signal-to-Noise Ratio (SNR) range to compute the Bit Error Rate (BER), verifying performance by plotting the results directly against the theoretical curve using `scipy.special.erfc`.
* **Tech Stack:** Python, NumPy, SciPy, Matplotlib
* **Status:** Actively Developed

---

### N-Body Simulation
📂 [View Code](./n-body)

A physics simulation tracking gravitational interactions, orbital mechanics, and multi-body dynamics.

* **Key Features:**
  * **Core Engine:** Built a basic gravitational orbit simulation to model multi-body celestial tracking.
  * **Collision Theory:** Designed custom fragmentation scoring logic to support future kinetic collision and merging mechanics.
* **Tech Stack:** C++, Python, NumPy, Matplotlib, Jupyter Notebook
* **Status:** Prototype


---

### Letterboxd Watchlist Comparison Tool
📂 [View Code](./letterboxd-tool)

A desktop application designed to scrape and cross-reference multiple Letterboxd user watchlists to find shared film interests.

* **Key Features:**
  * **Data Aggregation:** Scrapes user watchlists via BeautifulSoup and enriches data using TMDb API lookups for metadata, artwork, and regional streaming availability.
  * **Dynamic UI:** Developed a Tkinter interface featuring advanced filtering options (runtime, unseen status) and fluid poster rendering.
  * **Robust Config:** Employs a robust `config.json` system to cleanly manage user groups, API keys, streaming regions, and scrape delays to prevent rate-limiting.
* **Tech Stack:** Python, Tkinter, Pandas, Requests, BeautifulSoup, Pillow
* **Status:** Completed


---

## 🧠 Key Takeaways & Skills

* **Distributed & Parallel Computing:** Experience managing process communication, data synchronization, and load balancing across multi-node HPC clusters (MPI, OpenMP).
* **Digital Signal Processing (DSP):** Building numerical models for discrete-time systems, applying convolutions, tracking group delays, and constructing custom filter taps.
* **Stochastic Modeling & Analysis:** Simulating statistical physical properties like AWGN channels and pseudorandom distributions (Mersenne Twister), verified against analytical mathematical models.
* **Software Design:** Applying modular architecture, decoupled configurations (`dataclasses`, JSON), and automated visualization pipelines across both C++ and Python environments.
