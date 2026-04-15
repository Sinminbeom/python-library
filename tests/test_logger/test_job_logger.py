import json

from python_library.logger.job_logger import JobLogger, JobStatus


def test_job_logger_basic(capsys):
    logger = JobLogger(service="etl-pipeline", job_run_id="jr_test_001")

    logger.info("데이터 로드 완료", step="extract", status=JobStatus.DONE, row_count=1000)

    captured = capsys.readouterr()
    print(captured.out)
    record = json.loads(captured.out.strip())

    assert record["level"] == "INFO"
    assert record["logger"] == "etl-pipeline"
    assert record["message"] == "데이터 로드 완료"
    assert record["job_run_id"] == "jr_test_001"
    assert record["step"] == "extract"
    assert record["status"] == "DONE"
    assert record["row_count"] == 1000
    assert "timestamp" in record
    assert "thread_id" in record


def test_job_logger_omits_none_fields(capsys):
    logger = JobLogger(service="etl-pipeline")

    logger.info("시작")

    captured = capsys.readouterr()
    record = json.loads(captured.out.strip())

    assert "job_run_id" not in record
    assert "step" not in record
    assert "status" not in record
