from python_library.configure.app_config import AppConfig


def test_configure():
    AppConfig.set_config("./tests/test_configure/application.conf")

    project_name = AppConfig.instance().get_config("COMMON", "ProjectName")
    print(project_name)
    pass
