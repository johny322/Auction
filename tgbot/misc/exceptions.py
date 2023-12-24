from enum import Enum


class DeleteError(str, Enum):
    cant_for_everyone = ".*message can't be deleted for everyone.*"


class MessageError:
    Delete = DeleteError


class TelegramBadRequestText:
    Message = MessageError


if __name__ == '__main__':
    r = TelegramBadRequestText.Message.Delete.cant_for_everyone in "message can't be deleted for everyone"
    print(r)
