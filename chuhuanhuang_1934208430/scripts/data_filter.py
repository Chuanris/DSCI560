import csv
from bs4 import BeautifulSoup
import os

#open the raw data
with open("../data/raw_data/web_data.html", "r", encoding = "utf-8") as f:
  content = f.read()

#parse with BS4 indent
soup = BeautifulSoup(content, "html.parser")

#marketBanner part
market_data = []
market_data_container = soup.find('div', id = 'market-data-scroll-container', class_ = 'MarketsBanner-marketData')

print("filtering Market Banner")
if market_data_container:
  market_cards = market_data_container.find_all('a', class_ = 'MarketCard-container')
  if market_cards:
    for card in market_cards:
      symbol = card.find('span', class_ = 'MarketCard-symbol').text.strip()
      stock_pos = card.find('span', class_ = 'MarketCard-stockPosition').text.strip()
      change_pct = card.find('span', class_ = 'MarketCard-changesPct').text.strip()
      market_data.append({
	'marketCard_symbol': symbol,
	'marketCard_stockPosition': stock_pos,
	'marketCardchangePct': change_pct
    	})

#latestNews part
latest_news = []

print("filtering Latest News")
#<ul>
news_container = soup.select_one(".LatestNews-list")  
if news_container:
  #<li>
  news_items = news_container.find_all("li", class_ = "LatestNews-item") 
  if news_items:
    for item in news_items:
      timestamp_element = item.find("time", class_ = "LatestNews-timestamp")
      headline_element = item.find("a", class_ = "LatestNews-headline")

      timestamp = timestamp_element.text.strip() if timestamp_element else None
      title = headline_element.text.strip() if headline_element else None
      link = headline_element.get('href') if headline_element else None

      latest_news.append({
        "timestamp": timestamp,
        "title": title,
        "link": link
      })

print("storing results as CSV")
#store marketBanner as CSV
with open("../data/processed_data/market_data.csv", "w", newline = "", encoding = "utf-8") as csvfile:
  writer = csv.DictWriter(csvfile, fieldnames = ['marketCard_symbol', 'marketCard_stockPosition', 'marketCardchangePct'])
  writer.writeheader()
  writer.writerows(market_data)
print("marketBanner CSV created")

#store latestNews as CSV
with open("../data/processed_data/news_data.csv", "w", newline = "", encoding = "utf-8") as csvfile:
  writer = csv.DictWriter(csvfile, fieldnames = ['timestamp', 'title', 'link'])
  writer.writeheader()
  writer.writerows(latest_news)
print("latestNews CSV created")


