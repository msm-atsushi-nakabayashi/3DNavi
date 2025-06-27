#!/usr/bin/env python3
"""
Simple API test script to verify the 3DNavi application is working correctly.
Run this script to test the API endpoints manually.
"""

import requests
import json
import time

BASE_URL = "http://localhost:12000"

def test_health_endpoint():
    """Test the health check endpoint"""
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed:", response.json())
        else:
            print("❌ Health check failed:", response.status_code)
    except Exception as e:
        print("❌ Health check error:", str(e))

def test_home_page():
    """Test the home page"""
    print("\nTesting home page...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200 and "3DNavi" in response.text:
            print("✅ Home page loaded successfully")
        else:
            print("❌ Home page failed:", response.status_code)
    except Exception as e:
        print("❌ Home page error:", str(e))

def test_configuration_endpoint():
    """Test the configuration endpoint"""
    print("\nTesting configuration endpoint...")
    
    test_configs = [
        {
            "name": "Aluminum plate with anodizing",
            "data": {
                "material": "aluminum",
                "surface_treatment": "anodizing",
                "length": 100.0,
                "width": 50.0,
                "thickness": 5.0,
                "hole_diameter": 10.0,
                "quantity": 1
            }
        },
        {
            "name": "Steel plate with powder coating",
            "data": {
                "material": "steel",
                "surface_treatment": "powder_coating",
                "length": 200.0,
                "width": 100.0,
                "thickness": 10.0,
                "hole_diameter": 20.0,
                "quantity": 5
            }
        },
        {
            "name": "Titanium plate with machining",
            "data": {
                "material": "titanium",
                "surface_treatment": "machining",
                "length": 75.0,
                "width": 75.0,
                "thickness": 3.0,
                "hole_diameter": 8.0,
                "quantity": 2
            }
        }
    ]
    
    for config in test_configs:
        print(f"\n  Testing: {config['name']}")
        try:
            response = requests.post(f"{BASE_URL}/configure", data=config['data'])
            if response.status_code == 200:
                result = response.json()
                print(f"  ✅ Configuration successful")
                print(f"     Material: {result['configuration']['material']}")
                print(f"     Price: ${result['estimated_price']}")
                print(f"     Delivery: {result['estimated_delivery']}")
            else:
                print(f"  ❌ Configuration failed: {response.status_code}")
        except Exception as e:
            print(f"  ❌ Configuration error: {str(e)}")

def test_static_files():
    """Test static file access"""
    print("\nTesting static files...")
    
    static_files = [
        "/static/css/style.css",
        "/static/js/app.js",
        "/static/js/three-renderer.js"
    ]
    
    for file_path in static_files:
        try:
            response = requests.get(f"{BASE_URL}{file_path}")
            if response.status_code == 200:
                print(f"  ✅ {file_path} accessible")
            else:
                print(f"  ❌ {file_path} failed: {response.status_code}")
        except Exception as e:
            print(f"  ❌ {file_path} error: {str(e)}")

def main():
    print("🚀 Starting 3DNavi API Tests")
    print("=" * 50)
    
    # Wait a moment for server to be ready
    time.sleep(1)
    
    test_health_endpoint()
    test_home_page()
    test_configuration_endpoint()
    test_static_files()
    
    print("\n" + "=" * 50)
    print("✨ API tests completed!")
    print("\n🌐 You can now access the application at:")
    print(f"   {BASE_URL}")
    print("\n📝 Or use the external URL:")
    print("   https://work-1-nqrqnrulfiwdqxwt.prod-runtime.all-hands.dev")

if __name__ == "__main__":
    main()