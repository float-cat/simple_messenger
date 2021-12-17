from flask import render_template, redirect, url_for, flash
from flask_login import current_user
from webapp.FORMS import simple_messenger_reg

def NewGroupMessagesPage():
    if current_user.is_authenticated:
        return """<script src="/static/MessagesAjax.js">
                  </script>
                  <form name="newgm">
                    <input name="caption">
                    </input>
                    <input type="button" value="Создать"
                        onclick="msg.createNewGM(this.form)">
                    </input>
                  </form>
               """
