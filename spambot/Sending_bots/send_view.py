from fastapi import APIRouter, Depends
from spambot.core.models.db_helper import db_helper
from spambot.Sending_bots.schemas import InputSendingInfo
from sqlalchemy.ext.asyncio import AsyncSession
from spambot.Sending_bots.email_sending.email_sending import email_sender
from spambot.Sending_bots.db_requests import sending_get_sellers_where
from .whatsapp_sending.docker_run_api import start_docker_container, is_container_running
import time
import threading

router = APIRouter(prefix="/send", tags=["Sending"])


@router.post("/send_message/")
async def send_message_by_mail(sending_data: InputSendingInfo,
                               session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    print(sending_data)
    result = await sending_get_sellers_where(session=session,
                                             seller_type=sending_data.seller_type,
                                             sending_type=sending_data.sending_type)
    if sending_data.sending_type == "email":
        email_sender(customers_list=result,
                     article=sending_data.part_number,
                     theme=sending_data.email_subject)
    if sending_data.sending_type == "phone_number":
        docker_thread = threading.Thread(target=start_docker_container, daemon=True)
        docker_thread.start()
        time.sleep(4)
        if is_container_running("whatsapp-http-api"):
            return 200
        else:
            return 400
