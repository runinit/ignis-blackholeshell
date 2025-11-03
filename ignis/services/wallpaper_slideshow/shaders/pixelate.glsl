#version 330 core

// Pixelate transition
// Gradually increases pixel size then decreases while transitioning

uniform sampler2D currentTexture;
uniform sampler2D nextTexture;
uniform float progress;  // 0.0 to 1.0

in vec2 texCoord;
out vec4 fragColor;

void main() {
    // Calculate pixelation amount (peaks at middle of transition)
    float pixelation = sin(progress * 3.14159) * 50.0;
    pixelation = max(pixelation, 1.0);

    // Pixelate coordinates
    vec2 pixelSize = vec2(1.0 / pixelation, 1.0 / pixelation);
    vec2 pixelatedCoord = floor(texCoord / pixelSize) * pixelSize;

    // Sample textures with pixelated coordinates
    vec4 current = texture(currentTexture, pixelatedCoord);
    vec4 next = texture(nextTexture, pixelatedCoord);

    // Blend between the two
    fragColor = mix(current, next, progress);
}
