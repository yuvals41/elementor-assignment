import requests, csv, logging
from flask import Flask, jsonify

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def write_to_csv(characters: list):
    if characters is None:
        logging.error("No data to write to CSV.")
    
    try:
        with open("humanoid_characters.csv", "w", newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["Name", "Location", "Image"])
            writer.writeheader()
            for character in characters:
                writer.writerow(character)
        logging.info("Data written to CSV successfully.")
    except Exception as e:
        logging.error(f"Failed to write to CSV: {e}")

def get_humanoid_characters_details() -> list:
    results = list()
    page = 1
    logging.info("Requesting api https://rickandmortyapi.com/api/character")

    #breaks when last page is reached
    while True:
        try:
            response = requests.get(f"https://rickandmortyapi.com/api/character?page={page}", timeout=10)
            response.raise_for_status()
            data = response.json()

            for character_details in data["results"]:
                if character_details["species"] == "Human" and character_details["status"] == "Alive" and "Earth" in character_details["origin"]["name"]:
                    results.append({
                                    "Name": character_details["name"], 
                                    "Location": character_details["location"]["name"], 
                                    "Image": character_details["image"]
                                })

            if not data["info"]["next"]:
                break

            page += 1

        except requests.RequestException as err:
            logging.error(f"API request failed: {err}")
            return None
        except Exception as err:
            logging.error(f"Got an error: {err}")
            return None
        
    logging.info("Data fetched successfully.")
    write_to_csv(results)

    return results


@app.route("/healthcheck")
def health():
    return jsonify({'status': 'healthy'}), 200

@app.route("/get_details")
def get_details():
    characters = get_humanoid_characters_details()
    if characters is None:
        return jsonify({'error': 'Failed to fetch data'}), 500
    return jsonify(characters), 200

if "__main__"  == __name__ :
    app.run(host="0.0.0.0",port=8080)