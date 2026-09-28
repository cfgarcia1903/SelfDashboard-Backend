from dataclasses import dataclass



@dataclass
class Authorization:
    user_ID: str | None
    user_PIN: str | None
    user_Key: str | None
    
    def validate(self):
        return True
