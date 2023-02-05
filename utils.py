import prance

from typing import Any, Dict, List
from pathlib import Path


def _parse_spec_file(file: Path) -> Dict[str, Any]:
    """
    Parse a openapi specification file and return a validated
    dictionary with the contents of the spec

    :param file: Path object to the openapi spec file
    :return: Dictionary with details of specification
    """
    parser = prance.ResolvingParser(
        str(file.absolute()), lazy=True, backend="openapi-spec-validator"
    )
    parser.parse()
    return parser.specification


def combine_specifications(baseSpecPath: str, *paths: str) -> Dict[str, Any]:
    """
    Combine multiple openapi specification files into a single dictionary object with specification information

    :param baseSpecPath: Path to the base specification file that will serve as the base to build the combined spec
    :param paths: Paths to additional specification files to combine with the base spec
    """
    baseSpec = _parse_spec_file(Path(baseSpecPath))
    if not paths:
        return baseSpec

    # Add defaults for optional parts of the spec
    if "servers" not in baseSpec:
        baseSpec["servers"] = []
    if "components" not in baseSpec:
        baseSpec["components"] = dict()
    if "security" not in baseSpec:
        baseSpec["security"] = []
    if "tags" not in baseSpec:
        baseSpec["tags"] = []

    # Combine additional specs
    for path in paths:
        spec = _parse_spec_file(Path(path))

        if "paths" in spec:
            baseSpec["paths"] = dict(baseSpec["paths"], **spec["paths"])

        if "components" in spec:
            for attr in (
                "schemas",
                "responses",
                "parameters",
                "examples",
                "requestBodies",
                "headers",
                "securitySchemes",
                "links",
                "callbacks",
            ):
                if attr in spec["components"]:
                    baseSpec["components"][attr] = dict(
                        baseSpec["components"].get(attr, dict()),
                        **spec["components"][attr]
                    )

        for attr in ("security", "tags"):  # List-based specs
            if attr in spec:
                baseSpec[attr].append(spec[attr])

    return baseSpec
