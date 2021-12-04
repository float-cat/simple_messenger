def MessagesDiv():
    return """<div>
               <form name="receiveForm" method="POST" action="/messagesproc">
                <textarea name="messages"></textarea>
                <input name="typeRequest" style="display: none;">
                </input>
                <input name="lastId" value="0" style="display: none;">
                </input>
                <input type="button" value="Обновить"
                 onclick="msg.update(this.form, '2')">
                </input>
               </form>
               <br />
               <form name="sendForm" method="POST" action="/messagesproc">
                <input name="typeRequest" style="display: none;">
                </input>
                <input name="newMessageTmp" style="display: none;">
                </input>
                <input name="newMessage">
                </input>
                <input type="button" value="Отправить"
                 onclick="msg.send(this.form, '2')">
                </input>
               </form>
               <script type="text/javascript" src="/static/MessagesAjax.js">
               </script>
              </div>
           """
