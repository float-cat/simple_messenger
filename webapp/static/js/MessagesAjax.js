msg = {
    touid: 0,
    prevCount: -1,
    prevPrevCount: 0,
    lastId: 0,
    delta: 0,
    chatCount: 10,
    chatCountLimited: 20,

    async loadByScroll(form)
    {
        let elem = document.getElementById('receiveDiv');
        elem.addEventListener('scroll', function() {
            if(elem.scrollTop < 50 && msg.prevCount > 0 
                && msg.prevCount != msg.prevPrevCount)
            {
                msg.prevPrevCount = msg.prevCount;
                /* Прокручиваем прокрутку */
                let obj = document.getElementById('receiveDiv');
                obj.scrollTo(0, 60);
                msg.loadPrevMessages(form);
            }
        })
    },

    async loadByScrollOfList(form)
    {
        let elem = document.getElementById('messagesAllOutput');
        elem.addEventListener('scroll', function() {
            if(msg.chatCountLimited >= msg.chatCount &&
                elem.scrollTop + elem.offsetHeight > elem.scrollHeight - 20)
            {
                msg.chatCount += 10;
                msg.updateAllPM(document.forms['allPMInfo'], true)
            }
        })
    },

    /* Метод добавляет новое сообщение в чат */
    async setPM(idx, login, message, time, isOwner, isNew)
    {
        output = document.getElementById('receiveDiv');

        /* Проверяем есть ли такая переписка */
        /* Если нет, то создаем новую */
        newDiv = document.createElement('div');
        newDiv.id = 'message' + idx;
        if(isNew)
            output.append(newDiv);
        else
            output.prepend(newDiv);
        /* Обновляем сообщение */
        if (isOwner == 1){
            newDiv.innerHTML = '<div class="row justify-content-start">\
                <div class=" col col-11 col-sm-11 col-md-8\
                col-lg-6 alert alert-primary paddingmessage"\
                role="alert"><b>' + login + '&nbsp;</b> ' + time
                + '<p>' + message + '</p></div></div>';}
        else{
            newDiv.innerHTML = '<div class="row justify-content-end">\
                <div class=" col-11 col-sm-11 col-md-8\
                col-lg-6 col alert alert-secondary paddingmessage"\
                role="alert"><b>' + login + '&nbsp;</b> ' + time
                + '<p>' + message + '</p></div></div>';}



    },

    /* Метод обновляет или добавляет новую переписку */
    async setPMInfo(idx, login, message, time, isNewMessages)
    {
        let isChat = false;
        output = document.getElementById('messagesAllOutput');
        /* Проверяем групповая переписка или личная */
        if (idx[0] == 'c')
        {
            isChat = true;
            idx = idx.slice(1);
        }
        /* Проверяем есть ли такая переписка (div заменен на a) */
        let newA = document.getElementById('user' + idx);
       	if(isChat)
       	    newA = document.getElementById('chat' + idx);
        let url = (new URL(document.location)).searchParams;

        if(newA === null)
        {
            /* Если нет, то создаем новую */
            newA = document.createElement('a');
            if(isChat)
                newA.setAttribute("href", "messages?chatid=" + idx);
            else
                newA.setAttribute("href", "messages?userid=" + idx);
            if ((idx == url.get('userid') && !isChat)
                || (idx == url.get('chatid') && isChat))
            {
                newA.className = 'list-group-item list-group-item-action\
                    active py-3 lh-tight';
                newA.setAttribute("aria-current", "true");
            }
            else {
                newA.className = 'list-group-item\
                    list-group-item-action py-3 lh-tight';
            }
            if(isChat)
                newA.id = 'chat' + idx;
            else
                newA.id = 'user' + idx;
        }
        else
            newA.parentNode.removeChild(newA);
        if(isNewMessages)
            output.prepend(newA);
        else
            output.append(newA);
        /* Обновляем сообщение */
        newA.innerHTML ='<div class="d-flex w-100\
            align-items-center justify-content-between"><strong class="mb-1">'
            + login + '</strong><small>' + time
            + '</small></div><div class="col-10 mb-1 small">'
            + message + '</div>';
    },

    async setNewPM(result)
    {
        let newLastId = parseInt(result['lastid']);
        msg.delta = newLastId - msg.lastId;
        msg.lastId = newLastId;
        if (msg.prevCount < 0)
            msg.prevCount = parseInt(result['prevcount']);
        for(let idx = 0; idx < result['count']; idx++)
        {
            msg.setPM(
                result['msgids'][idx],
                result[result['msgids'][idx]]['login'],
                result[result['msgids'][idx]]['message'],
                result[result['msgids'][idx]]['time'],
                result[result['msgids'][idx]]['isOwner'],
                true
            );
        }
    },

    async setPrevPM(result)
    {
        msg.prevCount = parseInt(result['prevcount']);
        for(let idx = result['count'] - 1; idx >= 0; idx--)
        {
            msg.setPM(
                result['msgids'][idx],
                result[result['msgids'][idx]]['login'],
                result[result['msgids'][idx]]['message'],
                result[result['msgids'][idx]]['time'],
                result[result['msgids'][idx]]['isOwner'],
                false
            );
        }
    },

    async setAllPM(result)
    {
        for(let idx = 0; idx < result['count']; idx++)
        {
            msg.setPMInfo(
                result['msgids'][idx],
                result[result['msgids'][idx]]['login'],
                result[result['msgids'][idx]]['message'],
                result[result['msgids'][idx]]['time'],
                result['isnewmessages'] == 1
            );
        }
        if(result['isnewmessages'] == 0)
            msg.chatCountLimited = result['count'] + 20;
    },

    /* Метод, создающий новую групповую переписку */
    async createNewGM(form)
    {
        let formData = new FormData(form);
        formData.append('typeRequest', 'newGM');

        /* Выполняем POST-запрос */
        let response = await fetch('/messagesproc', {
            method: 'POST',
            body: formData
        });

        /* Получаем результат */
        let result = await response.json();

        /* Редиректим на страницу нового чата */
        document.location = '/messages?chatid=' + result['newgm']
    },


    /* Метод, получающий список пользователей в переписке */
    async getUserListOfGM(form)
    {
        let formData = new FormData(form);
        formData.append('typeRequest', 'listusersofGM');
        let url = (new URL(document.location)).searchParams;
        let chatId = url.get('chatid');
        if (chatId != null) 
            formData.append('chatId', chatId);
        else
            return;

        /* Выполняем POST-запрос */
        let response = await fetch('/messagesproc', {
            method: 'POST',
            body: formData
        });

        /* Получаем результат */
        let result = await response.json();

        let outputelem = document.getElementById('outputUserList');
        outputelem.innerHTML = '';
        outputelem.innerHTML +='<ul class="list-group">'
        for(let idx = 0; idx < result['count']; idx++)
        {
            let newDiv = document.createElement('div');
            newDiv.id = 'user' + idx;

            if(result['isowner'] == '1')
            {
                newDiv.innerHTML = '<li class="list-group-item"> <input type="button" class="btn btn-outline-danger btn-sm" \
                    onclick="msg.dropFromGM('
                    + chatId + ', '
                    + result['msgids'][idx] + ')" value="-"></input>' +  '&nbsp;&nbsp;' + result[result['msgids'][idx]]['login'] +'</li>';
            }


            outputelem.append(newDiv);
        }
        outputelem.innerHTML +='</ul>'
        if(result['isowner'] == '0')
        {
            let newDiv1 = document.createElement('div');
            newDiv1.id = 'dropSelf';
            newDiv1.innerHTML = '<input type="button" class="btn btn-outline-danger btn-sm" \
                onclick="msg.dropFromGM('
                + chatId + ', -1)" value="Покинуть беседу"></input> ';
            outputelem.append(newDiv1);
        }
    },

    /* Метод, удаляющий пользователя из переписки */
    async dropFromGM(chatId, userId)
    {
        let formData = new FormData();
        formData.append('typeRequest', 'dropFromGM');
        formData.append('chatId', chatId.toString());
        formData.append('userId', userId.toString());

        /* Выполняем POST-запрос */
        let response = await fetch('/messagesproc', {
            method: 'POST',
            body: formData
        });

        /* Получаем результат */
        let result = await response.json();
    },

    /* Метод, отправляющий сообщение */
    async send(form, toUserId)
    {
        /* Если поле сообщения пустое - игнорируем вызов */
        if(form.newMessage.value == '')
            return;

        /* Заполняем данные формы */
        form.typeRequest.value = 'send';
        /* Прячем сообщение, чтобы избежать паузы */
        form.newMessageTmp.value = form.newMessage.value;
        /* Сбрасываем поле сообщения */
        form.newMessage.value = '';
        let formData = new FormData(form);

        /* Выполняем POST-запрос */
        let response = await fetch('/messagesproc', {
            method: 'POST',
            body: formData
        });
    },

    /* Метод, загружающий предыдущие сообщения */
    async loadPrevMessages(form)
    {
        /* Заполняем данные формы */
        form.typeRequest.value = 'loadPrev';
        let formData = new FormData(form);
        formData.append('toUserId', msg.touid);
        formData.append('prevCount', msg.prevCount);

        /* Выполняем POST-запрос */
        let response = await fetch('/messagesproc', {
            method: 'POST',
            body: formData
        });

        /* Получаем результат */
        let result = await response.json();

        /* Ставим новые сообщения */
        msg.setPrevPM(result);
    },

    /* Метод, обновляющий сообщения */
    async update(form, toUserId)
    {
        /* Сохраняем идентификатор пользователя */
        msg.touid = toUserId;
        /* Заполняем данные формы */
        form.typeRequest.value = 'update';
        form.lastId.value = msg.lastId.toString();
        let formData = new FormData(form);

        /* Выполняем POST-запрос */
        let response = await fetch('/messagesproc', {
            method: 'POST',
            body: formData
        });

        /* Получаем результат */
        let result = await response.json();

        /* Запоминаем было уже обновление сообщений или нет */
        let started = (msg.lastId == 0);

        /* Ставим новые сообщения */
        msg.setNewPM(result);

        /* Если прибыли новые сообщения */
        if(msg.delta > 0 || started)
        {
            /* Прокручиваем прокрутку */
            let obj = document.getElementById('receiveDiv');
            obj.scrollTo(0, obj.scrollHeight);
        }
    },

    /* Метод, обновляющий статус переписок */
    async updateAllPM(form, isFull)
    {
        /* Заполняем данные формы */
        let formData = new FormData(form);
        formData.append('isFull', (isFull?'1':'0'));
        formData.append('count', msg.chatCount.toString());

        /* Выполняем POST-запрос */
        let response = await fetch('/messagesproc', {
            method: 'POST',
            body: formData
        });

        /* Получаем результат в JSON */
        let result = await response.json();

        /* Ставим новые сообщения */
        msg.setAllPM(result);
    }
};

document.addEventListener("DOMContentLoaded", () => {
    msg.loadByScroll(document.forms['sendForm']);
    msg.loadByScrollOfList(document.forms['sendForm']);
    msg.updateAllPM(document.forms['allPMInfo'], true)
    setInterval(
        () => {
            msg.updateAllPM(document.forms['allPMInfo'], false)
        },
        2000
    );
});
