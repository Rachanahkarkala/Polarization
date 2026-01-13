import numpy as np
from PIL import Image
from typing import Dict

class PolarizationProcessor:
    @staticmethod
    def compute_stokes_single(images: list) -> np.ndarray:
        """Compute Stokes parameters from 4 polarization images"""
        if len(images) != 4:
            raise ValueError("Need exactly 4 images for Stokes computation")
            
        I0, I45, I90, I135 = images
        
        # Compute Stokes parameters
        S0 = (I0 + I45 + I90 + I135) / 2
        S1 = I0 - I90
        S2 = I45 - I135
        
        return np.stack([S0, S1, S2], axis=-1)
    
    @staticmethod
    def compute_stokes_dual(I0: np.ndarray, I90: np.ndarray) -> np.ndarray:
        """Compute Stokes parameters from 2 images (0° and 90°)"""
        S0 = I0 + I90
        S1 = I0 - I90
        S2 = np.zeros_like(S0)
        
        return np.stack([S0, S1, S2], axis=-1)
    
    @staticmethod
    def compute_polarization_metrics(stokes: np.ndarray) -> Dict[str, np.ndarray]:
        """Compute all polarization metrics from Stokes parameters"""
        S0, S1, S2 = stokes[..., 0], stokes[..., 1], stokes[..., 2]
        
        # Avoid division by zero
        S0_safe = S0 + 1e-8
        
        # Degree of Polarization (DOP)
        dop = np.sqrt(S1**2 + S2**2) / S0_safe
        
        # Orientation Angle (OA) in degrees
        orientation_angle = 0.5 * np.arctan2(S2, S1 + 1e-8) * (180 / np.pi)
        
        # Ellipticity Angle (EA) in degrees
        ellipticity_angle = 0.5 * np.arcsin(S2 / (dop * S0_safe + 1e-8)) * (180 / np.pi)
        ellipticity_angle = np.nan_to_num(ellipticity_angle, nan=0.0)
        
        return {
            'dop': np.clip(dop, 0, 1),
            'orientation_angle': orientation_angle,
            'ellipticity_angle': ellipticity_angle,
            'S0': S0,
            'S1': S1,
            'S2': S2
        }
