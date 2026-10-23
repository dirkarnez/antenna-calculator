import numpy as np
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve

def simulate_24ghz_inverted_f():
    print("Initializing 2.4 GHz Numerical Partial Differential Equation Solver...\n")
    
    # ----------------------------------------------------
    # 1. TUNED 2.4 GHz GEOMETRY (Dimensions in Meters)
    # ----------------------------------------------------
    # Nodes scaled down so the structure resonates as a quarter-wave at 2.4 GHz
    nodes = np.array([
        [0.000, 0.000],  # 0: Shorting Pin Node (Grounded at the very back)
        [0.003, 0.000],  # 1: Tuned Feed Point (3mm from short for 50-ohm match)
        [0.005, 0.000],  # 2: Base corner of the main attachment
        [0.000, 0.005],  # 3: Back edge top
        [0.003, 0.005],  # 4: Mid-junction top
        [0.005, 0.005],  # 5: Main elbow corner
        [0.015, 0.005],  # 6: Radiating arm tip extending to 1.5 cm
        [0.015, 0.000]   # 7: Lower tip boundary
    ])

    # Slicing the sideways 'F' shape into a 2D mesh layout using 6 triangles
    elements = np.array([
        [0, 1, 4], [0, 4, 3],  # Segment containing the shorting and feed lines
        [1, 2, 5], [1, 5, 4],  # Middle intersection block of the junction
        [2, 7, 6], [2, 6, 5]   # Long horizontal wave-resonating arm segment
    ])

    num_nodes = len(nodes)

    # Electrical parameters for standard circuit board substrates (FR4 substrate)
    er = 4.4              # Dielectric constant
    h = 0.0016            # Substrate thickness (1.6 mm)
    c = 3e8               # Speed of light (m/s)
    uo = 4 * np.pi * 1e-7 # Permeability of free space
    
    # ----------------------------------------------------
    # 2. MATRIX ASSEMBLY ENGINE (Precalculating Elements)
    # ----------------------------------------------------
    S_global = lil_matrix((num_nodes, num_nodes))
    M_global = lil_matrix((num_nodes, num_nodes))

    for elem in elements:
        # Pull coordinates for our local master blueprint triangle
        p1, p2, p3 = nodes[elem[0]], nodes[elem[1]], nodes[elem[2]]
        
        # Calculate Jacobian determinant (Twice the surface area of the element)
        Ae2 = abs(p1[0]*(p2[1] - p3[1]) + p2[0]*(p3[1] - p1[1]) + p3[0]*(p1[1] - p2[1]))
        Area = Ae2 / 2.0
        
        # Compute gradient vectors across shape surfaces
        b = np.array([p2[1]-p3[1], p3[1]-p1[1], p1[1]-p2[1]])
        gamma = np.array([p3[0]-p2[0], p1[0]-p3[0], p2[0]-p1[0]])
        
        S_local = np.zeros((3, 3))
        M_local = np.zeros((3, 3))
        
        for i in range(3):
            for j in range(3):
                # Solving localized continuous equations over our matrix template
                S_local[i, j] = (b[i]*b[j] + gamma[i]*gamma[j]) / (2.0 * Ae2) if Ae2 != 0 else 0
                M_local[i, j] = (Area / 12.0) if i != j else (Area / 6.0)
        
        # Scale and paste the precalculated element results into global systems
        for i in range(3):
            for j in range(3):
                S_global[elem[i], elem[j]] += S_local[i, j]
                M_global[elem[i], elem[j]] += M_local[i, j]

    # ----------------------------------------------------
    # 3. 2.4 GHz SUB-BAND FREQUENCY SWEEP
    # ----------------------------------------------------
    freq_axis = np.linspace(2.0e9, 2.8e9, 41)  # Sweep around the 2.4 GHz spectrum band
    s11_results = []
    
    short_node = 0  # Anchor ground node (0 Volts)
    feed_node = 1   # Signal feed node
    
    print(f"{'Frequency (GHz)':<18}{'Return Loss S11 (dB)':<20}")
    print("-" * 38)
    
    for freq in freq_axis:
        omega = 2 * np.pi * freq
        k0_sq = (omega / c) ** 2
        
        # Wave Equation PDE Matrix Setup: [A] = [S] - k0^2 * er * [M]
        A_sys = S_global - (k0_sq * er * M_global)
        A_sys = A_sys.tolil()
        
        # Current excitation source array injection
        B_vec = np.zeros(num_nodes, dtype=complex)
        B_vec[feed_node] = 1j * omega * uo * h  
        
        # Inject Dirichlet Boundary Rule (Force Shorting Pin Node completely to 0V)
        A_sys[short_node, :] = 0
        A_sys[short_node, short_node] = 1
        B_vec[short_node] = 0
        
        # Compute the PDE grid results using linear system solver matrix algebra
        V_solution = spsolve(A_sys.tocsr(), B_vec)
        Z_in = V_solution[feed_node] / 1.0  
        
        # Compute return coefficients matching a standard 50-ohm reference line
        gamma_refl = (Z_in - 50) / (Z_in + 50)
        s11_db = 20 * np.log10(max(abs(gamma_refl), 1e-5))
        s11_results.append(s11_db)
        
        print(f"{freq/1e9:<18.2f}{s11_db:<20.2f}")

    # ----------------------------------------------------
    # 4. DISCOVER BANDWIDTH IMPEDANCE CUTOFFS
    # ----------------------------------------------------
    s11_results = np.array(s11_results)
    below_thresh = s11_results <= -10.0
    
    if np.any(below_thresh):
        matched_freqs = freq_axis[below_thresh]
        f_low = matched_freqs[0]
        f_high = matched_freqs[-1]
        f_center = (f_low + f_high) / 2.0
        fractional_bandwidth = ((f_high - f_low) / f_center) * 100
        
        print("\n" + "="*38)
        print(f"2.4 GHz Bandwidth Simulation Complete:")
        print(f"Resonance Range: {f_low/1e9:.2f} GHz to {f_high/1e9:.2f} GHz")
        print(f"Calculated Fractional Bandwidth: {fractional_bandwidth:.2f}%")
        print("="*38)
    else:
        min_idx = np.argmin(s11_results)
        print("\n" + "="*38)
        print("Antenna resonance calculated across grid layout:")
        print(f"Strongest natural resonance dip found at: {freq_axis[min_idx]/1e9:.2f} GHz")
        print("To deepen the dip below -10 dB, increase mesh triangle density.")
        print("="*38)

if __name__ == "__main__":
    simulate_24ghz_inverted_f()
