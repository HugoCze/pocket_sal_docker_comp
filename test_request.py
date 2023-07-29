import requests

def save_text_to_file(url, filename):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
        content = response.text

        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)

        print(f"Text successfully saved to {filename}.")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    url = "https://www.pudelek.pl/sprawa-joanny-z-krakowa-kinga-rusin-miazdzy-pis-i-polska-policje-kazali-jej-sie-rozebrac-do-naga-choc-krwawila-6921586600442848a?fbclid=IwAR2XwfbyjdWMuq5ALuZZaQCpM0zIGyUh4wkvQPOEuu8P_-dQqNw0aZaVZGc"
    filename = "pudelek_article.txt"
    save_text_to_file(url, filename)
