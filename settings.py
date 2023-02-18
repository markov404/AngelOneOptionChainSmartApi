

class InitSettings:
    def __init__(self, path_to_settings_file: str = "settings.txt") -> None:
        self.settings_file = path_to_settings_file

        self.API_KEY = self.get_setting("API_KEY")
        self.ID = self.get_setting("ID")
        self.PASSWORD = self.get_setting("PASSWORD")
        self.OTP_CODE = self.get_setting("OTP_CODE")

        api_key_and_id: str = f"{self.API_KEY} {self.ID}"
        passw_and_otp: str = f"{self.PASSWORD} {self.OTP_CODE}"
        settings: str = f"{api_key_and_id} {passw_and_otp}"
        print(f"Getted settings: {settings}")

    def get_setting(self, setting_name: str) -> str:
        path = self.settings_file

        with open(path, "r", encoding="utf-8") as file:
            readed_file = file.read()

        for item in readed_file.split(";"):
            if item.split(':')[0] == setting_name:
                return item.split(':')[1]
        raise Exception("File is not right formatted!")
