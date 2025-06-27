from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional
import uvicorn
import config

app = FastAPI(
    title=config.APP_TITLE,
    description=config.APP_DESCRIPTION
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Main page with 3D renderer and configuration form"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/configure")
async def configure_part(
    material: str = Form(...),
    surface_treatment: str = Form(...),
    length: float = Form(...),
    width: float = Form(...),
    thickness: float = Form(...),
    hole_diameter: float = Form(...),
    quantity: int = Form(...)
):
    """Handle part configuration submission"""
    configuration = {
        "material": material,
        "surface_treatment": surface_treatment,
        "dimensions": {
            "length": length,
            "width": width,
            "thickness": thickness,
            "hole_diameter": hole_diameter
        },
        "quantity": quantity
    }
    
    # Calculate estimated price using configuration
    base_price = config.BASE_PRICE
    material_multiplier = config.MATERIAL_MULTIPLIERS.get(material.lower(), 1.0)
    surface_multiplier = config.SURFACE_TREATMENT_MULTIPLIERS.get(surface_treatment.lower(), 1.0)
    
    volume = length * width * thickness
    estimated_price = base_price * material_multiplier * surface_multiplier * volume * quantity
    
    return {
        "status": "success",
        "configuration": configuration,
        "estimated_price": round(estimated_price, 2),
        "estimated_delivery": config.DEFAULT_DELIVERY_TIME
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=config.SERVER_HOST,
        port=config.SERVER_PORT,
        reload=config.DEBUG_MODE,
        access_log=True
    )