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


def combine_specifications(baseSpecPath: Path, *paths: List[Path]) -> Dict[str, Any]:
    baseSpec = _parse_spec_file(baseSpecPath)
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
        spec = _parse_spec_file(path)
        for attr in ("paths", "components"):  # Dict-based specs
            if attr in spec:
                baseSpec[attr] = dict(baseSpec[attr], **spec[attr])
        for attr in ("security", "tags"):  # List-based specs
            if attr in spec:
                baseSpec[attr].append(spec[attr])

    return baseSpec
