import boto3
import json
import io
import pyarrow as pa
import pyarrow.parquet as pq


def test_copy():
    client = boto3.client(service_name="s3")

    src_bucket_name = "python_library-dl-raw-dev"
    src_path = "test/test.txt"
    src_source = {"Bucket": src_bucket_name, "Key": src_path}

    dst_bucket_name = "python_library-dl-raw-dev"
    dst_path = "test/ttt/test.txt"

    client.copy_object(CopySource=src_source, Bucket=dst_bucket_name, Key=dst_path)


def test_list_objects():
    bucket_name = "python_library-dl-raw-dev"

    client = boto3.client(service_name="s3")

    response = client.list_objects(Bucket=bucket_name)
    print(response)

    pass


def test_write():
    client = boto3.client(service_name="s3")

    src_bucket = "python_library-dl-raw-dev"
    src_key = "test/meta.json"
    dst_bucket = "python_library-dl-raw-dev"
    dst_key = "test/parquet/output.parquet"

    # 1) src s3에서 파일 읽기 (예시는 CSV)
    obj = client.get_object(Bucket=src_bucket, Key=src_key)
    body = obj["Body"].read().decode("utf-8")

    # 1) JSON → Python 객체
    data = json.loads(body)

    # Arrow Table로 변환 (nested JSON 지원)
    table = pa.Table.from_pylist([data])

    buffer = io.BytesIO()
    pq.write_table(table, buffer)
    buffer.seek(0)

    client.put_object(Bucket=dst_bucket, Key=dst_key, Body=buffer.getvalue())
    pass


def test_read():
    client = boto3.client(service_name="s3")
    bucket = "python_library-dl-raw-dev"
    key = "test/parquet/output.parquet"

    obj = client.get_object(Bucket=bucket, Key=key)
    body = obj["Body"].read()

    table = pq.read_table(io.BytesIO(body))

    print()
    print(table)

    pass
