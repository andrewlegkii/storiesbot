import os
import logging
import requests
from dotenv import load_dotenv
from pytube import YouTube
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, MessageFilter, Filters


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
TOKEN = '5978160141:AAEv-aR_YApWY0cKKxepNBKyCLwkIfqyQuA'


def start_command(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Привет! Отправь мне ссылку на видео на YouTube, и я скачаю его для тебя.', quote=False)


def download_video(url: str) -> str:
    """Download video from YouTube and return path to downloaded video."""
    yt = YouTube(url)
    stream = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    stream.download()
    return stream.default_filename


def video_handler(update: Update, _: CallbackContext) -> None:
    """Handle video message."""
    # Get video url
    url = update.message.text
    logger.info(f'Received video url: {url}')
    try:
        # Download video
        filename = download_video(url)

        # Send video back to user
        with open(filename, 'rb') as f:
            update.message.reply_video(video=f)

        # Delete downloaded video
        os.remove(filename)
    except Exception as e:
        logger.error(e)
        update.message.reply_text('Не удалось скачать видео. Попробуйте еще раз позже.')


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add command handler
    dispatcher.add_handler(CommandHandler('start', start_command))

    # Add video message handler
    dispatcher.add_handler(MessageHandler(Filters.video, video_handler))


    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
