/**
 * Intellect Homes - Interactive 3D Architectural Studio (WebGL Three.js)
 * High-performance 3D House Visualizer, Material Configurator, Lighting Studio & 360 Panorama
 */

(function () {
  'use strict';

  let scene, camera, renderer, controls;
  let houseGroup, lightsGroup;
  let dirLight, ambientLight, duskLights = [];
  let currentMode = 'dusk'; // 'day', 'golden', 'dusk'
  let currentRenderColor = 0x2A2E35; // Charcoal default
  let currentWoodColor = 0x8D5B36; // Teak/Cedar default
  let currentBalconyStyle = 'glass'; // 'glass' or 'battens'
  let isAutoRotate = true;
  let canvasContainer;
  let hotspotElements = [];

  // Hotspots definition in 3D world space
  const hotspotsData = [
    {
      id: 'glazing',
      title: '7-Star NatHERS Double Glazing',
      desc: 'Commercial acoustic aluminium frames with argon-gas insulated double glazing.',
      pos: new THREE.Vector3(2.6, 2.8, 3.1)
    },
    {
      id: 'battens',
      title: 'Bespoke Cedar Screening',
      desc: 'Natural Australian timber battens providing thermal shading and architectural contrast.',
      pos: new THREE.Vector3(-1.8, 3.4, 3.1)
    },
    {
      id: 'portico',
      title: 'Grand Integrated Portico',
      desc: 'Recessed sheltered entry with flush-mount downlights and keyless digital access.',
      pos: new THREE.Vector3(0.3, 1.2, 3.6)
    },
    {
      id: 'cantilever',
      title: 'Cantilever Master Wing',
      desc: 'Architectural overhang extending 2.4m over the ground living zone with concealed structural steel.',
      pos: new THREE.Vector3(-2.2, 4.2, 1.0)
    }
  ];

  let houseMaterials = {};

  function init3DStudio() {
    canvasContainer = document.getElementById('architectural3DCanvas');
    if (!canvasContainer || typeof THREE === 'undefined') return;

    const width = canvasContainer.clientWidth || 900;
    const height = canvasContainer.clientHeight || 580;

    // 1. Scene setup
    scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x0a0e17, 0.025);

    // 2. Camera setup
    camera = new THREE.PerspectiveCamera(42, width / height, 0.1, 100);
    camera.position.set(11, 7, 13);

    // 3. Renderer setup
    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'high-performance' });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.15;
    canvasContainer.innerHTML = '';
    canvasContainer.appendChild(renderer.domElement);

    // 4. Controls
    if (typeof THREE.OrbitControls !== 'undefined') {
      controls = new THREE.OrbitControls(camera, renderer.domElement);
      controls.enableDamping = true;
      controls.dampingFactor = 0.05;
      controls.maxPolarAngle = Math.PI / 2 - 0.04; // Don't go below ground
      controls.minDistance = 6;
      controls.maxDistance = 24;
      controls.target.set(0, 2.2, 0);
    }

    // 5. Lighting Setup
    setupLighting();

    // 6. Build Architectural House Model
    buildArchitecturalHouse();

    // 7. Setup 3D Hotspot DOM Elements
    createHotspotsDOM();

    // 8. Event Listeners (Resize, UI Buttons)
    window.addEventListener('resize', onWindowResize);
    bindUIControls();

    // Set initial lighting preset (Dusk)
    setLightingMode('dusk');

    // 9. Start Animation Loop
    animate();
  }

  function setupLighting() {
    lightsGroup = new THREE.Group();

    ambientLight = new THREE.AmbientLight(0x3a4b63, 1.2);
    lightsGroup.add(ambientLight);

    dirLight = new THREE.DirectionalLight(0xfff5e6, 2.0);
    dirLight.position.set(14, 18, 12);
    dirLight.castShadow = true;
    dirLight.shadow.mapSize.width = 2048;
    dirLight.shadow.mapSize.height = 2048;
    dirLight.shadow.camera.near = 0.5;
    dirLight.shadow.camera.far = 45;
    dirLight.shadow.bias = -0.0005;
    const d = 12;
    dirLight.shadow.camera.left = -d;
    dirLight.shadow.camera.right = d;
    dirLight.shadow.camera.top = d;
    dirLight.shadow.camera.bottom = -d;
    lightsGroup.add(dirLight);

    // Secondary soft fill light
    const fillLight = new THREE.DirectionalLight(0x7395c2, 0.7);
    fillLight.position.set(-12, 10, -10);
    lightsGroup.add(fillLight);

    // Dusk / Night architectural facade spotlights
    const spotCoords = [
      { x: 0.3, y: 2.2, z: 3.5, color: 0xffb85c, intensity: 3.5, dist: 6 },
      { x: -3.5, y: 0.4, z: 4.0, color: 0xffd285, intensity: 4.0, dist: 5 }, // Ground uplight left
      { x: 3.5, y: 0.4, z: 4.0, color: 0xffd285, intensity: 4.0, dist: 5 },  // Ground uplight right
      { x: 1.8, y: 2.5, z: 0.5, color: 0xffa43c, intensity: 2.8, dist: 7 },  // Interior warm glow
      { x: -1.5, y: 3.5, z: 1.0, color: 0xffa43c, intensity: 3.0, dist: 7 }  // Upper interior glow
    ];

    spotCoords.forEach(c => {
      const pLight = new THREE.PointLight(c.color, c.intensity, c.dist, 2);
      pLight.position.set(c.x, c.y, c.z);
      lightsGroup.add(pLight);
      duskLights.push(pLight);
    });

    scene.add(lightsGroup);
  }

  function buildArchitecturalHouse() {
    houseGroup = new THREE.Group();

    // Reusable Materials
    houseMaterials.wallMain = new THREE.MeshStandardMaterial({
      color: currentRenderColor,
      roughness: 0.75,
      metalness: 0.1
    });

    houseMaterials.wallSecondary = new THREE.MeshStandardMaterial({
      color: 0x1C2026,
      roughness: 0.85,
      metalness: 0.15
    });

    houseMaterials.timber = new THREE.MeshStandardMaterial({
      color: currentWoodColor,
      roughness: 0.5,
      metalness: 0.05
    });

    houseMaterials.stone = new THREE.MeshStandardMaterial({
      color: 0x363A40,
      roughness: 0.9,
      metalness: 0.05
    });

    houseMaterials.glass = new THREE.MeshStandardMaterial({
      color: 0x88BBDD,
      roughness: 0.1,
      metalness: 0.85,
      transparent: true,
      opacity: 0.48
    });

    houseMaterials.interiorWarm = new THREE.MeshStandardMaterial({
      color: 0xFFE0B2,
      emissive: 0xDF982B,
      emissiveIntensity: 0.4,
      roughness: 0.3
    });

    houseMaterials.blackTrim = new THREE.MeshStandardMaterial({
      color: 0x111317,
      roughness: 0.4,
      metalness: 0.6
    });

    houseMaterials.concrete = new THREE.MeshStandardMaterial({
      color: 0xD0D4DC,
      roughness: 0.8,
      metalness: 0.05
    });

    houseMaterials.grass = new THREE.MeshStandardMaterial({
      color: 0x223B25,
      roughness: 0.95,
      metalness: 0.0
    });

    // 1. Ground Slab & Paved Alfresco
    const slabGeo = new THREE.BoxGeometry(14, 0.3, 14);
    const slabMesh = new THREE.Mesh(slabGeo, houseMaterials.concrete);
    slabMesh.position.y = -0.15;
    slabMesh.receiveShadow = true;
    houseGroup.add(slabMesh);

    // Front Landscape Lawn
    const lawnGeo = new THREE.BoxGeometry(22, 0.1, 22);
    const lawnMesh = new THREE.Mesh(lawnGeo, houseMaterials.grass);
    lawnMesh.position.y = -0.3;
    lawnMesh.receiveShadow = true;
    houseGroup.add(lawnMesh);

    // Driveway Paving
    const driveGeo = new THREE.BoxGeometry(4.2, 0.05, 7.5);
    const driveMesh = new THREE.Mesh(driveGeo, houseMaterials.concrete);
    driveMesh.position.set(-3.2, -0.08, 6.2);
    driveMesh.receiveShadow = true;
    houseGroup.add(driveMesh);

    // Pathway Paving
    const pathGeo = new THREE.BoxGeometry(1.6, 0.05, 5.5);
    const pathMesh = new THREE.Mesh(pathGeo, houseMaterials.concrete);
    pathMesh.position.set(0.3, -0.08, 5.2);
    pathMesh.receiveShadow = true;
    houseGroup.add(pathMesh);

    // 2. GROUND FLOOR MASSING
    // Double Garage (Left)
    const garageGeo = new THREE.BoxGeometry(4.0, 2.7, 5.8);
    const garageMesh = new THREE.Mesh(garageGeo, houseMaterials.wallSecondary);
    garageMesh.position.set(-3.2, 1.35, 1.2);
    garageMesh.castShadow = true;
    garageMesh.receiveShadow = true;
    houseGroup.add(garageMesh);

    // Garage Door Panel (Dark architectural horizontal slats)
    const gDoorGeo = new THREE.BoxGeometry(3.6, 2.4, 0.1);
    const gDoorMesh = new THREE.Mesh(gDoorGeo, houseMaterials.blackTrim);
    gDoorMesh.position.set(-3.2, 1.2, 4.15);
    gDoorMesh.castShadow = true;
    houseGroup.add(gDoorMesh);

    // Ground Floor Living & Kitchen Wing (Right)
    const livingGeo = new THREE.BoxGeometry(4.8, 2.7, 6.8);
    const livingMesh = new THREE.Mesh(livingGeo, houseMaterials.wallMain);
    livingMesh.position.set(2.4, 1.35, 0.6);
    livingMesh.castShadow = true;
    livingMesh.receiveShadow = true;
    houseGroup.add(livingMesh);

    // Massive Floor-to-Ceiling Ground Floor Glazing
    const gfGlassGeo = new THREE.BoxGeometry(3.6, 2.3, 0.1);
    const gfGlassMesh = new THREE.Mesh(gfGlassGeo, houseMaterials.glass);
    gfGlassMesh.position.set(2.4, 1.25, 4.02);
    houseGroup.add(gfGlassMesh);

    // Interior Warm Lit Core (visible through glass)
    const gfInteriorGeo = new THREE.BoxGeometry(3.4, 2.1, 0.1);
    const gfInteriorMesh = new THREE.Mesh(gfInteriorGeo, houseMaterials.interiorWarm);
    gfInteriorMesh.position.set(2.4, 1.25, 3.8);
    houseGroup.add(gfInteriorMesh);

    // Entrance Portico (Center)
    const porticoGeo = new THREE.BoxGeometry(2.0, 3.2, 2.2);
    const porticoMesh = new THREE.Mesh(porticoGeo, houseMaterials.stone);
    porticoMesh.position.set(0.3, 1.6, 2.4);
    porticoMesh.castShadow = true;
    porticoMesh.receiveShadow = true;
    houseGroup.add(porticoMesh);

    // Front Designer Pivot Door (Timber with black pull handle)
    const doorGeo = new THREE.BoxGeometry(1.2, 2.4, 0.08);
    const doorMesh = new THREE.Mesh(doorGeo, houseMaterials.timber);
    doorMesh.position.set(0.3, 1.2, 3.52);
    doorMesh.castShadow = true;
    houseGroup.add(doorMesh);

    // 3. FIRST FLOOR / CANTILEVERED UPPER MASSING
    // Master Suite Cantilever (Overhangs towards front & left)
    const upperMasterGeo = new THREE.BoxGeometry(4.8, 2.8, 6.4);
    const upperMasterMesh = new THREE.Mesh(upperMasterGeo, houseMaterials.wallMain);
    upperMasterMesh.position.set(-2.0, 4.1, 0.8);
    upperMasterMesh.castShadow = true;
    upperMasterMesh.receiveShadow = true;
    houseGroup.add(upperMasterMesh);

    // Upper Retreat Wing (Right)
    const upperRightGeo = new THREE.BoxGeometry(4.2, 2.8, 5.4);
    const upperRightMesh = new THREE.Mesh(upperRightGeo, houseMaterials.wallSecondary);
    upperRightMesh.position.set(2.3, 4.1, 0.3);
    upperRightMesh.castShadow = true;
    upperRightMesh.receiveShadow = true;
    houseGroup.add(upperRightMesh);

    // Upper Architectural Timber Screen (Bespoke Vertical Battens Feature)
    const battenCount = 14;
    const battenGroup = new THREE.Group();
    for (let i = 0; i < battenCount; i++) {
      const battenGeo = new THREE.BoxGeometry(0.08, 2.6, 0.15);
      const battenMesh = new THREE.Mesh(battenGeo, houseMaterials.timber);
      battenMesh.position.set(-3.6 + (i * 0.22), 4.1, 4.05);
      battenMesh.castShadow = true;
      battenGroup.add(battenMesh);
    }
    houseGroup.add(battenGroup);

    // Upper Master Balcony (Glass Balustrade)
    const balconyGeo = new THREE.BoxGeometry(3.6, 0.15, 1.2);
    const balconyMesh = new THREE.Mesh(balconyGeo, houseMaterials.concrete);
    balconyMesh.position.set(2.4, 2.8, 3.6);
    balconyMesh.castShadow = true;
    houseGroup.add(balconyMesh);

    const balustradeGeo = new THREE.BoxGeometry(3.6, 1.0, 0.06);
    const balustradeMesh = new THREE.Mesh(balustradeGeo, houseMaterials.glass);
    balustradeMesh.position.set(2.4, 3.3, 4.2);
    houseGroup.add(balustradeMesh);

    // Upper Floor Glass Sliding Suite
    const ufGlassGeo = new THREE.BoxGeometry(3.2, 2.3, 0.08);
    const ufGlassMesh = new THREE.Mesh(ufGlassGeo, houseMaterials.glass);
    ufGlassMesh.position.set(2.4, 4.0, 3.02);
    houseGroup.add(ufGlassMesh);

    // Upper Interior Warm Lit Core
    const ufInteriorGeo = new THREE.BoxGeometry(3.0, 2.1, 0.08);
    const ufInteriorMesh = new THREE.Mesh(ufInteriorGeo, houseMaterials.interiorWarm);
    ufInteriorMesh.position.set(2.4, 4.0, 2.8);
    houseGroup.add(ufInteriorMesh);

    // 4. Parapet Roof Caps & Architectural Cantilever Canopy
    const roofCapGeo = new THREE.BoxGeometry(9.6, 0.2, 7.8);
    const roofCapMesh = new THREE.Mesh(roofCapGeo, houseMaterials.blackTrim);
    roofCapMesh.position.set(0.1, 5.55, 0.6);
    roofCapMesh.castShadow = true;
    houseGroup.add(roofCapMesh);

    // Front Feature Blade Wall (Stone / Charcoal Textured accent)
    const bladeGeo = new THREE.BoxGeometry(0.4, 5.8, 2.2);
    const bladeMesh = new THREE.Mesh(bladeGeo, houseMaterials.stone);
    bladeMesh.position.set(0.45, 2.8, 3.4);
    bladeMesh.castShadow = true;
    houseGroup.add(bladeMesh);

    // 5. Landscaping Accents: Architectural Garden Planters & Trees
    const planterGeo = new THREE.BoxGeometry(3.2, 0.6, 1.0);
    const planterMesh = new THREE.Mesh(planterGeo, houseMaterials.blackTrim);
    planterMesh.position.set(2.6, 0.2, 4.8);
    planterMesh.castShadow = true;
    houseGroup.add(planterMesh);

    // Shrubs / Native architectural foliage
    for (let s = 0; s < 4; s++) {
      const shrubGeo = new THREE.DodecahedronGeometry(0.35 + Math.random() * 0.1);
      const shrubMat = new THREE.MeshStandardMaterial({ color: 0x2D5A27, roughness: 0.9 });
      const shrubMesh = new THREE.Mesh(shrubGeo, shrubMat);
      shrubMesh.position.set(1.4 + s * 0.8, 0.65, 4.8);
      shrubMesh.castShadow = true;
      houseGroup.add(shrubMesh);
    }

    scene.add(houseGroup);
  }

  function setLightingMode(mode) {
    currentMode = mode;
    if (!scene || !dirLight || !ambientLight) return;

    if (mode === 'day') {
      scene.fog.color.setHex(0xCFE0F2);
      ambientLight.color.setHex(0xE0ECF8);
      ambientLight.intensity = 1.6;

      dirLight.color.setHex(0xFFFFFF);
      dirLight.intensity = 2.4;
      dirLight.position.set(12, 20, 14);

      duskLights.forEach(l => l.intensity = 0.2);
      houseMaterials.interiorWarm.emissiveIntensity = 0.05;
      houseMaterials.glass.opacity = 0.65;
    } else if (mode === 'golden') {
      scene.fog.color.setHex(0x1B1822);
      ambientLight.color.setHex(0xFFBE76);
      ambientLight.intensity = 1.2;

      dirLight.color.setHex(0xFFAA44);
      dirLight.intensity = 2.8;
      dirLight.position.set(18, 8, 12);

      duskLights.forEach(l => l.intensity = 2.0);
      houseMaterials.interiorWarm.emissiveIntensity = 0.6;
      houseMaterials.glass.opacity = 0.45;
    } else if (mode === 'dusk') {
      scene.fog.color.setHex(0x080C14);
      ambientLight.color.setHex(0x28384D);
      ambientLight.intensity = 0.85;

      dirLight.color.setHex(0x406085);
      dirLight.intensity = 0.9;
      dirLight.position.set(8, 12, 10);

      duskLights.forEach(l => l.intensity = 4.2);
      houseMaterials.interiorWarm.emissiveIntensity = 0.95;
      houseMaterials.glass.opacity = 0.38;
    }

    // Update active state in UI buttons
    document.querySelectorAll('[data-lighting-mode]').forEach(btn => {
      btn.classList.toggle('active', btn.getAttribute('data-lighting-mode') === mode);
    });
  }

  function setRenderColor(hexColor) {
    currentRenderColor = hexColor;
    if (houseMaterials.wallMain) {
      houseMaterials.wallMain.color.setHex(hexColor);
    }
  }

  function setTimberColor(hexColor) {
    currentWoodColor = hexColor;
    if (houseMaterials.timber) {
      houseMaterials.timber.color.setHex(hexColor);
    }
  }

  function createHotspotsDOM() {
    const overlay = document.getElementById('architectural3DHotspots');
    if (!overlay) return;
    overlay.innerHTML = '';
    hotspotElements = [];

    hotspotsData.forEach((h, index) => {
      const pin = document.createElement('div');
      pin.className = 'hotspot-3d-pin';
      pin.innerHTML = `
        <div class="pin-pulse"></div>
        <div class="pin-core">${index + 1}</div>
        <div class="pin-tooltip">
          <strong>${h.title}</strong>
          <p>${h.desc}</p>
        </div>
      `;
      pin.addEventListener('click', (e) => {
        e.stopPropagation();
        focusOnHotspot(h);
      });
      overlay.appendChild(pin);
      hotspotElements.push({ element: pin, pos: h.pos });
    });
  }

  function updateHotspotsPosition() {
    if (!hotspotElements.length || !camera || !canvasContainer) return;

    const width = canvasContainer.clientWidth;
    const height = canvasContainer.clientHeight;
    const tempV = new THREE.Vector3();

    hotspotElements.forEach(item => {
      tempV.copy(item.pos);
      tempV.project(camera);

      // Check if behind camera
      const isBehind = tempV.z > 1;
      if (isBehind) {
        item.element.style.display = 'none';
        return;
      }

      item.element.style.display = 'block';
      const x = (tempV.x * 0.5 + 0.5) * width;
      const y = (-(tempV.y * 0.5) + 0.5) * height;
      item.element.style.transform = `translate(-50%, -50%) translate3d(${x}px, ${y}px, 0)`;
    });
  }

  function focusOnHotspot(h) {
    if (!controls) return;
    isAutoRotate = false;
    updateAutoRotateButton();

    // Smooth camera transition to hotspot
    const targetCamPos = new THREE.Vector3(
      h.pos.x + 3.2,
      h.pos.y + 1.8,
      h.pos.z + 4.5
    );

    let step = 0;
    const maxSteps = 45;
    const startCam = camera.position.clone();
    const startTarget = controls.target.clone();

    function tween() {
      step++;
      const t = step / maxSteps;
      const ease = t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;

      camera.position.lerpVectors(startCam, targetCamPos, ease);
      controls.target.lerpVectors(startTarget, h.pos, ease);
      controls.update();

      if (step < maxSteps) {
        requestAnimationFrame(tween);
      }
    }
    tween();
  }

  function resetCameraView() {
    if (!controls) return;
    const defaultPos = new THREE.Vector3(11, 7, 13);
    const defaultTarget = new THREE.Vector3(0, 2.2, 0);

    let step = 0;
    const maxSteps = 40;
    const startCam = camera.position.clone();
    const startTarget = controls.target.clone();

    function tween() {
      step++;
      const t = step / maxSteps;
      const ease = t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;

      camera.position.lerpVectors(startCam, defaultPos, ease);
      controls.target.lerpVectors(startTarget, defaultTarget, ease);
      controls.update();

      if (step < maxSteps) {
        requestAnimationFrame(tween);
      }
    }
    tween();
  }

  function updateAutoRotateButton() {
    const btn = document.getElementById('btnToggleAutoRotate');
    if (btn) {
      btn.classList.toggle('active', isAutoRotate);
      btn.innerHTML = isAutoRotate 
        ? `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><rect x="6" y="4" width="4" height="16"/><rect x="14" y="4" width="4" height="16"/></svg> Pause Rotation`
        : `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polygon points="5 3 19 12 5 21 5 3"/></svg> Auto-Rotate 360°`;
    }
  }

  function bindUIControls() {
    // Lighting buttons
    document.querySelectorAll('[data-lighting-mode]').forEach(btn => {
      btn.addEventListener('click', () => {
        setLightingMode(btn.getAttribute('data-lighting-mode'));
      });
    });

    // Render Color swatches
    document.querySelectorAll('[data-render-color]').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('[data-render-color]').forEach(b => b.classList.remove('selected'));
        btn.classList.add('selected');
        const color = parseInt(btn.getAttribute('data-render-color'), 16);
        setRenderColor(color);
      });
    });

    // Timber swatches
    document.querySelectorAll('[data-timber-color]').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('[data-timber-color]').forEach(b => b.classList.remove('selected'));
        btn.classList.add('selected');
        const color = parseInt(btn.getAttribute('data-timber-color'), 16);
        setTimberColor(color);
      });
    });

    // Auto rotate toggle
    const btnRotate = document.getElementById('btnToggleAutoRotate');
    if (btnRotate) {
      btnRotate.addEventListener('click', () => {
        isAutoRotate = !isAutoRotate;
        updateAutoRotateButton();
      });
    }

    // Reset camera button
    const btnReset = document.getElementById('btnResetCamera');
    if (btnReset) {
      btnReset.addEventListener('click', resetCameraView);
    }
  }

  function onWindowResize() {
    if (!camera || !renderer || !canvasContainer) return;
    const width = canvasContainer.clientWidth;
    const height = canvasContainer.clientHeight;
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
    renderer.setSize(width, height);
  }

  function animate() {
    requestAnimationFrame(animate);

    if (controls) {
      if (isAutoRotate) {
        controls.autoRotate = true;
        controls.autoRotateSpeed = 1.0;
      } else {
        controls.autoRotate = false;
      }
      controls.update();
    }

    updateHotspotsPosition();
    renderer.render(scene, camera);
  }

  // -------------------------------------------------------------
  // 360° 3D VIRTUAL INTERIOR PANORAMA VIEWER (Three.js Sphere)
  // -------------------------------------------------------------
  let panoScene, panoCamera, panoRenderer;
  let isUserInteracting = false, onPointerDownPointerX = 0, onPointerDownPointerY = 0;
  let lon = 0, onPointerDownLon = 0, lat = 0, onPointerDownLat = 0, phi = 0, theta = 0;
  let panoModalActive = false;

  function init360Panorama() {
    const modal = document.getElementById('virtualTourModal');
    const panoContainer = document.getElementById('panoContainer');
    if (!modal || !panoContainer || typeof THREE === 'undefined') return;

    panoScene = new THREE.Scene();
    panoCamera = new THREE.PerspectiveCamera(75, panoContainer.clientWidth / panoContainer.clientHeight, 1, 1100);
    panoCamera.target = new THREE.Vector3(0, 0, 0);

    const panoGeo = new THREE.SphereGeometry(500, 60, 40);
    panoGeo.scale(-1, 1, 1); // Invert inside sphere

    const textureLoader = new THREE.TextureLoader();
    // Use the 4K luxury kitchen image as 360 spherical panoramic texture
    textureLoader.load('assets/images/Gemini_Generated_Image_zc6bxgzc6bxgzc6b.jpeg', function (texture) {
      const material = new THREE.MeshBasicMaterial({ map: texture });
      const mesh = new THREE.Mesh(panoGeo, material);
      panoScene.add(mesh);
    });

    panoRenderer = new THREE.WebGLRenderer({ antialias: true });
    panoRenderer.setSize(panoContainer.clientWidth, panoContainer.clientHeight);
    panoRenderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    panoContainer.appendChild(panoRenderer.domElement);

    // Panorama Mouse / Touch Drag Handlers
    panoContainer.addEventListener('pointerdown', onPanoPointerDown);
    document.addEventListener('pointermove', onPanoPointerMove);
    document.addEventListener('pointerup', onPanoPointerUp);
    panoContainer.addEventListener('wheel', onPanoWheel, { passive: true });

    window.addEventListener('resize', () => {
      if (!panoCamera || !panoRenderer || !panoContainer) return;
      panoCamera.aspect = panoContainer.clientWidth / panoContainer.clientHeight;
      panoCamera.updateProjectionMatrix();
      panoRenderer.setSize(panoContainer.clientWidth, panoContainer.clientHeight);
    });

    // Modal open / close handlers
    document.querySelectorAll('[data-open-modal="virtualTourModal"]').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
        panoModalActive = true;
        setTimeout(() => {
          panoCamera.aspect = panoContainer.clientWidth / panoContainer.clientHeight;
          panoCamera.updateProjectionMatrix();
          panoRenderer.setSize(panoContainer.clientWidth, panoContainer.clientHeight);
        }, 150);
      });
    });

    animatePanorama();
  }

  function onPanoPointerDown(e) {
    if (e.isPrimary === false) return;
    isUserInteracting = true;
    onPointerDownPointerX = e.clientX;
    onPointerDownPointerY = e.clientY;
    onPointerDownLon = lon;
    onPointerDownLat = lat;
  }

  function onPanoPointerMove(e) {
    if (isUserInteracting === true) {
      lon = (onPointerDownPointerX - e.clientX) * 0.15 + onPointerDownLon;
      lat = (e.clientY - onPointerDownPointerY) * 0.15 + onPointerDownLat;
    }
  }

  function onPanoPointerUp() {
    isUserInteracting = false;
  }

  function onPanoWheel(e) {
    if (!panoCamera) return;
    const fov = panoCamera.fov + e.deltaY * 0.05;
    panoCamera.fov = THREE.MathUtils.clamp(fov, 35, 95);
    panoCamera.updateProjectionMatrix();
  }

  function animatePanorama() {
    requestAnimationFrame(animatePanorama);
    if (!panoModalActive || !panoCamera || !panoRenderer || !panoScene) return;

    if (!isUserInteracting) {
      lon += 0.08; // Subtle cinematic pan
    }

    lat = Math.max(-85, Math.min(85, lat));
    phi = THREE.MathUtils.degToRad(90 - lat);
    theta = THREE.MathUtils.degToRad(lon);

    const x = 500 * Math.sin(phi) * Math.cos(theta);
    const y = 500 * Math.cos(phi);
    const z = 500 * Math.sin(phi) * Math.sin(theta);

    panoCamera.lookAt(x, y, z);
    panoRenderer.render(panoScene, panoCamera);
  }

  // -------------------------------------------------------------
  // 3D CARD PERSPECTIVE TILT WITH DYNAMIC GLARE (VANILLA JS/CSS3D)
  // -------------------------------------------------------------
  function init3DCardTilt() {
    const cards = document.querySelectorAll('.design-card, .service-card, .timeline-card');
    cards.forEach(card => {
      // Create glare overlay
      let glare = card.querySelector('.card-3d-glare');
      if (!glare) {
        glare = document.createElement('div');
        glare.className = 'card-3d-glare';
        card.appendChild(glare);
      }

      card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;

        const rotateX = ((y - centerY) / centerY) * -9; // Max 9 deg
        const rotateY = ((x - centerX) / centerX) * 9;

        card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-6px) scale3d(1.015, 1.015, 1.015)`;
        
        // Glare dynamic position
        const glareX = (x / rect.width) * 100;
        const glareY = (y / rect.height) * 100;
        glare.style.background = `radial-gradient(circle at ${glareX}% ${glareY}%, rgba(255,255,255,0.18) 0%, rgba(255,255,255,0) 65%)`;
        glare.style.opacity = '1';
      });

      card.addEventListener('mouseleave', () => {
        card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateY(0) scale3d(1, 1, 1)';
        glare.style.opacity = '0';
      });
    });
  }

  // Initialize all when DOM is ready
  document.addEventListener('DOMContentLoaded', () => {
    init3DStudio();
    init360Panorama();
    init3DCardTilt();
  });

})();
