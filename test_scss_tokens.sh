#!/bin/bash
# Test SCSS compilation with Blackhole design tokens

set -e

echo "Testing SCSS compilation with Blackhole design tokens..."
echo ""

# Create a test SCSS file that uses the tokens
TEST_FILE="/tmp/test_blackhole_tokens.scss"

cat > "$TEST_FILE" << 'EOF'
// Import the tokens
@import "scss/_blackhole_tokens.scss";

// Test that tokens are accessible
.test-container {
    // Typography
    font-size: $font-size-m;
    font-weight: $font-weight-regular;

    // Spacing
    padding: $spacing-m;
    margin: $spacing-l;

    // Border radius
    border-radius: $radius-s;

    // Colors
    background-color: $surface-container;
    color: $on-surface;

    // Shadows
    box-shadow: $shadow-medium;

    // Opacity
    opacity: $opacity-full;

    // Animation
    transition: all $animation-normal $ease-in-out-cubic;
}

// Test mixins
.test-card {
    @include card-base;
}

.test-floating {
    @include floating;
}

.test-focus {
    &:focus {
        @include focus-ring;
    }
}
EOF

# Try to compile the test file
echo "Compiling test SCSS file..."
if sassc -t expanded -I ignis "$TEST_FILE" /tmp/test_output.css 2>&1; then
    echo "✅ SCSS compilation successful!"
    echo ""
    echo "Generated CSS sample:"
    head -30 /tmp/test_output.css
    echo ""
    echo "✅ All Blackhole design tokens are accessible and working!"
    rm -f "$TEST_FILE" /tmp/test_output.css
    exit 0
else
    echo "❌ SCSS compilation failed!"
    rm -f "$TEST_FILE" /tmp/test_output.css
    exit 1
fi
