"""STEP to GLTF conversion utility for the Part Management System."""

import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

# Default tolerances for STEP to GLB conversion
DEFAULT_TOL_LINEAR = 0.1
DEFAULT_TOL_ANGULAR = 0.5


def convert_step_to_gltf(
    step_file_path: str, output_dir: str, output_filename: Optional[str] = None
) -> dict:
    """Convert a STEP file to GLTF/GLB format using cascadio.

    Args:
        step_file_path (str): Path to the input STEP file
        output_dir (str): Directory to save the converted GLTF file
        output_filename (str, optional): Output filename without extension. Defaults to input filename.

    Returns:
        dict: Conversion result with status, file path, and error message if any
    """
    try:
        import cascadio  # type: ignore
    except ImportError:
        return {
            "success": False,
            "error": "cascadio library not available. Please install it: pip install cascadio",
            "gltf_path": None,
        }

    try:
        step_path = Path(step_file_path)
        if not step_path.exists():
            return {
                "success": False,
                "error": f"STEP file not found: {step_file_path}",
                "gltf_path": None,
            }

        if output_filename is None:
            output_filename = step_path.stem

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        glb_path = output_path / f"{output_filename}.glb"

        logger.info(f"Converting STEP file to GLB: {step_file_path} -> {glb_path}")

        # Use cascadio to convert STEP to GLB
        cascadio.step_to_glb(
            step_path.as_posix(),
            glb_path.as_posix(),
            tol_linear=DEFAULT_TOL_LINEAR,
            tol_angular=DEFAULT_TOL_ANGULAR,
        )

        if not glb_path.exists():
            return {
                "success": False,
                "error": "GLB file was not created",
                "gltf_path": None,
            }

        logger.info(f"Successfully converted STEP to GLB: {glb_path}")

        return {"success": True, "error": None, "gltf_path": str(glb_path)}

    except Exception as e:
        logger.error(f"Error converting STEP to GLTF: {str(e)}", exc_info=True)
        return {
            "success": False,
            "error": f"Conversion failed: {str(e)}",
            "gltf_path": None,
        }
