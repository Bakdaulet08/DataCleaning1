from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
wait = WebDriverWait(driver, 20)

try:
    driver.get("https://my.sdu.edu.kz/index.php?mod=transkript")

    table = wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
    rows = table.find_elements(By.TAG_NAME, "tr")

    data = []
    current_year = ""

    for row in rows:
        tds = row.find_elements(By.TAG_NAME, "td")
        if not tds:
            continue

        if "font-weight:bold" in row.get_attribute("innerHTML") and "padding-top:10px" in row.get_attribute("innerHTML"):
            current_year = tds[0].text.strip()
            continue

        if len(tds) >= 7:
            data.append({
                'Year': current_year,
                'Code': tds[0].text.strip(),
                'Title': tds[1].text.strip(),
                'Credits': tds[2].text.strip(),
                'Hours': tds[3].text.strip(),
                'Grade': tds[4].text.strip(),
                'Letter': tds[5].text.strip(),
                'GPA': tds[6].text.strip()
            })

    if data:
        df = pd.DataFrame(data)
        df.to_csv('transcript.csv', index=False, encoding='utf-8-sig')
        print("Saved to transcript.csv")
    else:
        print("No data found")

except Exception as e:
    print(f"Error: {e}")
    driver.save_screenshot("error.png")

finally:
    driver.quit()
