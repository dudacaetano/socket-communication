from enum import Enum


class NotificationType(Enum):
   REFRESH = "refresh"
   ACTION = "action"
   END_GAME = "end_game"
   ERROR = "error"
   MESSAGE = "message"
   INITIALIZE = "initialize"
   GIVEUP = "giveup"
   RESET = "reset"
   