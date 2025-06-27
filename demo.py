#!/usr/bin/env python3
"""
3DNavi Demo Script
Demonstrates the key features of the 3DNavi manufacturing platform
"""

import requests
import json
import time
from typing import Dict, Any

BASE_URL = "http://localhost:12000"

def print_header(title: str):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"🔧 {title}")
    print("=" * 60)

def print_quote(config: Dict[str, Any], result: Dict[str, Any]):
    """Print a formatted quote"""
    print(f"\n📋 Configuration:")
    print(f"   Material: {config['material'].title()}")
    print(f"   Surface Treatment: {config['surface_treatment'].replace('_', ' ').title()}")
    print(f"   Dimensions: {config['length']}×{config['width']}×{config['thickness']} mm")
    print(f"   Hole Diameter: {config['hole_diameter']} mm")
    print(f"   Quantity: {config['quantity']}")
    
    print(f"\n💰 Quote:")
    print(f"   Price: ${result['estimated_price']}")
    print(f"   Delivery: {result['estimated_delivery']}")

def demo_basic_configuration():
    """Demo basic part configuration"""
    print_header("Basic Part Configuration")
    
    config = {
        "material": "aluminum",
        "surface_treatment": "none",
        "length": 100.0,
        "width": 50.0,
        "thickness": 5.0,
        "hole_diameter": 10.0,
        "quantity": 1
    }
    
    response = requests.post(f"{BASE_URL}/configure", data=config)
    result = response.json()
    
    print_quote(config, result)

def demo_premium_materials():
    """Demo premium materials comparison"""
    print_header("Premium Materials Comparison")
    
    base_config = {
        "surface_treatment": "anodizing",
        "length": 75.0,
        "width": 75.0,
        "thickness": 3.0,
        "hole_diameter": 8.0,
        "quantity": 1
    }
    
    materials = ["aluminum", "steel", "titanium"]
    
    for material in materials:
        config = base_config.copy()
        config["material"] = material
        
        response = requests.post(f"{BASE_URL}/configure", data=config)
        result = response.json()
        
        print(f"\n🔹 {material.title()}:")
        print(f"   Price: ${result['estimated_price']}")

def demo_surface_treatments():
    """Demo different surface treatments"""
    print_header("Surface Treatment Options")
    
    base_config = {
        "material": "aluminum",
        "length": 50.0,
        "width": 50.0,
        "thickness": 2.0,
        "hole_diameter": 5.0,
        "quantity": 1
    }
    
    treatments = [
        ("none", "Raw Material"),
        ("anodizing", "Anodized Finish"),
        ("powder_coating", "Powder Coated"),
        ("machining", "Precision Machined")
    ]
    
    for treatment_code, treatment_name in treatments:
        config = base_config.copy()
        config["surface_treatment"] = treatment_code
        
        response = requests.post(f"{BASE_URL}/configure", data=config)
        result = response.json()
        
        print(f"\n🔹 {treatment_name}:")
        print(f"   Price: ${result['estimated_price']}")

def demo_bulk_pricing():
    """Demo bulk quantity pricing"""
    print_header("Bulk Quantity Pricing")
    
    config = {
        "material": "steel",
        "surface_treatment": "powder_coating",
        "length": 80.0,
        "width": 40.0,
        "thickness": 4.0,
        "hole_diameter": 6.0,
        "quantity": 1
    }
    
    quantities = [1, 10, 50, 100]
    
    for qty in quantities:
        config["quantity"] = qty
        
        response = requests.post(f"{BASE_URL}/configure", data=config)
        result = response.json()
        
        unit_price = result['estimated_price'] / qty
        
        print(f"\n🔹 Quantity {qty}:")
        print(f"   Total Price: ${result['estimated_price']}")
        print(f"   Unit Price: ${unit_price:.2f}")

def demo_custom_dimensions():
    """Demo custom dimension configurations"""
    print_header("Custom Dimension Examples")
    
    examples = [
        {
            "name": "Small Precision Part",
            "config": {
                "material": "titanium",
                "surface_treatment": "machining",
                "length": 25.0,
                "width": 15.0,
                "thickness": 1.5,
                "hole_diameter": 2.0,
                "quantity": 5
            }
        },
        {
            "name": "Large Industrial Plate",
            "config": {
                "material": "steel",
                "surface_treatment": "powder_coating",
                "length": 500.0,
                "width": 300.0,
                "thickness": 20.0,
                "hole_diameter": 50.0,
                "quantity": 2
            }
        },
        {
            "name": "Lightweight Plastic Component",
            "config": {
                "material": "plastic",
                "surface_treatment": "none",
                "length": 120.0,
                "width": 80.0,
                "thickness": 8.0,
                "hole_diameter": 15.0,
                "quantity": 25
            }
        }
    ]
    
    for example in examples:
        response = requests.post(f"{BASE_URL}/configure", data=example["config"])
        result = response.json()
        
        print(f"\n🔹 {example['name']}:")
        print(f"   Dimensions: {example['config']['length']}×{example['config']['width']}×{example['config']['thickness']} mm")
        print(f"   Material: {example['config']['material'].title()}")
        print(f"   Quantity: {example['config']['quantity']}")
        print(f"   Total Price: ${result['estimated_price']}")

def main():
    """Run the complete demo"""
    print("🚀 3DNavi Manufacturing Platform Demo")
    print("🌐 Application running at: http://localhost:12000")
    print("📱 External access: https://work-1-nqrqnrulfiwdqxwt.prod-runtime.all-hands.dev")
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code != 200:
            print("❌ Server is not responding. Please start the server first.")
            return
    except requests.exceptions.RequestException:
        print("❌ Cannot connect to server. Please start the server first.")
        print("💡 Run: python main.py")
        return
    
    print("✅ Server is running!")
    
    # Run demos
    demo_basic_configuration()
    demo_premium_materials()
    demo_surface_treatments()
    demo_bulk_pricing()
    demo_custom_dimensions()
    
    print_header("Demo Complete")
    print("🎉 Thank you for exploring 3DNavi!")
    print("🔗 Visit the web interface to try the interactive 3D renderer")
    print("📚 Check README.md for more information")

if __name__ == "__main__":
    main()