import requests
from bs4 import BeautifulSoup
import pandas as pd


class Card:
    def __init__(self, title, price, top_prize, num_prizes):
        self.title = title
        self.price = price
        self.top_prize = top_prize
        self.num_prizes = num_prizes

url = "https://www.national-lottery.co.uk/games/gamestore/scratchcards"
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

games = []
games.extend(soup.find_all('tr', class_='even'))
games.extend(soup.find_all('tr', class_='odd'))

cards = []

fp = None
for game in games:
    if not game.find('td', {'data-th': 'Game Name'}):
        fp = game

if fp in games:
    games.remove(fp)

for game in games:
    title = game.find('td', {'data-th': 'Game Name'}).find('a').text.strip()
    price = game.find('td', {'data-th': 'Price'}).text.strip()
    top_prize = game.find('td', {'data-th': 'Prize amount'}).text.strip()[1:]
    num_prizes = game.find('td', {'data-th': 'No. of remaining top prizes'}).text.strip()

    cards.append(Card(title, price, top_prize, num_prizes))

best_card = cards[0] 
for card in cards:
    if int(card.num_prizes) > int(best_card.num_prizes):
        best_card = card

print(f"Best scratchcard: {best_card.title}\nNumber of prizes left: {best_card.num_prizes}")
