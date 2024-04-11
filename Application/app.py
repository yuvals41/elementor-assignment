import requests, csv, logging
from flask import Flask, jsonify

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_humanoid_characters_details() -> list:
    results = list()
    page = 1
    logging.info("Requesting api https://rickandmortyapi.com/api/character")

    #breaks when last page is reached
    while True:
        try:
            response = requests.get(f"https://rickandmortyapi.com/api/character?page={page}")
            response.raise_for_status()
            data = response.json()

            for character_details in data["results"]:
                if character_details["species"] == "Human" and character_details["status"] == "Alive" and "Earth" in character_details["origin"]["name"]:
                    results.append({
                                    "Name": character_details["name"], 
                                    "Location": character_details["location"]["name"], 
                                    "Image": character_details["image"]
                                })

            if data["info"]["next"]:
                page += 1
            else:
                break

        except requests.RequestException as err:
            logging.error(f"API request failed: {err}")
            return None
        except Exception as err:
            logging.error(f"Got an error: {err}")
            return None
        
    logging.info("Data fetched successfully.")

    #i put the csv writer here so you can see i did the first step, instead of removing it or writing it as a function that i dont use
    with open("humaniod_character_details.csv", "w") as csvfile:
        csv_writer = csv.DictWriter(csvfile,fieldnames=["Name", "Location", "Image"])
        logging.info("Writing to csv")

        for result in results:
            csv_writer.writerow(result)

    return results


@app.route("/health")
def health():
    return jsonify({'status': 'healthy'}), 200

@app.route("/get_details")
def get_details():
    return get_humanoid_characters_details(), 200

if "__main__"  == __name__ :
    app.run(host="0.0.0.0",port=8080)