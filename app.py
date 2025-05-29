from flask import Flask, render_template, request
from utils.web_fallback import search_tool
from utils.pdf_vectorstore import load_and_index_pdf
from utils.query_pdf import query_pdf
from markupsafe import Markup
import markdown

pdf_path = "data/Dream_Textbook.pdf"
load_and_index_pdf(pdf_path)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    answer = ""
    web_info = ""
    user_input = ""
    if request.method == 'POST':
        user_input = request.form.get('question')
        answer = query_pdf(user_input)
        html_answer = Markup(markdown.markdown(answer))

        if "more_info" in request.form:
            web_info = search_tool(user_input)

    return render_template("index.html", question=user_input, answer=html_answer, web_info=web_info)

if __name__ == '__main__':
    app.run(debug=True)
