#version 330 core

// Swirl/twist transition
// Creates a swirling distortion effect

uniform sampler2D currentTexture;
uniform sampler2D nextTexture;
uniform float progress;  // 0.0 to 1.0

in vec2 texCoord;
out vec4 fragColor;

void main() {
    vec2 center = vec2(0.5, 0.5);
    vec2 offset = texCoord - center;

    // Distance from center
    float dist = length(offset);

    // Rotation angle based on distance and progress
    float angle = progress * 6.28318 * (1.0 - dist);  // 2π radians

    // Rotate coordinates
    float s = sin(angle);
    float c = cos(angle);
    vec2 rotatedOffset = vec2(
        offset.x * c - offset.y * s,
        offset.x * s + offset.y * c
    );

    vec2 swirlCoord = center + rotatedOffset;

    // Sample textures
    vec4 current = texture(currentTexture, swirlCoord);
    vec4 next = texture(nextTexture, texCoord);

    // Blend with fade
    fragColor = mix(current, next, progress);
}
