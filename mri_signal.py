!python -m pip install pydicom numpy matplotlib nibabel scipy
!python -m pip install pylibjpeg pylibjpeg-libjpeg pylibjpeg-openjpeg

import numpy as np
import matplotlib.pyplot as plt
import pydicom
import nibabel as nib
from pathlib import Path
import os
from scipy import ndimage

print("All libraries imported successfully!")
######################################################################################################

# =====================================================
# 1.2 CREATE SAMPLE 3D MRI DATA
# =====================================================

def create_sample_mri(shape=(64, 64, 30)):
    """
    Create a synthetic 3D MRI volume for demonstration
    """
    # Create a 3D volume with background
    volume = np.random.normal(100, 15, shape).astype(np.float32)
    
    # Add a spherical structure (simulating tissue)
    z, y, x = np.ogrid[:shape[0], :shape[1], :shape[2]]
    center = np.array(shape) // 2
    
    # Main sphere
    radius = min(shape) // 4
    sphere_mask = ((x - center[2])**2 + (y - center[1])**2 + 
                   (z - center[0])**2) <= radius**2
    volume[sphere_mask] = np.random.normal(800, 50, np.sum(sphere_mask))
    
    # Smaller bright sphere (simulating tumor or vessel)
    small_center = center + np.array([5, 5, 0])
    small_radius = radius // 3
    small_sphere = ((x - small_center[2])**2 + (y - small_center[1])**2 + 
                    (z - small_center[0])**2) <= small_radius**2
    volume[small_sphere] = np.random.normal(1200, 60, np.sum(small_sphere))
    
    return volume

# Create sample data
sample_volume = create_sample_mri()
print(f"Sample volume created with shape: {sample_volume.shape}")
print(f"Intensity range: [{sample_volume.min():.1f}, {sample_volume.max():.1f}]")


