from flask import Flask, request,  jsonify

# CRéation de notre app Flask
app = Flask(__name__) 


@app.route('/', methods=['GET'])
def home():
	"""Route qui retourne du texte"""
	return "Bienvenue sur l'api Flask ! L'application fonctionne 😊"


@app.route('/api/echo', methods=['POST'])
def echo():
	"""
	Route POST qui reçoit des données JSON et les renvoie.
	"""
	
	data = request.get_json()

	if not data:
		return jsonify({
			"erreur": "Aucune donnée JSON reçue...",
			"astuce": "Envoie un body JSON dans postman"
		}), 400

	return jsonify({
		"message": "Aucune donnée JSON reçue...",
		"data": data,
		"status": "succes"
	}), 201

if __name__ == '__main__':
	print("\n" + "=" * 50)

	print("Url de base : http://localhost:5000")
	print("Url de base : http://localhost:5000/api/echo")

	print("\n" + "=" * 50)

	# http://localhost:5000
	app.run(debug=True, host='0.0.0.0', port=5000)