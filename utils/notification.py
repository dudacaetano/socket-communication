from enum import Enum

class NotificationType(Enum):
   REFRESH = "refresh"
   ACTION = "action"
   END_GAME = "end_game"
   ERROR = "error"
   CHAT = "chat"
   CONFIG = "config"
   GIVEUP = "giveup"
   RESET = "reset"
    
    