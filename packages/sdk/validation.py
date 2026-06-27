import logging
from typing import Dict, List, Set, Any
from pydantic import BaseModel, Field

logger = logging.getLogger("SDKValidation")


class ManifestIdentity(BaseModel):
    id: str
    name: str
    version: str
    description: str
    author: str


class ManifestRequirements(BaseModel):
    capabilities: List[Dict[str, str]] = Field(default_factory=list)
    tools: List[Dict[str, str]] = Field(default_factory=list)
    permissions: List[str] = Field(default_factory=list)


class PackageManifest(BaseModel):
    manifest_version: str
    type: str  # 'employee' | 'capability' | 'skill'
    identity: ManifestIdentity
    requirements: ManifestRequirements = Field(
        default_factory=lambda: ManifestRequirements()
    )


class SDKValidator:
    """
    Validates QEVN packages manifest schemas and analyzes dependency trees
    to prevent circular dependency references.
    """

    @classmethod
    def validate_manifest(cls, manifest_dict: Dict[str, Any]) -> PackageManifest:
        """Validates manifest fields against Pydantic schema rules."""
        try:
            return PackageManifest(**manifest_dict)
        except Exception as e:
            raise ValueError(f"Manifest validation failed: {str(e)}")

    @classmethod
    def check_circular_dependencies(
        cls, target_id: str, dependency_map: Dict[str, List[str]]
    ) -> bool:
        """
        DFS cycle detection checking for circular references in package structures.
        """
        visited: Set[str] = set()
        rec_stack: Set[str] = set()

        def dfs(node: str) -> bool:
            visited.add(node)
            rec_stack.add(node)

            for neighbor in dependency_map.get(node, []):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    # Cycle found!
                    return True

            rec_stack.remove(node)
            return False

        if dfs(target_id):
            raise ValueError(
                f"Circular dependency error detected starting from package: {target_id}"
            )

        logger.info(
            f"Dependency graph check completed. No cycles detected for package '{target_id}'."
        )
        return True
