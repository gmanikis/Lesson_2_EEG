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

#####################################################################################################################

# =====================================================
# 1.1 LOADING DICOM FILES
# =====================================================

def load_dicom_series(dicom_folder):
    """
    Load a series of DICOM files from a folder
    
    Parameters:
    -----------
    dicom_folder : str
        Path to folder containing DICOM files
        
    Returns:
    --------
    volume : 3D numpy array
    slices : list of pydicom objects
    """
    # Get all DICOM files
    dicom_files = []
    for root, dirs, files in os.walk(dicom_folder):
        for file in files:
            if file.endswith('.dcm'):
                dicom_files.append(os.path.join(root, file))
    
    # Read DICOM files
    slices = [pydicom.dcmread(f) for f in dicom_files]
    
    # Sort slices by Instance Number or Image Position
    slices.sort(key=lambda x: float(x.ImagePositionPatient[2]))
    
    # Get the pixel arrays
    image_stack = np.stack([s.pixel_array for s in slices])
    
    print(f"Loaded {len(slices)} DICOM slices")
    print(f"Volume shape: {image_stack.shape}")
    print(f"Data type: {image_stack.dtype}")
    
    return image_stack, slices

# Example usage (students will replace with their own path)
# dicom_folder = "path/to/your/dicom/folder"
# volume_3d, dicom_slices = load_dicom_series(dicom_folder)

##############################################################################################

# =====================================================
# 1.3 VISUALIZING 3D MRI SLICES
# =====================================================

def visualize_slices(volume, slice_indices=None, cmap='gray'):
    """
    Visualize multiple slices from a 3D volume
    
    Parameters:
    -----------
    volume : 3D numpy array
    slice_indices : list of slice indices to display
    cmap : colormap for display
    """
    if slice_indices is None:
        # Show beginning, middle, and end slices
        slice_indices = [0, volume.shape[0]//2, volume.shape[0]-1]
    
    fig, axes = plt.subplots(1, len(slice_indices), figsize=(15, 5))
    
    if len(slice_indices) == 1:
        axes = [axes]
    
    for idx, slice_num in enumerate(slice_indices):
        axes[idx].imshow(volume[slice_num, :, :], cmap=cmap)
        axes[idx].set_title(f'Slice {slice_num}')
        axes[idx].axis('off')
        axes[idx].set_xlabel(f'Min: {volume[slice_num].min():.0f}, Max: {volume[slice_num].max():.0f}')
    
    plt.tight_layout()
    plt.show()

#######################################################################################################################

# =====================================================
# 1.4 ACCESSING AND MODIFYING PIXELS
# =====================================================

def explore_pixel_values(volume, z, y, x, region_size=3):
    """
    Explore pixel values around a specific location
    
    Parameters:
    -----------
    volume : 3D numpy array
    z, y, x : coordinates
    region_size : size of region to display around point
    """
    print(f"Pixel value at ({z}, {y}, {x}): {volume[z, y, x]:.2f}")
    
    # Extract a small region around the point
    half_size = region_size // 2
    region = volume[
        max(0, z-half_size):min(volume.shape[0], z+half_size+1),
        max(0, y-half_size):min(volume.shape[1], y+half_size+1),
        max(0, x-half_size):min(volume.shape[2], x+half_size+1)
    ]
    
    print(f"\nRegion around point ({region.shape}):")
    print(region[region.shape[0]//2, :, :])
    
    # Visualize
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Show slice with marked point
    axes[0].imshow(volume[z, :, :], cmap='gray')
    axes[0].plot(x, y, 'r+', markersize=15, markeredgewidth=2)
    axes[0].set_title(f'Slice {z} with marked point')
    axes[0].axis('off')
    
    # Show zoomed region
    axes[1].imshow(region[region.shape[0]//2, :, :], cmap='gray')
    axes[1].set_title(f'Zoomed region around ({y}, {x})')
    axes[1].axis('off')
    
    plt.tight_layout()
    plt.show()

##################################################################################################################

# =====================================================
# 1.5 MODIFYING PIXEL INTENSITIES
# =====================================================

def modify_intensities(volume, operation='multiply', value=1.5):
    """
    Modify pixel intensities in various ways
    
    Parameters:
    -----------
    volume : 3D numpy array
    operation : 'multiply', 'add', 'threshold', 'window'
    value : parameter for the operation
    
    Returns:
    --------
    modified_volume : 3D numpy array
    """
    modified = volume.copy()
    
    if operation == 'multiply':
        modified = modified * value
        print(f"Multiplied intensities by {value}")
        
    elif operation == 'add':
        modified = modified + value
        print(f"Added {value} to all intensities")
        
    elif operation == 'threshold':
        modified[modified < value] = 0
        print(f"Applied threshold at {value}")
        
    elif operation == 'window':
        # Window/Level operation (common in medical imaging)
        window_width, window_level = value
        lower = window_level - window_width / 2
        upper = window_level + window_width / 2
        modified = np.clip(modified, lower, upper)
        print(f"Applied window: width={window_width}, level={window_level}")
    
    return modified


