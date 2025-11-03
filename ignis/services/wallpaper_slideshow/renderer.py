import os
import math
from pathlib import Path
from typing import Optional, Callable
from gi.repository import GLib
from PIL import Image


SHADERS_DIR = os.path.join(os.path.dirname(__file__), "shaders")


class TransitionRenderer:
    """Handles wallpaper transitions with GLSL shaders.

    This class manages the transition between two wallpapers using
    fragment shaders for visual effects.
    """

    def __init__(self):
        self._current_image: Optional[Image.Image] = None
        self._next_image: Optional[Image.Image] = None
        self._transition_progress: float = 0.0
        self._transition_duration: float = 1.0
        self._shader_name: str = "fade"
        self._animation_timer: Optional[int] = None
        self._on_complete: Optional[Callable] = None

    def load_shader(self, shader_name: str) -> Optional[str]:
        """Load a GLSL shader file.

        Args:
            shader_name: Name of the shader (without .glsl extension)

        Returns:
            Shader source code or None if not found
        """
        shader_path = os.path.join(SHADERS_DIR, f"{shader_name}.glsl")

        if not os.path.exists(shader_path):
            print(f"Shader not found: {shader_path}")
            return None

        try:
            with open(shader_path, "r") as f:
                return f.read()
        except IOError as e:
            print(f"Failed to load shader {shader_name}: {e}")
            return None

    def start_transition(
        self,
        current_path: str,
        next_path: str,
        shader: str = "fade",
        duration: float = 1.0,
        on_complete: Optional[Callable] = None
    ) -> bool:
        """Start a transition between two wallpapers.

        Args:
            current_path: Path to current wallpaper
            next_path: Path to next wallpaper
            shader: Shader name to use for transition
            duration: Transition duration in seconds
            on_complete: Callback to call when transition completes

        Returns:
            True if transition was started successfully
        """
        # Stop any existing transition
        self.stop_transition()

        # Load images
        try:
            self._current_image = Image.open(current_path)
            self._next_image = Image.open(next_path)
        except Exception as e:
            print(f"Failed to load images for transition: {e}")
            return False

        self._shader_name = shader
        self._transition_duration = duration
        self._transition_progress = 0.0
        self._on_complete = on_complete

        # Start animation timer (60 FPS)
        self._animation_timer = GLib.timeout_add(
            16,  # ~60 FPS
            self._on_animation_tick
        )

        return True

    def stop_transition(self) -> None:
        """Stop the current transition."""
        if self._animation_timer is not None:
            GLib.source_remove(self._animation_timer)
            self._animation_timer = None

        self._current_image = None
        self._next_image = None
        self._transition_progress = 0.0

    def _on_animation_tick(self) -> bool:
        """Handle animation frame update."""
        # Update progress
        frame_time = 0.016  # ~16ms at 60 FPS
        self._transition_progress += frame_time / self._transition_duration

        if self._transition_progress >= 1.0:
            # Transition complete
            self._transition_progress = 1.0
            self._render_frame()

            if self._on_complete:
                self._on_complete()

            self.stop_transition()
            return False  # Stop timer

        # Render current frame
        self._render_frame()

        return True  # Continue timer

    def _render_frame(self) -> None:
        """Render a single frame of the transition.

        This is a simplified version - in a full implementation,
        this would render to an OpenGL texture using the shader.
        For now, we'll use PIL for software rendering of basic effects.
        """
        if not self._current_image or not self._next_image:
            return

        # Apply easing function to progress
        progress = self._ease_in_out_cubic(self._transition_progress)

        # For this simplified version, we'll just do a basic blend
        # A full implementation would use OpenGL and GLSL shaders
        if self._shader_name == "fade":
            self._render_fade(progress)
        # Additional shaders would be implemented here

    def _render_fade(self, progress: float) -> None:
        """Software implementation of fade transition."""
        # This is a placeholder - actual rendering would happen via OpenGL
        pass

    @staticmethod
    def _ease_in_out_cubic(t: float) -> float:
        """Cubic easing function for smooth animation."""
        if t < 0.5:
            return 4 * t * t * t
        else:
            return 1 - pow(-2 * t + 2, 3) / 2

    @staticmethod
    def get_available_shaders() -> list[str]:
        """Get list of available shader names."""
        if not os.path.exists(SHADERS_DIR):
            return []

        shaders = []
        for file in Path(SHADERS_DIR).glob("*.glsl"):
            shaders.append(file.stem)

        return sorted(shaders)


# Utility function for direct image transitions without GPU
def create_transition_image(
    current_path: str,
    next_path: str,
    progress: float,
    output_path: str,
    transition_type: str = "fade"
) -> bool:
    """Create a transition frame between two images using CPU rendering.

    This is a fallback for systems without OpenGL support.

    Args:
        current_path: Path to current wallpaper
        next_path: Path to next wallpaper
        progress: Transition progress (0.0 to 1.0)
        output_path: Where to save the transition frame
        transition_type: Type of transition effect

    Returns:
        True if successful
    """
    try:
        current = Image.open(current_path)
        next_img = Image.open(next_path)

        # Ensure same size
        if current.size != next_img.size:
            next_img = next_img.resize(current.size, Image.Resampling.LANCZOS)

        # Ensure same mode
        if current.mode != next_img.mode:
            next_img = next_img.convert(current.mode)

        # Apply transition
        if transition_type == "fade":
            # Simple alpha blend
            result = Image.blend(current, next_img, progress)

        elif transition_type == "slide":
            # Horizontal slide
            width, height = current.size
            offset = int(width * progress)

            result = Image.new(current.mode, current.size)
            result.paste(current, (-offset, 0))
            result.paste(next_img, (width - offset, 0))

        elif transition_type == "zoom":
            # Zoom effect
            scale = 1.0 + progress * 0.2  # Zoom out by 20%

            # Zoom out current image
            new_size = (int(current.size[0] * scale), int(current.size[1] * scale))
            current_scaled = current.resize(new_size, Image.Resampling.LANCZOS)

            # Center crop
            left = (new_size[0] - current.size[0]) // 2
            top = (new_size[1] - current.size[1]) // 2
            current_cropped = current_scaled.crop((
                left, top,
                left + current.size[0],
                top + current.size[1]
            ))

            # Blend with next image
            result = Image.blend(current_cropped, next_img, progress)

        else:
            # Default to fade
            result = Image.blend(current, next_img, progress)

        # Save result
        result.save(output_path, quality=95)
        return True

    except Exception as e:
        print(f"Failed to create transition image: {e}")
        return False
