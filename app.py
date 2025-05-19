from flask import Flask, request, render_template, jsonify
import pickle
import nltk
nltk.download('punkt')

# Load the trained model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

app = Flask(__name__, static_folder='static')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get the SMS text from the form
    sms_text = request.form.get('sms')
    
    # Transform and predict
    prediction = model.predict([sms_text])[0]
    
    # Return the result
    result = "Spam" if prediction == 1 else "Ham"
    
    # Return JSON if requested
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'result': result})
    
    # Otherwise return the HTML with the result included
    # Make sure the result is clearly marked in the HTML for the JS to find
    return render_template('index.html', result=result, sms_text=sms_text)

if __name__ == "__main__":
    app.run(debug=True)