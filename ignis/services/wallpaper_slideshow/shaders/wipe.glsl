#version 330 core

// Wipe transition
// A diagonal wipe from top-left to bottom-right

uniform sampler2D currentTexture;
uniform sampler2D nextTexture;
uniform float progress;  // 0.0 to 1.0

in vec2 texCoord;
out vec4 fragColor;

void main() {
    // Diagonal wipe calculation
    // Wipe progresses from top-left (0,0) to bottom-right (1,1)
    float wipePosition = (texCoord.x + texCoord.y) / 2.0;

    // Soft edge for smoother transition
    float edgeWidth = 0.1;
    float alpha = smoothstep(progress - edgeWidth, progress + edgeWidth, wipePosition);

    // Sample textures
    vec4 current = texture(currentTexture, texCoord);
    vec4 next = texture(nextTexture, texCoord);

    // Blend based on wipe position
    fragColor = mix(next, current, alpha);
}
