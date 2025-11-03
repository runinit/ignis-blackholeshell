#version 330 core

// Horizontal slide transition
// Current image slides left while next image slides in from right

uniform sampler2D currentTexture;
uniform sampler2D nextTexture;
uniform float progress;  // 0.0 to 1.0

in vec2 texCoord;
out vec4 fragColor;

void main() {
    // Calculate horizontal offset
    float offset = progress;

    // Coordinates for current texture (sliding left)
    vec2 currentCoord = vec2(texCoord.x + offset, texCoord.y);

    // Coordinates for next texture (sliding in from right)
    vec2 nextCoord = vec2(texCoord.x + offset - 1.0, texCoord.y);

    // Sample textures
    vec4 current = texture(currentTexture, currentCoord);
    vec4 next = texture(nextTexture, nextCoord);

    // Choose which texture to display based on position
    if (texCoord.x < 1.0 - progress) {
        fragColor = current;
    } else {
        fragColor = next;
    }
}
