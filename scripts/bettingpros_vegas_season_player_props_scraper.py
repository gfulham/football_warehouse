from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Set up headless browser
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

base_url = "https://www.bettingpros.com"
main_url = f"{base_url}/nfl/odds/player-futures/"
driver.get(main_url)
time.sleep(5)  # let JS load

# Get player links
links = driver.find_elements(By.CSS_SELECTOR, "a.player-link")  # links to player future pages
player_urls = []
seen_names = set()

for link in links:
    name = link.text.strip()
    href = link.get_attribute("href")
    if name and name not in seen_names:
        seen_names.add(name)
        player_urls.append((name, href))
    if len(player_urls) >= 100:
        break

print(f"Collected {len(player_urls)} player URLs.")

# Collect data per player
all_data = []

for name, url in player_urls:
    driver.get(url)
    time.sleep(3)

    try:
        position = driver.find_element(By.CSS_SELECTOR, ".player-info__meta").text.split("•")[0].strip()
    except:
        position = "Unknown"

    rows = driver.find_elements(By.CSS_SELECTOR, ".odds-prop__item")
    for row in rows:
        try:
            category = row.find_element(By.CLASS_NAME, "odds-prop__label").text.strip()
            line = row.find_element(By.CLASS_NAME, "odds-prop__line").text.strip()
            odds = row.find_element(By.CLASS_NAME, "odds-prop__odds").text.strip()
            all_data.append({
                "Player": name,
                "Position": position,
                "Category": category,
                "Line": line,
                "Odds": odds,
                "URL": url
            })
        except:
            continue

# Save to CSV
df = pd.DataFrame(all_data)
df.to_csv("player_futures_odds.csv", index=False)
print("Saved player_futures_odds.csv")

driver.quit()
