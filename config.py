"""
Configuration settings for 3DNavi Manufacturing Platform
"""

# Server Configuration
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 12000
DEBUG_MODE = True

# Application Settings
APP_TITLE = "3DNavi - On-Demand Manufacturing Platform"
APP_DESCRIPTION = "Modern on-demand manufacturing with real-time 3D visualization"

# Pricing Configuration
BASE_PRICE = 0.001  # Base price per cubic mm (more realistic pricing)

# Material pricing multipliers
MATERIAL_MULTIPLIERS = {
    "aluminum": 1.0,
    "steel": 1.2,
    "titanium": 3.0,
    "plastic": 0.5
}

# Surface treatment pricing multipliers
SURFACE_TREATMENT_MULTIPLIERS = {
    "none": 1.0,
    "anodizing": 1.3,
    "powder_coating": 1.2,
    "machining": 1.5
}

# Manufacturing Settings
DEFAULT_DELIVERY_TIME = "5-7 business days"
MAX_QUANTITY = 10000
MIN_DIMENSION = 0.1  # mm
MAX_DIMENSION = 1000  # mm

# 3D Renderer Settings
DEFAULT_DIMENSIONS = {
    "length": 100.0,
    "width": 50.0,
    "thickness": 5.0,
    "hole_diameter": 10.0
}

# Material colors for 3D visualization (hex values)
MATERIAL_COLORS = {
    "aluminum": 0xc0c0c0,
    "steel": 0x808080,
    "titanium": 0xa0a0a0,
    "plastic": 0x4a90e2
}