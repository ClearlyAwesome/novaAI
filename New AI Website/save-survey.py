from flask import Flask, request
import csv
import os

app = Flask(__name__)

@app.route('/save-survey', methods=['POST'])
def save_survey():
    print("Received a POST request to /save-survey")  # Debugging message
    data = {
        "Company Name": request.form.get('company_name'),
        "Industry": request.form.get('industry'),
        "Departments": request.form.get('departments'),
        "Participants": request.form.get('participants'),
        "AI Familiarity": request.form.get('ai_familiarity'),
        "AI Usage": request.form.get('ai_usage'),
        "Training Goals": request.form.get('training_goals'),
        "Relevant AI Areas": request.form.get('relevant_ai_areas'),
        "AI Tools Used": request.form.get('ai_tools_used'),
        "AI Tools Interest": request.form.get('ai_tools_interest'),
        "Challenges": request.form.get('ai_challenges'),
        "Specific Requests": request.form.get('specific_requests')
    }
    print("Data extracted:", data)  # Debugging message

    file_path = 'survey_responses.csv'
    try:
        file_exists = os.path.exists(file_path)
        print(f"File exists: {file_exists}")  # Debugging message

        with open(file_path, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if not file_exists:
                print("Creating a new file and adding headers.")  # Debugging message
                writer.writerow(data.keys())
            writer.writerow(data.values())
            print("Data successfully written to file.")  # Debugging message

        return "Survey submitted successfully!", 200
    except Exception as e:
        print(f"Error during saving: {e}")
        return "An error occurred while saving the survey.", 500

if __name__ == "__main__":
    app.run(debug=True)
