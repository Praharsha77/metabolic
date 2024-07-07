from flask import Flask, render_template, request
import pandas as pd
import pickle
from werkzeug.utils import quote

app = Flask(__name__)

with open('model.pkl', 'rb') as f:
    model = pickle.load(f)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        if request.method == 'POST':
            age = float(request.form['age'])
            height = float(request.form['height'])
            weight = float(request.form['weight'])
            duration = float(request.form['duration'])
            heart_rate = float(request.form['heart_rate'])
            body_temp = float(request.form['body_temp'])
            gender = request.form['gen']

            gender_encoded = encode_gender(gender)
            if gender_encoded is None:
                return "Invalid gender value", 400

            user_data = pd.DataFrame({
                'Age': [age],
                'Height': [height],
                'Weight': [weight],
                'Duration': [duration],
                'Heart_Rate': [heart_rate],
                'Body_Temp': [body_temp],
                'Gender': [gender_encoded]
            })

            user_data = user_data[['Gender', 'Age', 'Height', 'Weight', 'Duration', 'Heart_Rate', 'Body_Temp']]

            calories = model.predict(user_data)[0]

            return render_template('result.html', calories=calories)
    except Exception as e:
        return str(e), 500


@app.route('/recommendation', methods=['POST'])
def recommendation():
    try:
        calories = float(request.form.get('calories', 0))
        recommendations = get_diet_recommendations(calories)
        videos = get_videos()
        articles = get_articles()
        return render_template('Recommendation.html', recommendations=recommendations, videos=videos, articles=articles)
    except Exception as e:
        return str(e), 500


def encode_gender(gender):
    if gender == 'male':
        return 0
    elif gender == 'female':
        return 1
    else:
        return None


def get_diet_recommendations(calories):
    if calories < 200:
        return "Consider light snacks like a piece of fruit or a small handful of nuts. ..."
    elif 200 <= calories < 500:
        return "You could have a balanced snack, such as yogurt with granola or a smoothie. ..."
    elif 500 <= calories < 800:
        return "A small meal with lean protein, whole grains, and vegetables would be beneficial. ..."
    else:
        return "A hearty meal with a good balance of protein, carbs, and fats is recommended. ..."


def get_videos():
    return [
        {
            "title": "Top 5 Benefits of Exercise | Why Exercise is Important",
            "thumbnail": "https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg",
            "link": "https://www.youtube.com/user/FitnessBlender"
        },
        {
            "title": "Exercise and Weight Loss | The Ultimate Guide",
            "thumbnail": "https://img.youtube.com/vi/3C2WThErFZ0/mqdefault.jpg",
            "link": "https://www.youtube.com/user/yogawithadriene"
        }
    ]


def get_articles():
    return [
        {
            "title": "10 Benefits of Regular Exercise",
            "link": "https://www.healthline.com/nutrition/10-benefits-of-exercise"
        },
        {
            "title": "How Much Exercise Do You Really Need?",
            "link": "https://www.mayoclinic.org/healthy-lifestyle/fitness/in-depth/exercise/art-20048389"
        }
    ]


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
