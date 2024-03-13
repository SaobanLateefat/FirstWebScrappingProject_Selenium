from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


website = 'https://playgroundsafety.org/take-action/find-playground-inspector'
path = r'C:\Users\SAOBAN\PycharmProjects\chromedriver-win64\chromedriver.exe'
driver = webdriver.Chrome()
driver.get(website)
driver.maximize_window()

# Wait for the container to be present
containers = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.XPATH, "//div[@class='inspector-row']"))
)

data = []

for container in containers:
    try:
        # Extract the text from the <div> element (containing the name)
        name_divs = container.find_elements(By.XPATH, "./div")
        for name_div in name_divs:
            name_parts = name_div.text.split()
            first_name = name_parts[0]
            last_name = name_parts[1]

        # Extract the email addresses
        email_links = container.find_elements(By.XPATH, "./a[contains(@href, 'mailto:')]")
        for email_link in email_links:
            email = email_link.text

        # Extract the phone number
        phone_links = container.find_elements(By.XPATH,"./a[contains(@href, 'tel:')]")
        for phone_link in phone_links:
            phone = phone_link.text


        # Extract the city and state
        address_spans = container.find_elements(By.XPATH, "./address/span")
        for address_span in address_spans:
            city_state = address_span.text.split(',')
            city = city_state[0].strip()
            state = city_state[1].strip()
            data.append({'First Name': first_name, 'Last Name': last_name, 'Email': email, 'Phone': phone, 'City': city, 'State': state})

    except Exception as e:
        print("An error occurred:", e)

# Create a dataframe from the list of dictionaries
df = pd.DataFrame(data)

# Save the DataFrame as a CSV file
df.to_csv('ins_data.csv', index=False)

# Print a message indicating the file has been saved
print("CSV file saved successfully.")

driver.quit()
