#!/usr/bin/env python3
"""
Test script for Blackhole Shell design tokens.
Validates that all required tokens are defined in _blackhole_tokens.scss
"""

import os
import re


def test_blackhole_tokens():
    """Test that all design tokens are defined."""
    print("Testing Blackhole Shell design tokens...")
    print()

    tokens_file = os.path.join(
        os.path.dirname(__file__), "ignis", "scss", "_blackhole_tokens.scss"
    )

    # Read the tokens file
    with open(tokens_file, "r") as f:
        content = f.read()

    # Define required token categories and their tokens
    required_tokens = {
        "Typography": [
            "$font-size-xxs",
            "$font-size-xs",
            "$font-size-s",
            "$font-size-m",
            "$font-size-l",
            "$font-size-xl",
            "$font-size-xxl",
            "$font-size-xxxl",
            "$font-weight-regular",
            "$font-weight-medium",
            "$font-weight-semibold",
            "$font-weight-bold",
        ],
        "Spacing": [
            "$spacing-xxs",
            "$spacing-xs",
            "$spacing-s",
            "$spacing-m",
            "$spacing-l",
            "$spacing-xl",
        ],
        "Border Radius": [
            "$radius-xxs",
            "$radius-xs",
            "$radius-s",
            "$radius-m",
            "$radius-l",
            "$radius-screen",
        ],
        "Borders": [
            "$border-s",
            "$border-m",
            "$border-l",
        ],
        "Opacity": [
            "$opacity-none",
            "$opacity-light",
            "$opacity-medium",
            "$opacity-heavy",
            "$opacity-almost",
            "$opacity-full",
        ],
        "Shadows": [
            "$shadow-opacity",
            "$shadow-blur-max",
            "$shadow-offset-x",
            "$shadow-offset-y",
            "$shadow-standard",
            "$shadow-light",
            "$shadow-medium",
            "$shadow-heavy",
        ],
        "Animations": [
            "$animation-faster",
            "$animation-fast",
            "$animation-normal",
            "$animation-slow",
            "$animation-slowest",
            "$delay-tooltip",
            "$ease-out-cubic",
            "$ease-in-cubic",
            "$ease-in-out-cubic",
        ],
        "Material Design 3 Colors": [
            "$primary",
            "$on-primary",
            "$secondary",
            "$on-secondary",
            "$tertiary",
            "$on-tertiary",
            "$error",
            "$on-error",
            "$background",
            "$on-background",
            "$surface",
            "$on-surface",
            "$surface-variant",
            "$on-surface-variant",
            "$surface-container",
            "$surface-container-low",
            "$surface-container-high",
            "$outline",
            "$outline-variant",
        ],
    }

    # Test each category
    total_tokens = 0
    for category, tokens in required_tokens.items():
        print(f"Testing {category} tokens...")

        missing = []
        for token in tokens:
            # Check if token is defined (look for the pattern "$token-name:")
            pattern = re.escape(token) + r"\s*:"
            if not re.search(pattern, content):
                missing.append(token)

        if missing:
            raise AssertionError(
                f"Missing tokens in {category}: {', '.join(missing)}"
            )

        print(f"  ✅ All {len(tokens)} {category.lower()} tokens defined")
        total_tokens += len(tokens)

    print()

    # Test that mixins are defined
    print("Testing utility mixins...")
    required_mixins = [
        "@mixin card-base",
        "@mixin floating",
        "@mixin transition-standard",
        "@mixin focus-ring",
        "@mixin text-truncate",
    ]

    missing_mixins = []
    for mixin in required_mixins:
        if mixin not in content:
            missing_mixins.append(mixin)

    if missing_mixins:
        raise AssertionError(f"Missing mixins: {', '.join(missing_mixins)}")

    print(f"  ✅ All {len(required_mixins)} utility mixins defined")
    print()

    # Test z-index scale
    print("Testing z-index scale...")
    z_indices = [
        "$z-background",
        "$z-default",
        "$z-elevated",
        "$z-dropdown",
        "$z-overlay",
        "$z-modal",
        "$z-tooltip",
        "$z-notification",
    ]

    missing_z = []
    for z in z_indices:
        pattern = re.escape(z) + r"\s*:"
        if not re.search(pattern, content):
            missing_z.append(z)

    if missing_z:
        raise AssertionError(f"Missing z-index tokens: {', '.join(missing_z)}")

    print(f"  ✅ All {len(z_indices)} z-index levels defined")
    print()

    # Summary
    print("=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("=" * 60)
    print()
    print(f"Summary:")
    print(f"  - {total_tokens} design tokens validated")
    print(f"  - {len(required_mixins)} utility mixins validated")
    print(f"  - {len(z_indices)} z-index levels validated")
    print(f"  - File size: {len(content)} characters")
    print()
    print("Blackhole Shell design system is ready to use!")


if __name__ == "__main__":
    try:
        test_blackhole_tokens()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
        exit(1)
