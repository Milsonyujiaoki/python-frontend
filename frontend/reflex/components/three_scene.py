"""Minimal Three.js scene wrapper for Reflex.

The component renders an empty ``<div>`` that will be populated with a Three.js
scene (camera, renderer, a rotating cube) when the component mounts. The JavaScript
is injected via ``rx.eval`` and uses the CDN version of Three.js.

Example usage::

    from reflex import rx
    from .three_scene import three_scene

    def page():
        return rx.vstack(
            three_scene(id="demo-scene"),
            rx.text("A simple rotating cube rendered with Three.js"),
        )
"""

import reflex as rx

THREE_CDN = "https://cdn.jsdelivr.net/npm/three@0.161.0/build/three.min.js"

def three_scene(*, id: str = "three-scene", width: str = "400px", height: str = "300px") -> rx.Component:
    """Render a canvas with a rotating cube.

    Args:
        id: HTML element id for the container div.
        width: CSS width of the container.
        height: CSS height of the container.
    """
    # Ensure Three.js is loaded once.
    rx.use_effect(_load_three_js, [])

    # After the container exists, initialise the scene.
    rx.use_effect(lambda: _init_scene(id, width, height), [id])

    # Plain div; the JS will replace its contents with a canvas.
    return rx.html(f"<div id='{id}' style='width:{width};height:{height};'></div>")

def _load_three_js() -> None:
    """Inject Three.js script tag if not already present."""
    js = (
        "if (!window.THREE) {"
        f"var s=document.createElement('script');s.src='{THREE_CDN}';s.onload=function(){{window.THREE_LOADED=true;}};document.head.appendChild(s);"
        "}"
    )
    rx.eval(js)

def _init_scene(container_id: str, width: str, height: str) -> None:
    """Create a basic Three.js scene inside ``container_id``.
    This function runs in the browser after the container div is attached.
    """
    js = f"""
    (function() {{
        if (!window.THREE) {{ console.warn('Three.js not loaded'); return; }}
        const container = document.getElementById('{container_id}');
        if (!container) {{ console.warn('Container {container_id} not found'); return; }}
        // Create renderer
        const renderer = new THREE.WebGLRenderer({{ antialias: true }});
        renderer.setSize({width.replace('px','')}, {height.replace('px','')});
        container.innerHTML = '';
        container.appendChild(renderer.domElement);
        // Scene & camera
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, {width.replace('px','')}/{height.replace('px','')}, 0.1, 1000);
        camera.position.z = 2;
        // Cube geometry
        const geometry = new THREE.BoxGeometry(1, 1, 1);
        const material = new THREE.MeshNormalMaterial();
        const cube = new THREE.Mesh(geometry, material);
        scene.add(cube);
        // Animation loop
        function animate() {{
            requestAnimationFrame(animate);
            cube.rotation.x += 0.01;
            cube.rotation.y += 0.01;
            renderer.render(scene, camera);
        }}
        animate();
    }})();
    """
    rx.eval(js)

__all__ = ["three_scene"]
