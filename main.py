import numpy as np
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve

def simulate_inverted_f_bandwidth():
    # ----------------------------------------------------
    # 1. GEOMETRY DEFINITION (Nodes and Triangular Mesh)
    # ----------------------------------------------------
    # Coordinates of vertices defining a small Planar Inverted-F Antenna (in meters)
    # The shape forms a main radiating plate with an integrated feed/short zone
    nodes = np.array([
        [0.00, 0.00],  # 0: Shorting Pin Node (Grounded)
        [0.01, 0.00],  # 1: Feed Point Node (Excitation input)
        [0.03, 0.00],  # 2: Corner of the arm
        [0.00, 0.02],  # 3: Back edge
        [0.01, 0.02],  # 4: Mid-plate node
        [0.03, 0.02],  # 5: Front edge corner
        [0.05, 0.02],  # 6: Extended radiating arm tip
        [0.05, 0.00]   # 7: Lower edge of extended arm
    ])

    # Element connectivity matrix (Triangles adding up to make the shape)
    elements = np.array([
        [0, 1, 4], [0, 4, 3],  # Segment near short and feed
        [1, 2, 5], [1, 5, 4],  # Middle section of the patch
        [2, 7, 6], [2, 6, 5]   # Extended arm segment of the Inverted-F
    ])

    num_nodes = len(nodes)
    num_elements = len(elements)

    # Substrate electrical properties (e.g., standard FR4 substrate metrics)
    er = 4.4            # Relative Permittivity (Dielectric Constant)
    h = 0.0016          # Substrate Thickness (1.6 mm)
    c = 3e8             # Speed of light (m/s)
    eo = 8.854e-12      # Permittivity of free space
    uo = 4 * np.pi * 1e-7 # Permeability of free space
    
    # ----------------------------------------------------
    # 2. PRE-INTEGRATING THE MASTER TRIANGLE UNITS
    # ----------------------------------------------------
    # Global Stiffness (S) and Mass (M) sparse matrix assemblers
    S_global = lil_matrix((num_nodes, num_nodes))
    M_global = lil_matrix((num_nodes, num_nodes))

    for elem in elements:
        # Get coordinates of the 3 vertices of this individual triangle
        p1, p2, p3 = nodes[elem[0]], nodes[elem[1]], nodes[elem[2]]
        
        # Calculate the Determinant of the Jacobian (Twice the area of the triangle)
        Ae2 = abs(p1[0]*(p2[1] - p3[1]) + p2[0]*(p3[1] - p1[1]) + p3[0]*(p1[1] - p2[1]))
        Area = Ae2 / 2.0
        
        # Compute shape function gradients (b and c coefficients for linear triangle elements)
        b = np.array([p2[1]-p3[1], p3[1]-p1[1], p1[1]-p2[1]])
        gamma = np.array([p3[0]-p2[0], p1[0]-p3[0], p2[0]-p1[0]])
        
        # Assemble local element matrices
        S_local = np.zeros((3, 3))
        M_local = np.zeros((3, 3))
        
        for i in range(3):
            for j in range(3):
                # Gradient multiplication for Helmholtz stiffness
                S_local[i, j] = (b[i]*b[j] + gamma[i]*gamma[j]) / (2.0 * Ae2)
                # Consistent mass integration over reference triangle area
                M_local[i, j] = (Area / 12.0) if i != j else (Area / 6.0)
        
        # Stitch local elements directly into the overall Global System Topology
        for i in range(3):
            for j in range(3):
                S_global[elem[i], elem[j]] += S_local[i, j]
                M_global[elem[i], elem[j]] += M_local[i, j]

    # ----------------------------------------------------
    # 3. FREQUENCY SWEEP & BOUNDARY INTERLOCKS
    # ----------------------------------------------------
    freq_axis = np.linspace(1.5e9, 3.5e9, 101) # Sweep from 1.5 GHz to 3.5 GHz
    s11_results = []
    
    short_node = 0  # Inverted-F shorting pin anchored to Ground Plane (0V)
    feed_node = 1   # Excitation point where 50-ohm line attaches
    
    print(f"{'Frequency (GHz)':<18}{'Return Loss S11 (dB)':<20}")
    print("-" * 38)
    
    for freq in freq_axis:
        omega = 2 * np.pi * freq
        k0_sq = (omega / c) ** 2
        
        # Wave Equation PDE Matrix: [A] = [S] - k0^2 * er * [M]
        A_sys = S_global - (k0_sq * er * M_global)
        A_sys = A_sys.tolil()
        
        # Force Forcing Vector (Source Current Injection)
        B_vec = np.zeros(num_nodes, dtype=complex)
        B_vec[feed_node] = 1j * omega * uo * h  # Simulated input current stimulus
        
        # Apply Dirichlet Boundary Condition for the shorting pin (Force Voltage to 0V)
        A_sys[short_node, :] = 0
        A_sys[short_node, short_node] = 1
        B_vec[short_node] = 0
        
        # Convert to compressed format and solve the linear matrix PDE system [A]{V} = {B}
        V_solution = spsolve(A_sys.tocsr(), B_vec)
        
        # Extract Input Impedance (Z_in) at the feed node zone
        Z_in = V_solution[feed_node] / 1.0 # Normalized against 1A input current
        
        # Calculate S11 Return Loss against a standard 50-ohm reference line
        gamma_refl = (Z_in - 50) / (Z_in + 50)
        s11_db = 20 * np.log10(max(abs(gamma_refl), 1e-5))
        s11_results.append(s11_db)
        
        # Print ongoing computation frame updates
        if int(freq / 1e7) % 20 == 0:
            print(f"{freq/1e9:<18.2f}{s11_db:<20.2f}")

    # ----------------------------------------------------
    # 4. IMPEDANCE BANDWIDTH EVALUATION
    # ----------------------------------------------------
    s11_results = np.array(s11_results)
    below_thresh = s11_results <= -10.0 # Find frequencies with proper matching (< -10 dB)
    
    if np.any(below_thresh):
        matched_freqs = freq_axis[below_thresh]
        f_low = matched_freqs[0]
        f_high = matched_freqs[-1]
        f_center = (f_low + f_high) / 2.0
        fractional_bandwidth = ((f_high - f_low) / f_center) * 100
        
        print("\n" + "="*38)
        print(f"Simulation Analysis Complete:")
        print(f"Lower Cutoff:  {f_low/1e9:.3f} GHz")
        print(f"Upper Cutoff:  {f_high/1e9:.3f} GHz")
        print(f"Calculated -10dB Fractional Bandwidth: {fractional_bandwidth:.2f}%")
        print("="*38)
    else:
        print("\nAntenna mismatch: Return loss did not drop below -10 dB threshold.")

if __name__ == "__main__":
    simulate_inverted_f_bandwidth()
