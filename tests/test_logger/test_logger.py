import json

from python_library.logger.app_logger import AppLogger


def test_logger():
    AppLogger.set_config("./tests/test_logger/logging.conf", "python-library")

    print()
    AppLogger.instance().info("test")
    AppLogger.instance().info("테스트")
    pass


def test_json_formatter_via_conf(capsys):
    AppLogger._Singleton__instance = None
    AppLogger.set_config("./tests/test_logger/logging_json.conf", "python-library")

    AppLogger.instance().info("conf 기반 JSON 포맷 테스트")

    captured = capsys.readouterr()
    print(captured.out)
    record = json.loads(captured.out.strip())

    assert record["level"] == "INFO"
    assert record["logger"] == "python-library"
    assert record["message"] == "conf 기반 JSON 포맷 테스트"
    assert "timestamp" in record
    assert "thread_id" in record


def test_rich_logger():
    AppLogger._Singleton__instance = None
    AppLogger.set_config("./tests/test_logger/logging_rich.conf", "python-library")

    print()
    AppLogger.instance().info("info test")
    AppLogger.instance().error("[bold red]리치 마크업 에러 메시지[/bold red]")
    pass
