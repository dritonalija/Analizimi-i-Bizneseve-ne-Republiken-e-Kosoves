import requests
import gender_guesser.detector as gender
from nameparser import HumanName
# Funksioni për të parashikuar gjininë për një listë emrash duke përdorur Genderize.io
def predict_genders_with_genderize(names):
    # Përgatit URL-në duke shtuar parametrat `name[]` për secilin emër
    url = "https://api.genderize.io/"
    params = [("name[]", name) for name in names]
    
    # Bën kërkesën HTTP GET
    response = requests.get(url, params=params)
    
    # Kontrollon nëse kërkesa është kryer me sukses
    if response.status_code == 200:
        data = response.json()
        # Kthen një fjalor ku emrat janë çelësat dhe gjinia është vlera
        return {entry['name']: entry.get('gender', 'unknown') for entry in data}
    else:
        # Në rast gabimi, printo statusin dhe mesazhin e gabimit
        print("Gabim:", response.status_code, response.text)
        return None
    
# Inicializojmë detektuesin e gjinisë
d = gender.Detector()

def predict_genders_with_gender_guesser(name):
    first_name = HumanName(name).first  # merr vetëm emrin e parë
    guess = d.get_gender(first_name)
    if guess in ['male', 'mostly_male']:
        return 'Mashkull'
    elif guess in ['female', 'mostly_female']:
        return 'Femër'
    else:
        return 'Panjohur'

# Lista e emrave për të cilët duam të parashikojmë gjininë
names = ["Emri"]

# Thirr funksionin dhe printo rezultatet
genders = predict_genders_with_genderize(names)

print(genders)
