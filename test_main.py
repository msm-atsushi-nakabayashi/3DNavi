import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_home_page():
    """Test that the home page loads correctly"""
    response = client.get("/")
    assert response.status_code == 200
    assert "3DNavi" in response.text
    assert "On-Demand Manufacturing Platform" in response.text

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_configure_part_valid_data():
    """Test part configuration with valid data"""
    form_data = {
        "material": "aluminum",
        "surface_treatment": "anodizing",
        "length": 100.0,
        "width": 50.0,
        "thickness": 5.0,
        "hole_diameter": 10.0,
        "quantity": 1
    }
    
    response = client.post("/configure", data=form_data)
    assert response.status_code == 200
    
    result = response.json()
    assert result["status"] == "success"
    assert "configuration" in result
    assert "estimated_price" in result
    assert "estimated_delivery" in result
    
    # Check configuration details
    config = result["configuration"]
    assert config["material"] == "aluminum"
    assert config["surface_treatment"] == "anodizing"
    assert config["quantity"] == 1
    
    # Check dimensions
    dimensions = config["dimensions"]
    assert dimensions["length"] == 100.0
    assert dimensions["width"] == 50.0
    assert dimensions["thickness"] == 5.0
    assert dimensions["hole_diameter"] == 10.0

def test_configure_part_different_materials():
    """Test configuration with different materials"""
    materials = ["aluminum", "steel", "titanium", "plastic"]
    
    for material in materials:
        form_data = {
            "material": material,
            "surface_treatment": "none",
            "length": 50.0,
            "width": 25.0,
            "thickness": 2.0,
            "hole_diameter": 5.0,
            "quantity": 1
        }
        
        response = client.post("/configure", data=form_data)
        assert response.status_code == 200
        
        result = response.json()
        assert result["status"] == "success"
        assert result["configuration"]["material"] == material

def test_configure_part_different_surface_treatments():
    """Test configuration with different surface treatments"""
    treatments = ["none", "anodizing", "powder_coating", "machining"]
    
    for treatment in treatments:
        form_data = {
            "material": "aluminum",
            "surface_treatment": treatment,
            "length": 50.0,
            "width": 25.0,
            "thickness": 2.0,
            "hole_diameter": 5.0,
            "quantity": 1
        }
        
        response = client.post("/configure", data=form_data)
        assert response.status_code == 200
        
        result = response.json()
        assert result["status"] == "success"
        assert result["configuration"]["surface_treatment"] == treatment

def test_configure_part_price_calculation():
    """Test that price calculation works correctly"""
    # Test with aluminum and no surface treatment (baseline)
    form_data_baseline = {
        "material": "aluminum",
        "surface_treatment": "none",
        "length": 10.0,
        "width": 10.0,
        "thickness": 1.0,
        "hole_diameter": 2.0,
        "quantity": 1
    }
    
    response_baseline = client.post("/configure", data=form_data_baseline)
    baseline_price = response_baseline.json()["estimated_price"]
    
    # Test with titanium (should be more expensive)
    form_data_titanium = form_data_baseline.copy()
    form_data_titanium["material"] = "titanium"
    
    response_titanium = client.post("/configure", data=form_data_titanium)
    titanium_price = response_titanium.json()["estimated_price"]
    
    assert titanium_price > baseline_price
    
    # Test with surface treatment (should be more expensive)
    form_data_treated = form_data_baseline.copy()
    form_data_treated["surface_treatment"] = "anodizing"
    
    response_treated = client.post("/configure", data=form_data_treated)
    treated_price = response_treated.json()["estimated_price"]
    
    assert treated_price > baseline_price
    
    # Test with higher quantity (should be proportionally more expensive)
    form_data_quantity = form_data_baseline.copy()
    form_data_quantity["quantity"] = 5
    
    response_quantity = client.post("/configure", data=form_data_quantity)
    quantity_price = response_quantity.json()["estimated_price"]
    
    assert quantity_price > baseline_price

def test_configure_part_missing_fields():
    """Test configuration with missing required fields"""
    # Missing material
    form_data = {
        "surface_treatment": "none",
        "length": 50.0,
        "width": 25.0,
        "thickness": 2.0,
        "hole_diameter": 5.0,
        "quantity": 1
    }
    
    response = client.post("/configure", data=form_data)
    assert response.status_code == 422  # Unprocessable Entity

def test_configure_part_edge_cases():
    """Test configuration with edge case values"""
    # Very small dimensions
    form_data_small = {
        "material": "plastic",
        "surface_treatment": "none",
        "length": 0.1,
        "width": 0.1,
        "thickness": 0.1,
        "hole_diameter": 0.05,
        "quantity": 1
    }
    
    response = client.post("/configure", data=form_data_small)
    assert response.status_code == 200
    
    # Large quantity
    form_data_large_qty = {
        "material": "aluminum",
        "surface_treatment": "none",
        "length": 10.0,
        "width": 10.0,
        "thickness": 1.0,
        "hole_diameter": 2.0,
        "quantity": 1000
    }
    
    response = client.post("/configure", data=form_data_large_qty)
    assert response.status_code == 200
    result = response.json()
    assert result["configuration"]["quantity"] == 1000

def test_static_files_accessible():
    """Test that static files are accessible"""
    # Test CSS file
    response = client.get("/static/css/style.css")
    assert response.status_code == 200
    
    # Test JavaScript files
    response = client.get("/static/js/app.js")
    assert response.status_code == 200
    
    response = client.get("/static/js/three-renderer.js")
    assert response.status_code == 200

def test_price_precision():
    """Test that prices are properly rounded to 2 decimal places"""
    form_data = {
        "material": "aluminum",
        "surface_treatment": "none",
        "length": 33.33,
        "width": 33.33,
        "thickness": 3.33,
        "hole_diameter": 5.0,
        "quantity": 3
    }
    
    response = client.post("/configure", data=form_data)
    assert response.status_code == 200
    
    result = response.json()
    price = result["estimated_price"]
    
    # Check that price has at most 2 decimal places
    assert len(str(price).split('.')[-1]) <= 2

if __name__ == "__main__":
    pytest.main([__file__, "-v"])