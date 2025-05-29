from flask import Flask, render_template, request
from utils.web_fallback import search_tool
from utils.vector_store import create_vector_store
from utils.qa_engine import answer_question

db = create_vector_store()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    answer = ""
    web_info = ""
    user_input = ""
    if request.method == 'POST':
        user_input = request.form.get('question')
        answer = answer_question(db, user_input)

        if "more_info" in request.form:
            web_info = search_tool(user_input)

    return render_template("index.html", question=user_input, answer=answer, web_info=web_info)

if __name__ == '__main__':
    app.run(debug=True)
