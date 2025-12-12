#!/usr/bin/env python3
"""
Onshape API Auth and Example Call
"""

import requests  # type: ignore
import base64
from typing import Dict, List, Optional


class OnshapeAPI:
    def __init__(
        self,
        access_key: str,
        secret_key: str,
        base_url: str = "https://cad.onshape.com",
    ):
        self.base_url = base_url
        # Create proper basic auth header for Onshape API keys
        credentials = f"{access_key}:{secret_key}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Basic {encoded_credentials}",
        }

    def get_document_contents(self, document_id: str, workspace_id: str) -> Dict:
        """
        Get the contents of a document including folders and elements.

        Args:
            document_id: The document ID
            workspace_id: The workspace ID

        Returns:
            Dictionary containing document contents with folders and elements
        """
        url = f"{self.base_url}/api/v12/documents/d/{document_id}/w/{workspace_id}/contents"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_drawings_in_folder(
        self, document_id: str, workspace_id: str, folder_name: str
    ) -> List[Dict]:
        """
        Get all drawing elements in a specific folder.

        Args:
            document_id: The document ID
            workspace_id: The workspace ID
            folder_name: Name of the folder to search in

        Returns:
            List of drawing elements in the specified folder
        """
        contents = self.get_document_contents(document_id, workspace_id)
        drawings = []

        # Get all elements (tabs) from the document
        elements = contents.get("elements", [])
        folders = contents.get("folders", {})

        # For now, if no folder_name is specified or folder_name is empty, return all drawings
        if not folder_name:
            # Filter for drawings
            for element in elements:
                if element.get("elementType") == "DRAWING":
                    drawings.append(element)
        else:
            folder_elements = self._find_elements_in_folder(
                folders, folder_name, elements
            )
            # Filter for drawing-related elements (could be DRAWING or APPLICATION type)
            drawings = [
                elem
                for elem in folder_elements
                if elem.get("elementType") in ["DRAWING", "APPLICATION"]
            ]

        return drawings

    def get_drawing_views(
        self, document_id: str, workspace_id: str, element_id: str
    ) -> List[Dict]:
        """
        Get views for a specific drawing element.

        Args:
            document_id: The document ID
            workspace_id: The workspace ID
            element_id: The drawing element ID

        Returns:
            List of drawing views
        """
        url = f"{self.base_url}/api/v12/drawings/d/{document_id}/w/{workspace_id}/e/{element_id}/views"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        data = response.json()
        return data.get("items", [])

    def get_element_reference(
        self, document_id: str, workspace_id: str, element_id: str, reference_id: str
    ) -> Dict:
        """
        Get reference information for a specific model reference in a drawing.

        Args:
            document_id: The document ID
            workspace_id: The workspace ID
            element_id: The drawing element ID
            reference_id: The model reference ID

        Returns:
            Reference information dictionary
        """
        url = f"{self.base_url}/api/v12/appelements/d/{document_id}/w/{workspace_id}/e/{element_id}/references/{reference_id}"
        params = {"includeInternal": "false"}
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def construct_part_studio_url(
        self, document_id: str, workspace_id: str, element_id: str
    ) -> str:
        """
        Construct a URL to view a part studio element.

        Args:
            document_id: The document ID
            workspace_id: The workspace ID
            element_id: The part studio element ID

        Returns:
            URL string to the part studio
        """
        return f"https://cad.onshape.com/documents/{document_id}/w/{workspace_id}/e/{element_id}"

    def _find_elements_in_folder(
        self, folders: Dict, folder_name: str, all_elements: List[Dict]
    ) -> List[Dict]:
        """
        Find elements that belong to a specific folder.
        """
        elements_in_folder = []
        self._collect_elements_from_folder(
            folders, folder_name, all_elements, elements_in_folder
        )
        return elements_in_folder

    def _collect_elements_from_folder(
        self,
        folder_data: Dict,
        target_name: str,
        all_elements: List[Dict],
        result: List,
    ) -> None:
        """
        Recursively collect elements from a specific folder.
        """
        if not isinstance(folder_data, dict):
            return

        current_name = folder_data.get("groupName", "")
        if current_name == target_name:
            # Found target folder - collect its elements
            self._extract_elements_from_groups(
                folder_data.get("groups", []), all_elements, result
            )
            return

        # Search in subfolders
        for group in folder_data.get("groups", []):
            if (
                isinstance(group, dict)
                and group.get("btType") != "BTDocumentElementReference-2484"
            ):
                self._collect_elements_from_folder(
                    group, target_name, all_elements, result
                )

    def _extract_elements_from_groups(
        self, groups: List[Dict], all_elements: List[Dict], result: List
    ) -> None:
        """
        Extract element objects from folder groups.
        """
        for group in groups:
            if group.get("btType") == "BTDocumentElementReference-2484":
                element_id = group.get("elementId")
                element = self._find_element_by_id(all_elements, element_id)
                if element:
                    result.append(element)

    def _find_element_by_id(
        self, elements: List[Dict], element_id: str
    ) -> Optional[Dict]:
        """
        Find an element by its ID.
        """
        for elem in elements:
            if elem.get("id") == element_id:
                return elem
        return None


