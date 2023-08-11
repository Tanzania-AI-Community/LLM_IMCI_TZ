import os
import logging
import uvicorn
from sarufi import Sarufi
from heyoo import WhatsApp
from dotenv import load_dotenv
from fastapi import FastAPI, Response, Request, BackgroundTasks

from utils import media_uploads
from mangum import Mangum


app = FastAPI()
handler = Mangum(app)

# Load .env file
load_dotenv(".env")

messenger = WhatsApp(os.environ["WHATSAPP_TOKEN"],
                     phone_number_id=os.environ["WHATSAPP_PHONE_NUMBER_ID"])

VERIFY_TOKEN = "30cca545-3838-48b2-80a7-9e43b1ae8ce4"

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

sarufi_bot = Sarufi(os.environ["SARUFI_API_KEY"])
sarufi_bot = sarufi_bot.get_bot(id=os.environ["SARUFI_BOT_ID"])


def send_medias(action: dict, mobile: str, type: str):
    for act in action:
        link = act.get("link")
        caption = act.get("caption")
        if type == "images":
            messenger.send_image(
                image=link, recipient_id=mobile, caption=caption)
        elif type == "videos":
            messenger.send_video(
                video=link, recipient_id=mobile, caption=caption)
        elif type == "audios":
            messenger.send_document(document=link, recipient_id=mobile,
                                    caption=caption)
        elif type == "sticker":
            messenger.send_sticker(sticker=link, recipient_id=mobile)
        elif type == "documents":
            messenger.send_document(document=link, recipient_id=mobile,
                                    caption=caption)


def execute_actions(actions: dict, mobile: str):
    if actions.get("actions"):
        actions = actions.get("actions")
        for action in actions:
            # print(action)
            if action.get("send_message"):
                message = action.get("send_message")
                if isinstance(message, list):
                    message = "\n".join(message)
                messenger.send_message(message=message, recipient_id=mobile)

            elif action.get("send_reply_button"):
                reply_button = action.get("send_reply_button")
                messenger.send_reply_button(
                    button=reply_button, recipient_id=mobile)

            elif action.get("send_button"):
                messenger.send_button(
                    button=action.get("send_button"), recipient_id=mobile)

            elif action.get("send_images"):
                images = action.get("send_images")
                send_medias(images, mobile, "images")

            elif action.get("send_videos"):
                videos = action.get("send_videos")
                send_medias(videos, mobile, "videos")

            elif action.get("send_audios"):
                audios = action.get("send_audios")
                send_medias(audios, mobile, "audios")

            elif action.get("send_documents"):
                documents = action.get("send_documents")
                send_medias(documents, mobile, "documents")

            elif action.get("send_stickers"):
                stickers = action.get("send_stickers")
                send_medias(stickers, mobile, "stickers")

            else:
                logging.info("Unkown message type")


def respond(mobile: str, message: str, message_type: str = "text"):
    """
      Send message to user
    """
    try:

        response = sarufi_bot.respond(
            message=message,
            message_type=message_type,
            channel="whatsapp",
            chat_id=mobile
        )
        execute_actions(actions=response, mobile=mobile)
    except Exception as error:
        logging.error("error while generating response: ", error)


@app.get("/")
async def wehbook_verification(request: Request):
    if request.query_params.get("hub.verify_token") == VERIFY_TOKEN:
        content = request.query_params.get("hub.challenge")
        logging.info("Verified webhook")
        return Response(content=content, media_type="text/plain", status_code=200)

    logging.error("Webhook Verification failed")
    return "Invalid verification token"


@app.post("/")
async def webhook_handler(request: Request, tasks: BackgroundTasks):

    data = await request.json()
    # logging.info("Received webhook data: %s", data)
    changed_field = messenger.changed_field(data)

# os.path.join(os.getcwd(),"media")
    if changed_field == "messages":
        new_message = messenger.is_message(data)
        if new_message:
            mobile = messenger.get_mobile(data)
            name = messenger.get_name(data)
            message_type = messenger.get_message_type(data)

            logging.info(
                f"New Message; sender:{mobile} name:{name} type:{message_type}\n")
            message_id = messenger.get_message_id(data)
            messenger.mark_as_read(message_id)
            if message_type == "text":
                message = messenger.get_message(data)
                name = messenger.get_name(data)
                logging.info("Message: %s", message)

                tasks.add_task(respond,
                               message=message,
                               message_type=message_type,
                               mobile=mobile,
                               )

            elif message_type == "interactive":
                message_response = messenger.get_interactive_response(data)
                intractive_type = message_response.get("type")
                message_id = message_response[intractive_type]["id"]
                message_text = message_response[intractive_type]["title"]
                logging.info(
                    f"Interactive Message; {message_id}: {message_text}")

                tasks.add_task(respond,
                               message=message_id,
                               message_type=message_type,
                               mobile=mobile,
                               )

            elif message_type == "location":
                message_location = messenger.get_location(data)
                message_latitude = message_location["latitude"]
                message_longitude = message_location["longitude"]
                logging.info("Location: %s, %s",
                             message_latitude, message_longitude)

            elif message_type == "image":
                await media_uploads(messenger, data, "image", mobile)

            elif message_type == "video":
                await media_uploads(messenger, data, "video", mobile)

            elif message_type == "audio":
                await media_uploads(messenger, data, "audio", mobile)

            elif message_type == "document":
                await media_uploads(messenger, data, "document", mobile)

            else:
                print(f"{mobile} sent {message_type} \n{data}")

    else:
        delivery = messenger.get_delivery(data)
        if delivery:
            print(f"Message : {delivery}")
        else:
            print("No new message")

    return "OK", 200


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
