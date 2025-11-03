#version 330 core

// Zoom transition
// Current image zooms out while fading to next image

uniform sampler2D currentTexture;
uniform sampler2D nextTexture;
uniform float progress;  // 0.0 to 1.0

in vec2 texCoord;
out vec4 fragColor;

void main() {
    // Zoom factor (zoom out by 30% at peak)
    float zoomFactor = 1.0 + progress * 0.3;

    // Center point for zoom
    vec2 center = vec2(0.5, 0.5);

    // Calculate zoomed coordinates
    vec2 zoomedCoord = center + (texCoord - center) * zoomFactor;

    // Sample textures
    vec4 current = texture(currentTexture, zoomedCoord);
    vec4 next = texture(nextTexture, texCoord);

    // Fade between zoomed current and next
    fragColor = mix(current, next, progress);
}
