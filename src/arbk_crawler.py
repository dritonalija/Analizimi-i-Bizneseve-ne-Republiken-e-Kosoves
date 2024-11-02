import csv
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import os

# Ekstrakto dhe pastro "Emri i biznesit" nga rreshtat ku "Komuna" është "I panjohur"
def extract_cleaned_business_names(csv_file_path, field_to_search, value_to_search):
    business_names = set()  # Përdor një set për të shmangur dublikatat
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Kontrollo nëse fusha e caktuar përmban vlerën e kërkuar
            if row[field_to_search] == value_to_search:
                # Ndaj emrin e biznesit në fjalë
                business_name_words = row['Emri i biznesit'].split()
                # Hiq fjalën e fundit nëse përmban një pikë
                if business_name_words and '.' in business_name_words[-1]:
                    business_name_words.pop()  # Hiq fjalën e fundit
                # Rikonstrukto emrin e biznesit pa fjalën e fundit nëse është hequr
                business_name = ' '.join(business_name_words).strip()
                business_names.add(business_name)
    return list(business_names)

# Përdor emrat e biznesit të ekstraktuar si terma kërkimi në skriptën Playwright
def fill_form_and_capture_response(search_terms):
    target_url = "https://arbk.rks-gov.net/"  # Uebfaqja e synuar
    api_capture_url = "https://arbk.rks-gov.net/api/api/Services/KerkoBiznesin"  # URL-ja specifike e API për të kapur përgjigjen
    output_csv_file = "../data/raw/arbk_crawler_data.csv"  # File CSV për të ruajtur të dhënat

    with sync_playwright() as p:
        # Hap shfletuesin
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # Defino një funksion për të kapur përgjigjet e rrjetit
        def log_response(response):
            if api_capture_url in response.url and response.status == 200:
                # Kap përmbajtjen e përgjigjes si JSON
                response_body = response.json()
                if response_body:
                    # Kontrollo nëse "teDhenatBiznesit" është e pranishme në çdo hyrje të përgjigjes
                    for entry in response_body:
                        if "teDhenatBiznesit" in entry:
                            business_data = entry["teDhenatBiznesit"]

                            # Kontrollo nëse file CSV ekziston dhe ka përmbajtje
                            file_exists = os.path.isfile(output_csv_file) and os.path.getsize(output_csv_file) > 0

                            # Hap file CSV në modalitetin e shtimit dhe shkruaj të dhënat
                            with open(output_csv_file, mode='a', newline='', encoding='utf-8') as file:
                                writer = csv.DictWriter(file, fieldnames=business_data.keys())
                                # Shkruaj header vetëm nëse file është bosh
                                if not file_exists:
                                    writer.writeheader()
                                writer.writerow(business_data)
                            print(f"Të dhënat për '{business_data.get('Emri i biznesit', 'Unknown')}' janë ruajtur në {output_csv_file}")
                else:
                    print("Nuk u gjetën të dhëna të vlefshme në përgjigje.")

        # Vendos një dëgjues të ngjarjes së përgjigjes para se të nisë kërkimin
        page.on("response", log_response)

        # Shko te faqja e synuar vetëm një herë
        page.goto(target_url)

        # Përsërit për çdo term kërkimi në varg
        for search_term in search_terms:
            print(f"Duke kërkuar për: {search_term}")

            # Kontrollo nëse CAPTCHA është i pranishëm duke përdorur `wait_for_selector` me timeout të shkurtër
            try:
                page.wait_for_selector('iframe[src*="https://www.google.com/recaptcha/api2/bframe"]', timeout=3000)
                print("CAPTCHA e detektuar! Ju lutem, zgjidhni atë manualisht dhe shtypni Enter për të vazhduar.")
                input("Pasi të keni zgjidhur CAPTCHA-n, shtypni Enter për të vazhduar...")  # Pauzo derisa të zgjidhet manualisht
            except PlaywrightTimeoutError:
                # Vazhdon vetëm nëse CAPTCHA nuk u gjet brenda timeout-it të specifikuar
                pass

            # Fshi përmbajtjen e fushës së kërkimit, plotëso formularin me termin aktual të kërkimit
            page.fill("input[placeholder='Emri i Biznesit']", search_term)

            # Dërgo formularin duke shtypur Enter
            page.press("input[placeholder='Emri i Biznesit']", "Enter")

            # Prit disa sekonda për të lejuar kapjen e përgjigjes
            page.wait_for_timeout(5000)  # Rregullo kohën e pritjes nëse është e nevojshme

        # Mbyll shfletuesin
        browser.close()

# Rruga drejt file-it CSV që përmban "Komuna" dhe "Emri i biznesit"
input_csv_file = '../data/processed/prepared_data.csv'  # Zëvendëso me rrugën e file-it tuaj CSV

# Ekstrakto emrat e bizneseve nga CSV ku "Komuna" është "I panjohur"
search_terms = extract_cleaned_business_names(input_csv_file, field_to_search='Komuna', value_to_search='I panjohur')

# Ekzekuto funksionin me termat e kërkimit të ekstraktuar
fill_form_and_capture_response(search_terms)
