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


