from celery import shared_task
import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def get_currency():
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')

    # driver_path = '/usr/share/doc/chromium-driver'  # Set the executable path here
    driver = webdriver.Chrome()

    driver.get("https://banks.az/en/services/currency-rates")
    time.sleep(2)
    x = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'style_one-item__OPF0z')))

    euro_list = ['EUR']
    usd_list = ['USD']
    rub_list = ['RUB']
    tl_list = ['TRY']

    for i in range(4, len(x)):
        if x[i].text == 'USD':
            usd_list.append(f"Bank buys -> {x[i + 2].text} , Bank sells -> {x[i + 3].text} ,")
        if x[i].text == 'EUR':
            euro_list.append(f"Bank buys -> {x[i + 2].text}, Bank sells -> {x[i + 3].text} ")
        if x[i].text == 'RUB':
            rub_list.append(f"Bank buys -> {x[i + 2].text}, Bank sells -> {x[i + 3].text}")
        if x[i].text == 'TRY':
            tl_list.append(f"Bank buys -> {x[i + 2].text}, Bank sells -> {x[i + 3].text}")

        subject = 'Mr.Intigam - At the moment currency'
        message = [usd_list, euro_list, rub_list, tl_list]
        from_mail = settings.EMAIL_HOST_USER
        to_mail = "guluzadeintigam@gmail.com"

        send_mail(subject, str(message), from_mail, [to_mail])

    driver.close()
