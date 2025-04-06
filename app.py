import joblib
from flask import Flask, request, jsonify, render_template
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn import datasets

app = Flask(__name__)

# Charger le modèle et le scaler
clf = joblib.load('iris_model.pkl')
scaler = joblib.load('scaler.pkl')

# Charger le dataset Iris pour obtenir les noms des classes
iris = datasets.load_iris()


@app.route('/')
def home():
    return render_template('index.html')

# Route pour la prédiction
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Récupérer les données envoyées par l'utilisateur
        data = request.get_json()

        # Vérifier que les bonnes clés sont présentes
        if not all(key in data for key in ["sepal_length", "sepal_width", "petal_length", "petal_width"]):
            return jsonify({"error": "Missing input data"}), 400

        # Extraire les dimensions de la fleur
        new_data = [[
            data["sepal_length"],
            data["sepal_width"],
            data["petal_length"],
            data["petal_width"]
        ]]

        # Normaliser les données
        new_data_scaled = scaler.transform(new_data)

        # Faire la prédiction
        predicted_class = clf.predict(new_data_scaled)
        predicted_flower = iris.target_names[predicted_class[0]]

        # Retourner la classe prédite sous forme de JSON
        return jsonify({"predicted_class": predicted_flower})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
