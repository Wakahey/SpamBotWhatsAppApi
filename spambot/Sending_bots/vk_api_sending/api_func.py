import vk_api
from .config import TOKEN, BASE_MESSAGE
from spambot.core.config import logger
from fastapi import HTTPException

session_vk = vk_api.VkApi(token=TOKEN)
vk = session_vk.get_api()


def authorization_token():
    session_vk = vk_api.VkApi(token=TOKEN)
    vk = session_vk.get_api()
    return vk


def get_info_by_id(id_num, vk_auth=authorization_token()):
    logger.info(f"Получаем информацию по id={id_num}")
    user = vk_auth.users.get(user_ids=f"{id_num}")
    if user:
        logger.info(user)
        id_num = user[0]["id"]
        return id_num
    else:
        logger.error("Пользователя с таким id не существует")
        raise ValueError("Пользователя с таким id не существует")


def send_message(id, brand, model, space_part, additional_info):
    vk.messages.send(user_id=id,
                     random_id=0,
                     message=BASE_MESSAGE.format(brand,
                                                 model,
                                                 space_part,
                                                 additional_info))


if __name__ == '__main__':
    session_vk = vk_api.VkApi(token=TOKEN)
    vk = session_vk.get_api()
    print(get_info_by_id(id_num="pena_loleshchuk"))
    # send_message(id=id, brand="BMW", model="SBR400", space_part="LP2000", additional_info="скиньте фото")
