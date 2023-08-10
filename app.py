from flask import Flask, render_template, request
import config
import os
import openai

def page_not_found(e):
  return render_template('404.html'), 404


app = Flask(__name__)
app.config.from_object(config.config['development'])
app.register_error_handler(404, page_not_found)

openai.api_key = app.config['OPENAI_KEY']

def createImageFromPrompt(prompt):
    response = openai.Image.create(prompt=prompt, n=3, size="512x512")
    return response['data']

@app.route('/', methods=["GET", "POST"])
def index():
    generated_prompt = ""

    if request.method == 'POST':
        images = []
        prompt = request.form['prompt']
        res = createImageFromPrompt(prompt)

        if len(res) > 0:
            for img in res:
                images.append(img['url'])
                generated_prompt = prompt

    return render_template('index.html', **locals())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000', debug=True)