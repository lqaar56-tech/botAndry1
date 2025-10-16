import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Токен
TOKEN = "7576277750:AAE6KPdzhtEOUi3i12vgK5H5S7w2OrwaqiA"
bot = telebot.TeleBot(TOKEN)

# Сделки
deals = [
    {"nft_link": "PlushPepe #2536", "rarity": "💎 Легендарный", "seller_tag": "@seller_plushpepe",
     "market_link": "https://t.me/nft/PlushPepe-2536", "score": 10.0},  # Лучшая
    {"nft_link": "LowRider #7302", "rarity": "✨ Редкий", "seller_tag": "@seller_lowrider",
     "market_link": "https://t.me/nft/LowRider-7302", "score": 9.0},
    {"nft_link": "EvilEye #40584", "rarity": "⭐️ Обычный", "seller_tag": "@seller_evileye",
     "market_link": "https://t.me/nft/EvilEye-40584", "score": 8.5},
    {"nft_link": "ArtisanBrick #1452", "rarity": "✨ Редкий", "seller_tag": "@seller_artisan1452",
     "market_link": "https://t.me/nft/ArtisanBrick-1452", "score": 8.8},
    {"nft_link": "ArtisanBrick #1184", "rarity": "⭐️ Обычный", "seller_tag": "@seller_artisan1184",
     "market_link": "https://t.me/nft/ArtisanBrick-1184", "score": 8.7}
]

# Форматирование сделки
def format_deal(deal):
    return f"{deal['nft_link']} | {deal['rarity']} | {deal['seller_tag']}"

# Главное меню
def main_menu():
    kb = InlineKeyboardMarkup()
    # Лучшая сделка фиксированно PlushPepe
    best = deals[0]
    kb.add(InlineKeyboardButton("🔥 Лучшая сделка", url=best['market_link']))
    kb.add(InlineKeyboardButton("📜 Все сделки", callback_data="show_all"))
    return kb

# Кнопки со списком всех сделок
def deals_menu():
    kb = InlineKeyboardMarkup()
    for deal in deals:
        kb.add(InlineKeyboardButton(format_deal(deal), url=deal["market_link"]))
    return kb

# /start
@bot.message_handler(commands=['start'])
def start(message):
    text = (
        "👋 Привет! Я — твой помощник по NFT-подаркам 🎁\n\n"
        "Выбирай команду ниже или через кнопки:\n"
        "/bestdeal — показать лучшую сделку\n"
        "/alldeals — показать все сделки"
    )
    bot.send_message(message.chat.id, text, reply_markup=main_menu())

# /bestdeal
@bot.message_handler(commands=['bestdeal'])
def bestdeal_cmd(message):
    best = deals[0]  # фиксируем PlushPepe как лучшую
    text = f"💎 *Лучшая сделка:*\n{format_deal(best)}\n\nВыбери одну из сделок ниже:"
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=deals_menu())

# /alldeals
@bot.message_handler(commands=['alldeals'])
def alldeals_cmd(message):
    text = "📜 *Все доступные NFT-сделки:*\n\nВыбери интересующую через кнопки:"
    bot.send_message(message.chat.id, text, parse_mode="Markdown", reply_markup=deals_menu())

# Колбэки (меню)
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "show_all":
        text = "📜 Выбери сделку из списка ниже:"
        bot.send_message(call.message.chat.id, text, reply_markup=deals_menu())
        bot.answer_callback_query(call.id)
    else:
        bot.answer_callback_query(call.id, "Неизвестная команда.")

# Ловим любые сообщения
@bot.message_handler(func=lambda message: True)
def any_text(message):
    bot.reply_to(message, "Используй /start, /bestdeal или /alldeals для работы со мной!")

# Запуск
if __name__ == "__main__":
    print("Бот запущен...")
    bot.polling(none_stop=True)



import json
from typing import List, Dict, Any


class TelegramGiftFilter:
    def init(self, gifts: List[Dict[str, Any]]):
        self.gifts = gifts

    def filter(
        self,
        pattern: str = None,
        background: str = None,
        model: str = None,
        rarity: str = None,
        collection: str = None,
        mint_range: tuple = None
    ) -> List[Dict[str, Any]]:
        """Фильтрует подарки по заданным критериям"""
        result = self.gifts

        if pattern:
            result = [g for g in result if g.get("pattern") == pattern]
        if background:
            result = [g for g in result if g.get("background") == background]
        if model:
            result = [g for g in result if g.get("model") == model]
        if rarity:
            result = [g for g in result if g.get("rarity") == rarity]
        if collection:
            result = [g for g in result if g.get("collection") == collection]
        if mint_range:
            low, high = mint_range
            result = [
                g for g in result
                if low <= int(g.get("mint_number", 0)) <= high
            ]
        return result

    def list_unique(self, key: str) -> List[str]:
        """Возвращает все уникальные значения по ключу (например, все узоры или модели)"""
        return sorted(set(g.get(key) for g in self.gifts if g.get(key)))

    def rarity_score(self, gift: Dict[str, Any]) -> float:
        """Вычисляет условную редкость подарка"""
        weights = {
            "pattern": 0.35,
            "background": 0.25,
            "model": 0.15,
            "rarity": 0.2,
            "mint_number": 0.05,
        }
        score = 0
        for key, weight in weights.items():
            value = gift.get(key)
            if not value:
                continue
            rarity_value = 1 / (self._frequency(key, value) or 1)
            score += rarity_value * weight
        return round(score, 4)

    def _frequency(self, key: str, value: str) -> int:
        """Считает, сколько раз встречается значение (нужно для rarity_score)"""
        return sum(1 for g in self.gifts if g.get(key) == value)


# === Пример использования ===

if name == "main":
    # Загружаем данные (можно заменить на реальное API)
    with open("gifts.json", "r", encoding="utf-8") as f:
        gifts = json.load(f)

    gf = TelegramGiftFilter(gifts)

    # Все уникальные узоры, фоны и коллекции
    print("Узоры:", gf.list_unique("pattern"))
    print("Фоны:", gf.list_unique("background"))
    print("Коллекции:", gf.list_unique("collection"))

    # Фильтр: редкие подарки с узором "Haunted House" из коллекции "Halloween"
    rare_ones = gf.filter(pattern="Haunted House", collection="Halloween")
    print(f"Найдено {len(rare_ones)} редких подарков!")

    # Подсчёт редкости первого найденного
    if rare_ones:
        print("Редкость первого:", gf.rarity_score(rare_ones[0]))