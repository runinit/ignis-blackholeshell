#version 330 core

// Simple cross-fade transition
// Blends linearly between two textures

uniform sampler2D currentTexture;
uniform sampler2D nextTexture;
uniform float progress;  // 0.0 to 1.0

in vec2 texCoord;
out vec4 fragColor;

void main() {
    vec4 current = texture(currentTexture, texCoord);
    vec4 next = texture(nextTexture, texCoord);

    // Linear interpolation between the two textures
    fragColor = mix(current, next, progress);
}
