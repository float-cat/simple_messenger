from flask import request, render_template, redirect, url_for, flash
from flask_login import current_user
from webapp.FORMS import simple_messenger_messages

def MessagesPage():
    title = "Сообщения"
    # Создаем форму для отправки сообщений
    messages_forms = simple_messenger_messages()
    toUserId = request.args.get('userid')
    toChatId = request.args.get('chatid')
    if toChatId:
        toUserId = 'c' + toChatId
    if current_user.is_authenticated:
        return render_template(
            'messenger.html',
            page_title=title,
            form=messages_forms,
            user_name=current_user.login,
            toUserId=toUserId)
    else:
        flash('Авторизуйтесь пожалуйста')
        return redirect(url_for('auth'))
