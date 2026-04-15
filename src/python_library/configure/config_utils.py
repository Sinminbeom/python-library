import configparser


class ConfigUtils:
    @staticmethod
    def config_parser(config_file) -> dict:
        config = configparser.ConfigParser()
        config.read(config_file)

        options = dict()
        for section in config.sections():
            for option in config.options(section):
                value = config.get(section, option)
                options[(section, option)] = value

        return options