def main():
    # === CONFIG ===
    ACCESS_KEY = "on_IWMQdi0CdWKXV0yMep6Tq"
    SECRET_KEY = "UbWkcjRdjLucZHfOZKvXKNvszQGt0mcgBcdyORObGiQuvBht"

    DOCUMENT_KEY = "131e985f14cd75cccd6e840f"
    WORKSPACE_KEY = "0f2acdf6bf86540201651005"
    FOLDER_NAME = "drawings"

    # Initialize API client with auth
    api = OnshapeAPI(ACCESS_KEY, SECRET_KEY)

    # Get all drawings in the specified folder
    try:
        drawings = api.get_drawings_in_folder(DOCUMENT_KEY, WORKSPACE_KEY, FOLDER_NAME)
        print(
            f"Successfully retrieved {len(drawings)} drawings from folder '{FOLDER_NAME}'"
        )

        if drawings:
            for drawing in drawings:
                drawing_id = drawing.get("id")
                drawing_name = drawing.get("name", "Unknown")
                print(f"- {drawing_name} (ID: {drawing_id})")

                # Get drawing views
                try:
                    views = api.get_drawing_views(
                        DOCUMENT_KEY, WORKSPACE_KEY, drawing_id
                    )
                    print(f"  Found {len(views)} views in drawing")

                    if views:
                        # Get modelReferenceId from first view (or any view that has it)
                        model_ref_id = None
                        for view in views:
                            if "modelReferenceId" in view and view["modelReferenceId"]:
                                model_ref_id = view["modelReferenceId"]
                                break

                        if model_ref_id:
                            print(f"  Model Reference ID: {model_ref_id}")

                            # Get reference information
                            try:
                                reference_info = api.get_element_reference(
                                    DOCUMENT_KEY,
                                    WORKSPACE_KEY,
                                    drawing_id,
                                    model_ref_id,
                                )
                                target_element_id = reference_info.get(
                                    "targetElementId"
                                )

                                if target_element_id:
                                    print(f"  Target Element ID: {target_element_id}")

                                    # Construct part studio URL
                                    part_studio_url = api.construct_part_studio_url(
                                        DOCUMENT_KEY, WORKSPACE_KEY, target_element_id
                                    )
                                    print(f"  Part Studio URL: {part_studio_url}")
                                else:
                                    print("  No target element ID found in reference")
                            except Exception as e:
                                print(f"  Failed to get reference info: {e}")
                        else:
                            print("  No model reference ID found in views")
                except Exception as e:
                    print(f"  Failed to get drawing views: {e}")

                print()  # Empty line between drawings
        else:
            print(f"No drawings found in folder '{FOLDER_NAME}'")
    except Exception as e:
        print(f"API call failed: {e}")


if __name__ == "__main__":
    main()
