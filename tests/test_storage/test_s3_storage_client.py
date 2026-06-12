from unittest.mock import patch

from python_library.storage.s3.s3_storage_client import S3StorageClient
from python_library.storage.s3.s3_storage_factory import S3StorageFactory
from python_library.storage.s3.s3_storage_info_factory import S3StorageInfoFactory


@patch("python_library.storage.s3.s3_storage_client.boto3")
def test_connect_without_credentials(mock_boto3):
    client = S3StorageClient()
    client.connect()

    call_kwargs = mock_boto3.client.call_args.kwargs
    assert "aws_access_key_id" not in call_kwargs
    assert "aws_secret_access_key" not in call_kwargs
    assert "aws_session_token" not in call_kwargs


@patch("python_library.storage.s3.s3_storage_client.boto3")
def test_connect_with_sts_credentials(mock_boto3):
    client = S3StorageClient(
        access_key="ASIA_TEST_KEY",
        secret_key="test_secret",
        session_token="test_token",
    )
    client.connect()

    call_kwargs = mock_boto3.client.call_args.kwargs
    assert call_kwargs["aws_access_key_id"] == "ASIA_TEST_KEY"
    assert call_kwargs["aws_secret_access_key"] == "test_secret"
    assert call_kwargs["aws_session_token"] == "test_token"


@patch("python_library.storage.s3.s3_storage_client.boto3")
def test_factory_creates_client_with_sts_credentials(mock_boto3):
    factory = S3StorageFactory(
        S3StorageInfoFactory(
            access_key="ASIA_TEST_KEY",
            secret_key="test_secret",
            session_token="test_token",
        )
    )
    storage = factory.create_storage()
    storage.connect()

    call_kwargs = mock_boto3.client.call_args.kwargs
    assert call_kwargs["aws_access_key_id"] == "ASIA_TEST_KEY"
    assert call_kwargs["aws_secret_access_key"] == "test_secret"
    assert call_kwargs["aws_session_token"] == "test_token"
