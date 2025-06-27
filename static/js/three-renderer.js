class ThreeRenderer {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.controls = null;
        this.plate = null;
        this.wireframeMode = false;
        
        this.init();
        this.createPlate();
        this.animate();
        
        // Bind event handlers
        this.setupEventHandlers();
    }
    
    init() {
        // Scene
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0xf0f0f0);
        
        // Camera
        this.camera = new THREE.PerspectiveCamera(
            75,
            this.container.clientWidth / this.container.clientHeight,
            0.1,
            1000
        );
        this.camera.position.set(150, 100, 150);
        
        // Renderer
        this.renderer = new THREE.WebGLRenderer({ antialias: true });
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        this.container.appendChild(this.renderer.domElement);
        
        // Controls
        this.controls = new THREE.OrbitControls(this.camera, this.renderer.domElement);
        this.controls.enableDamping = true;
        this.controls.dampingFactor = 0.05;
        
        // Lighting
        this.setupLighting();
        
        // Handle window resize
        window.addEventListener('resize', () => this.onWindowResize());
    }
    
    setupLighting() {
        // Ambient light
        const ambientLight = new THREE.AmbientLight(0x404040, 0.6);
        this.scene.add(ambientLight);
        
        // Directional light
        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
        directionalLight.position.set(100, 100, 50);
        directionalLight.castShadow = true;
        directionalLight.shadow.mapSize.width = 2048;
        directionalLight.shadow.mapSize.height = 2048;
        this.scene.add(directionalLight);
        
        // Point light for better illumination
        const pointLight = new THREE.PointLight(0xffffff, 0.5);
        pointLight.position.set(-50, 50, 50);
        this.scene.add(pointLight);
    }
    
    createPlate(length = 100, width = 50, thickness = 5, holeDiameter = 10) {
        // Remove existing plate
        if (this.plate) {
            this.scene.remove(this.plate);
        }
        
        // Create plate geometry with hole
        const plateShape = new THREE.Shape();
        plateShape.moveTo(-length/2, -width/2);
        plateShape.lineTo(length/2, -width/2);
        plateShape.lineTo(length/2, width/2);
        plateShape.lineTo(-length/2, width/2);
        plateShape.lineTo(-length/2, -width/2);
        
        // Create hole
        const holeShape = new THREE.Path();
        holeShape.absarc(0, 0, holeDiameter/2, 0, Math.PI * 2, false);
        plateShape.holes.push(holeShape);
        
        // Extrude the shape
        const extrudeSettings = {
            depth: thickness,
            bevelEnabled: true,
            bevelSegments: 2,
            steps: 2,
            bevelSize: 0.5,
            bevelThickness: 0.5
        };
        
        const geometry = new THREE.ExtrudeGeometry(plateShape, extrudeSettings);
        
        // Center the geometry
        geometry.translate(0, 0, -thickness/2);
        
        // Material
        const material = new THREE.MeshLambertMaterial({
            color: 0x888888,
            transparent: true,
            opacity: 0.9
        });
        
        // Create mesh
        this.plate = new THREE.Mesh(geometry, material);
        this.plate.castShadow = true;
        this.plate.receiveShadow = true;
        
        this.scene.add(this.plate);
        
        // Add coordinate system helper
        this.addCoordinateSystem();
    }
    
    addCoordinateSystem() {
        // Remove existing axes
        const existingAxes = this.scene.getObjectByName('axes');
        if (existingAxes) {
            this.scene.remove(existingAxes);
        }
        
        const axesHelper = new THREE.AxesHelper(75);
        axesHelper.name = 'axes';
        this.scene.add(axesHelper);
    }
    
    updatePlate(dimensions) {
        const { length, width, thickness, hole_diameter } = dimensions;
        this.createPlate(length, width, thickness, hole_diameter);
    }
    
    toggleWireframe() {
        this.wireframeMode = !this.wireframeMode;
        if (this.plate) {
            this.plate.material.wireframe = this.wireframeMode;
        }
    }
    
    resetView() {
        this.camera.position.set(150, 100, 150);
        this.controls.reset();
    }
    
    setupEventHandlers() {
        // Reset view button
        document.getElementById('reset-view')?.addEventListener('click', () => {
            this.resetView();
        });
        
        // Wireframe toggle button
        document.getElementById('wireframe-toggle')?.addEventListener('click', () => {
            this.toggleWireframe();
        });
        
        // Listen for dimension changes
        const dimensionInputs = ['length', 'width', 'thickness', 'hole_diameter'];
        dimensionInputs.forEach(inputId => {
            const input = document.getElementById(inputId);
            if (input) {
                input.addEventListener('input', () => {
                    this.updateFromForm();
                });
            }
        });
    }
    
    updateFromForm() {
        const dimensions = {
            length: parseFloat(document.getElementById('length').value) || 100,
            width: parseFloat(document.getElementById('width').value) || 50,
            thickness: parseFloat(document.getElementById('thickness').value) || 5,
            hole_diameter: parseFloat(document.getElementById('hole_diameter').value) || 10
        };
        
        this.updatePlate(dimensions);
    }
    
    onWindowResize() {
        this.camera.aspect = this.container.clientWidth / this.container.clientHeight;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
    }
    
    animate() {
        requestAnimationFrame(() => this.animate());
        
        this.controls.update();
        this.renderer.render(this.scene, this.camera);
    }
}

// Initialize the renderer when the page loads
let threeRenderer;
document.addEventListener('DOMContentLoaded', () => {
    threeRenderer = new ThreeRenderer('three-container');
});