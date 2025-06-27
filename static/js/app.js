class App {
    constructor() {
        this.form = document.getElementById('config-form');
        this.quoteResult = document.getElementById('quote-result');
        this.quoteContent = document.getElementById('quote-content');
        
        this.setupEventHandlers();
    }
    
    setupEventHandlers() {
        this.form.addEventListener('submit', (e) => {
            e.preventDefault();
            this.submitConfiguration();
        });
        
        // Real-time updates for material selection
        document.getElementById('material').addEventListener('change', (e) => {
            this.updateMaterialVisualization(e.target.value);
        });
    }
    
    async submitConfiguration() {
        const formData = new FormData(this.form);
        
        // Show loading state
        this.showLoading();
        
        try {
            const response = await fetch('/configure', {
                method: 'POST',
                body: formData
            });
            
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            
            const result = await response.json();
            this.displayQuote(result);
            
        } catch (error) {
            console.error('Error:', error);
            this.showError('Failed to get quote. Please try again.');
        }
    }
    
    showLoading() {
        this.quoteResult.classList.remove('hidden', 'error');
        this.quoteContent.innerHTML = '<div class="loading">Calculating quote...</div>';
    }
    
    showError(message) {
        this.quoteResult.classList.remove('hidden');
        this.quoteResult.classList.add('error');
        this.quoteContent.innerHTML = `<div class="error">${message}</div>`;
    }
    
    displayQuote(result) {
        this.quoteResult.classList.remove('hidden', 'error');
        
        const config = result.configuration;
        const dimensions = config.dimensions;
        
        this.quoteContent.innerHTML = `
            <div class="quote-item">
                <span>Material:</span>
                <span>${this.capitalizeFirst(config.material)}</span>
            </div>
            <div class="quote-item">
                <span>Surface Treatment:</span>
                <span>${this.capitalizeFirst(config.surface_treatment.replace('_', ' '))}</span>
            </div>
            <div class="quote-item">
                <span>Dimensions:</span>
                <span>${dimensions.length} × ${dimensions.width} × ${dimensions.thickness} mm</span>
            </div>
            <div class="quote-item">
                <span>Hole Diameter:</span>
                <span>${dimensions.hole_diameter} mm</span>
            </div>
            <div class="quote-item">
                <span>Quantity:</span>
                <span>${config.quantity}</span>
            </div>
            <div class="quote-item">
                <span>Estimated Delivery:</span>
                <span>${result.estimated_delivery}</span>
            </div>
            <div class="quote-item">
                <span><strong>Total Price:</strong></span>
                <span><strong>$${result.estimated_price}</strong></span>
            </div>
        `;
    }
    
    updateMaterialVisualization(material) {
        if (!threeRenderer || !threeRenderer.plate) return;
        
        const materialColors = {
            'aluminum': 0xc0c0c0,
            'steel': 0x808080,
            'titanium': 0xa0a0a0,
            'plastic': 0x4a90e2
        };
        
        const color = materialColors[material] || 0x888888;
        threeRenderer.plate.material.color.setHex(color);
    }
    
    capitalizeFirst(str) {
        return str.charAt(0).toUpperCase() + str.slice(1);
    }
}

// Initialize the app when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new App();
});