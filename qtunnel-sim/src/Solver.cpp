#include <complex>
#include <vector>
#include <cmath>
#include <fftw3.h> // For FFT-based propagation

void Solver::propagateStep(Wavefunction& wf, const std::vector<double>& V, const Grid& grid) {
    int Nx = wf.Nx;
    int Ny = wf.Ny;
    double dx = grid.dx;
    double dy = grid.dy;
    double dt = this->dt;
    double hbar = 1.0;
    double mass = 1.0;

    // ---- Step 1: FFT psi ----
    std::vector<std::complex<double>> psi_fft(Nx*Ny);
    fftw_plan plan_forward = fftw_plan_dft_2d(Ny, Nx,
                                              reinterpret_cast<fftw_complex*>(wf.psi.data()),
                                              reinterpret_cast<fftw_complex*>(psi_fft.data()),
                                              FFTW_FORWARD, FFTW_ESTIMATE);
    fftw_execute(plan_forward);

    // ---- Step 2: Apply kinetic phase in k-space ----
    for(int j=0; j<Ny; ++j){
        double ky = 2.0*M_PI*(j <= Ny/2 ? j : j-Ny)/ (Ny*dy);
        for(int i=0; i<Nx; ++i){
            double kx = 2.0*M_PI*(i <= Nx/2 ? i : i-Nx)/ (Nx*dx);
            double kinetic_phase = std::exp(-1i * hbar*dt*(kx*kx + ky*ky)/(2.0*mass));
            psi_fft[j*Nx + i] *= kinetic_phase;
        }
    }

    // ---- Step 3: Inverse FFT ----
    fftw_plan plan_backward = fftw_plan_dft_2d(Ny, Nx,
                                               reinterpret_cast<fftw_complex*>(psi_fft.data()),
                                               reinterpret_cast<fftw_complex*>(wf.psi.data()),
                                               FFTW_BACKWARD, FFTW_ESTIMATE);
    fftw_execute(plan_backward);

    // Normalize by Nx*Ny due to FFTW scaling
    for(auto &val : wf.psi) val /= (Nx*Ny);

    // ---- Step 4: Apply potential in real space ----
    for(size_t idx=0; idx<wf.psi.size(); ++idx){
        wf.psi[idx] *= std::exp(-1i * V[idx] * dt / hbar);
    }

    fftw_destroy_plan(plan_forward);
    fftw_destroy_plan(plan_backward);
}
