import numpy as np
import plotly.graph_objects as go
from sklearn.decomposition import PCA

# --- SYSTEM CONFIGURATION (4D Demo Lattice) ---
DIM = 4

# Private Key — a secret vector known only to the owner
SECRET_KEY = np.array([2, -1, 3, 1])


# --- MODULE 1: ENCRYPTION ---
def encrypt_string(text, private_key):
    cipher_text = []
    
    # We find a vector that is strictly orthogonal to our private key.
    # The dot product of an orthogonal vector and the key is ALWAYS zero.
    # For the key [2, -1, 3, 1], an orthogonal vector would be, e.g., [1, 2, 0, 0] (2*1 + (-1)*2 = 0)
    orthogonal_base = np.array([1, 2, 0, 0])
    
    for char in text:
        m = ord(char) # Convert the character into its numerical ASCII/Unicode code
        
        # The secret point is the character code scaled by the private key vector
        secret_point = m * private_key
        
        # Generate a random offset ("lattice fog") strictly along the orthogonal line.
        # No matter how much we scale this vector, the private key will completely ignore it.
        r = np.random.randint(-50, 50)
        lattice_noise = r * orthogonal_base
        
        # Final 4D vector representing the encrypted character
        c_vector = secret_point + lattice_noise
        cipher_text.append(c_vector.tolist())
        
    return cipher_text


# --- MODULE 2: DECRYPTION ---
def decrypt_string(cipher_text, private_key):
    decrypted_text = ""
    
    # Calculate the squared length (norm) of the private key
    key_norm = np.dot(private_key, private_key)
    
    for c_vector in cipher_text:
        c_array = np.array(c_vector)
        
        # The dot product instantly flattens the orthogonal fog to absolute ZERO.
        # Leaving only the clean projection of our secret point.
        projection = np.dot(c_array, private_key)
        
        # Reconstruct the original character code without any rounding errors
        m_calculated = int(projection // key_norm)
        
        try:
            decrypted_text += chr(m_calculated)
        except ValueError:
            decrypted_text += "?"
            
    return decrypted_text


# --- EXECUTION & STRING ENCRYPTION ---
input_str = "QUANTUM_MIND"

# Pass the string through the encryption loop
encrypted_data = encrypt_string(input_str, SECRET_KEY)
decrypted_str = decrypt_string(encrypted_data, SECRET_KEY)

# Print raw text results to the console
print(f"Original Text: {input_str}")
print(f"Decrypted Text: {decrypted_str}\n")


# --- VISUALIZATION BLOCK ---
data_4d = np.array(encrypted_data)
num_points = len(data_4d)

fig = go.Figure()

# Compress 4D character coordinates into a 3D space for the plot
if num_points >= 3:
    pca = PCA(n_components=3)
    data_3d = pca.fit_transform(data_4d)
    
    fig.add_trace(
        go.Scatter3d(
            x=data_3d[:, 0],
            y=data_3d[:, 1],
            z=data_3d[:, 2],
            mode="markers+text",
            text=[f"Char: {char}" for char in input_str],
            textposition="top center",
            marker=dict(
                size=8,
                color=np.arange(num_points),
                colorscale="Viridis",
                opacity=0.8,
            ),
        )
    )
else:
    data_display = np.zeros((num_points, 3))
    data_display[:, : min(num_points, 2)] = data_4d[:, : min(num_points, 2)]
    
    fig.add_trace(
        go.Scatter3d(
            x=data_display[:, 0],
            y=data_display[:, 1],
            z=data_display[:, 2],
            mode="markers+text",
            text=[f"Char: {char}" for char in input_str],
            textposition="top center",
            marker=dict(
                size=10, color=np.arange(num_points), colorscale="Viridis"
            ),
        )
    )

# 3D Scene Styling (with custom dark background)
fig.update_layout(
    title="4D Ciphertext Projection into 3D Space (Mathematical Fog)",
    scene=dict(
        xaxis=dict(title="Dimension X"),
        yaxis=dict(title="Dimension Y"),
        zaxis=dict(title="Dimension Z"),
        bgcolor="rgb(20, 20, 30)",
    ),
    margin=dict(l=0, r=0, b=0, t=40),
    template="plotly_dark",
)

# --- SMART OUTPUT CHANNELS ---
# 1. Save the interactive 3D space as a standalone web page
fig.write_html("crypto_fog_map.html")
print("Visual telemetry successfully exported to: crypto_fog_map.html")

# 2. Try to open the browser locally (will be safely skipped on headless servers like GitHub)
try:
    import os
    if 'GITHUB_ACTIONS' not in os.environ:
        fig.show()
except Exception:
    pass
