from flask import render_template

def IndexPage():
    title = 'SimpleMessenger - главная страница'
    return render_template('index.html', page_title=title)
