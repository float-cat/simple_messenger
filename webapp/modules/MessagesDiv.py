from flask import request

def MessagesDiv():
    toUserId = request.args.get('userid')
    if request.cookies.get("login") \
        and request.cookies.get("password"):
        res = """<script type="text/javascript">
                  userInfo = {
                      login: '""" + request.cookies.get("login") + """',
                      password: '""" + request.cookies.get("password") + """'
                  }
                 </script>
                 <script type="text/javascript" src="/static/MessagesAjax.js">
                 </script>
              """
    if toUserId:
        res += f"""<div>
                    <form name="receiveForm" method="POST" action="/messagesproc">
                     <textarea name="messages"></textarea>
                    </form>
                    <br />
                    <form name="sendForm" method="POST" action="/messagesproc">
                     <input name="typeRequest" style="display: none;">
                     </input>
                     <input name="newMessageTmp" style="display: none;">
                     </input>
                     <input name="toUserId" value="{toUserId}" style="display: none;">
                     </input>
                     <input name="lastId" value="0" style="display: none;">
                     </input>
                     <input name="newMessage">
                     </input>
                     <input type="button" value="Отправить"
                      onclick="msg.send(this.form, '{toUserId}')">
                     </input>
                    </form>
                    <script type="text/javascript">
                     setInterval(
                      () => msg.update(document.forms['sendForm'], '{toUserId}'),
                      2000
                     );
                    </script>
                   </div>
                """
    else:
        res += """<div id="messagesAll">
                   <div id="messagesAllOutput">
                   </div>
                   <form name="allPMInfo">
                    <input name="typeRequest" style="display: none;"
                        value="allPMInfo">
                    </input>
                   </form>
                   <script type="text/javascript">
                    setInterval(
                     () => msg.updateAllPM(document.forms['allPMInfo']),
                     2000
                    );
                   </script>
                  </div>
               """
    return res
