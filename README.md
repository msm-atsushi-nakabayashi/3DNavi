# 3DNavi - On-Demand Manufacturing Platform

A modern web application for on-demand manufacturing with real-time 3D visualization and instant quoting.

## Features

- **Interactive 3D Renderer**: Real-time visualization of flat plates with holes using Three.js
- **Dynamic Configuration**: Adjust material, surface treatment, dimensions, and quantity
- **Instant Quoting**: Get immediate price estimates based on your specifications
- **Responsive Design**: Works on desktop and mobile devices
- **RESTful API**: Clean API endpoints for integration

## Technology Stack

- **Backend**: FastAPI with Uvicorn
- **Frontend**: HTML5, CSS3, JavaScript
- **3D Rendering**: Three.js
- **Testing**: Pytest
- **Styling**: Modern CSS with gradients and animations

## Quick Start

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd 3DNavi
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

4. Open your browser and navigate to:
   - Local: http://localhost:12000
   - External: https://work-1-nqrqnrulfiwdqxwt.prod-runtime.all-hands.dev

## Testing

Run the comprehensive test suite:

```bash
# Run unit tests
python -m pytest test_main.py -v

# Run API integration tests
python test_api.py
```

## API Endpoints

### GET /
Returns the main application page with 3D renderer and configuration form.

### POST /configure
Submit part configuration and get instant quote.

**Parameters:**
- `material`: aluminum, steel, titanium, plastic
- `surface_treatment`: none, anodizing, powder_coating, machining
- `length`: Length in mm (float)
- `width`: Width in mm (float)
- `thickness`: Thickness in mm (float)
- `hole_diameter`: Hole diameter in mm (float)
- `quantity`: Number of parts (integer)

**Response:**
```json
{
  "status": "success",
  "configuration": {
    "material": "aluminum",
    "surface_treatment": "anodizing",
    "dimensions": {
      "length": 100.0,
      "width": 50.0,
      "thickness": 5.0,
      "hole_diameter": 10.0
    },
    "quantity": 1
  },
  "estimated_price": 325.00,
  "estimated_delivery": "5-7 business days"
}
```

### GET /health
Health check endpoint for monitoring.

## 3D Renderer Features

- **Real-time Updates**: Dimensions update the 3D model instantly
- **Interactive Controls**: Orbit, zoom, and pan around the model
- **Material Visualization**: Different materials show different colors
- **Wireframe Mode**: Toggle between solid and wireframe view
- **Reset View**: Return to default camera position

## Project Structure

```
3DNavi/
├── main.py                 # FastAPI application
├── requirements.txt        # Python dependencies
├── test_main.py           # Unit tests
├── test_api.py            # API integration tests
├── templates/
│   └── index.html         # Main application template
├── static/
│   ├── css/
│   │   └── style.css      # Application styles
│   └── js/
│       ├── app.js         # Main application logic
│       └── three-renderer.js  # 3D rendering logic
└── README.md              # This file
```

## Development

### Adding New Materials

1. Update the material options in `templates/index.html`
2. Add material multiplier in `main.py` configure_part function
3. Add material color in `static/js/app.js` updateMaterialVisualization function

### Adding New Surface Treatments

1. Update surface treatment options in `templates/index.html`
2. Add surface multiplier in `main.py` configure_part function

### Customizing 3D Models

The 3D renderer is modular and can be extended to support different part geometries by modifying the `ThreeRenderer` class in `static/js/three-renderer.js`.

## Deployment

The application is configured to run on port 12000 and accepts connections from any host (0.0.0.0). For production deployment:

1. Set up a reverse proxy (nginx/Apache)
2. Configure SSL certificates
3. Set up environment variables for configuration
4. Consider using a production ASGI server like Gunicorn

## License

This project is open source and available under the MIT License.