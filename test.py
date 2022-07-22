import logging
import requests
from telegram import Update, ForceReply
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    CallbackContext,
)

from bs4 import BeautifulSoup

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

URL = "https://api.openweathermap.org/data/2.5/weather/"
APPID = "f0073aec073f44b014cd174b032cfcda"


def get_weather_url(params):
    """
    Get weather data from OpenWeather
    """
    params["appid"] = APPID
    return requests.get(URL, params=params).json()


# Define a few command handlers. These usually take the two arguments update and
# context.


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(f"Enter the product name:")


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text("Help!")


def url(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    query = update.message.text.lower()
    chat_id = update.message.chat.id
    URL = f"https://asaxiy.uz/product?key={query}"
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")
    # get the first ten products

    products = soup.find_all(
        "div", attrs={"class": "col-6 col-xl-3 col-md-4"}, limit=10
    )

    for product in products:
        image = product.find("div", attrs={"class": "product__item-img"}).find("img")
        image_url = image["data-src"]
        price = product.find("span", attrs={"class": "product__item-price"})
        link = product.find("a", attrs={"class": "title__link"})
        link = link["href"]
        title = product.find("h5", attrs={"class": "product__item__info-title"})
        caption = f"{title.text}\n"
        caption += f"{price.text}\n"
        caption += f"{image_url}"
        context.bot.send_message(chat_id=chat_id, text=caption)
        # print(image["data-src"])
        # print(price.text.strip())
        # print(link["href"])
        # print(title.text.strip())
    # products = soup.find_all(
    #     "div", attrs={"class": "col-6 col-xl-3 col-md-4"}, limit=10
    # )
    # for product in products:
    #     product_image = product.find("div", attrs={"class": "product__item-img"})
    #     product_image = product_image.find("img")["src"]
    #     product_name = product.find("h5", attrs={"class": "product__item__info-title"})
    #     product_price = product.find("span", attrs={"class": "product__item-price"})

    #     update.message.reply_photo(
    #         photo=product_image["src"],
    #         caption=f"{product_name.text}\n{product_price.text}",
    #     )


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("5509269318:AAFB_rA_sMQk0DCAtNHLQZrtpuGgEuanoTU")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, url))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()
