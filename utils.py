import os
import logging
media_file_path="media"

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s" )



def create_media_folders()->None:
  os.getcwd()
  media_files=['audios','images','documents','videos']
  
  if os.path.exists(media_file_path):
    os.chdir(media_file_path)
    for file in media_files:
      if not os.path.exists(file):
        os.mkdir(file)

  else:
    os.mkdir(media_file_path)
    os.chdir(media_file_path)
    for file in media_files:
      if not os.path.exists(file):
        os.mkdir(file)

  os.chdir("..")


async def media_uploads(messenger,data,message_type,mobile=None):
  create_media_folders()
  if message_type == "image":
    image = messenger.get_image(data)
    image_id, mime_type = image["id"], image["mime_type"]
    image_url = messenger.query_media_url(image_id)
    file_name=f"{image_id}_{mobile}"
    image_filename = messenger.download_media(image_url,
                                              mime_type,
                                              file_path=f"{media_file_path}/{message_type}s/{file_name}")
    
    logging.info(f"{mobile} sent image {image_filename}")

  elif message_type == "video":
    video = messenger.get_video(data)
    video_id, mime_type = video["id"], video["mime_type"]
    video_url = messenger.query_media_url(video_id)
    file_name=f"{video_id}_{mobile}"
    video_filename = messenger.download_media(video_url, mime_type,file_path=f"{media_file_path}/{message_type}s/{file_name}")
    logging.info(f"{mobile} sent video {video_filename}")

  elif message_type == "audio":
    audio = messenger.get_audio(data)
    audio_id, mime_type = audio["id"], audio["mime_type"]
    audio_url = messenger.query_media_url(audio_id)
    file_name=f"{audio_id}_{mobile}"
    audio_filename = messenger.download_media(audio_url, mime_type,file_path=f"{media_file_path}/{message_type}s/{file_name}")
    logging.info(f"{mobile} sent audio {audio_filename}")

  elif message_type == "document":
    file = messenger.get_document(data)
    file_id, mime_type = file["id"], file["mime_type"]
    file_url = messenger.query_media_url(file_id)
    file_name=f"{file_id}_{mobile}"
    file_filename = messenger.download_media(file_url, mime_type,file_path=f"{media_file_path}/{message_type}s/{file_name}")
    logging.info(f"{mobile} sent file {file_filename}")