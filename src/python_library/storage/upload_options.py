from dataclasses import dataclass, field

from boto3.s3.transfer import MB

from python_library.define.enum import IENUM


class E_CHECKSUM_ALGORITHM(IENUM):
    SHA256 = "SHA256"


@dataclass(frozen=True)
class UploadOptions:
    max_concurrency: int = 1
    multipart_threshold: int = 8 * MB
    multipart_chunk_size: int = 8 * MB
    checksum_algorithm: str = E_CHECKSUM_ALGORITHM.SHA256
    metadata: dict[str, str] = field(default_factory=dict)
    tagging: dict[str, str] = field(default_factory=dict)
