msg = {
    lastId: 0,

    /* Метод добавляет новое сообщение в чат */
    async setPM(idx, login, message, time, isOwner)
    {
        output = document.getElementById('receiveDiv');
        /* Проверяем есть ли такая переписка */
        /* Если нет, то создаем новую */
        newDiv = document.createElement('div');
        newDiv.id = 'message' + idx;
        output.append(newDiv);
        /* Обновляем сообщение */
        if (isOwner == 1){
            newDiv.innerHTML = '<div class="row justify-content-start">\
                <div class=" col col-11 col-sm-11 col-md-8\
                col-lg-6 alert alert-primary "\
                role="alert"><b>' + login + '&nbsp;</b> ' + time
                + '<p>' + message +'</p></div></div>';}
        else{
            newDiv.innerHTML = '<div class="row justify-content-end">\
                <div class=" col-11 col-sm-11 col-md-8\
                col-lg-6 col alert alert-secondary "\
                role="alert"><b>' + login + '&nbsp;</b> ' + time
                + '<p>' + message +'</p></div></div>';}


    },

    /* Метод обновляет или добавляет новую переписку */
    async setPMInfo(idx, login, message, time)
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
            newA.id = 'user' + idx;
            output.append(newA);
        }
        /* Обновляем сообщение */
        newA.innerHTML ='<div class="d-flex w-100\
            align-items-center justify-content-between"><strong class="mb-1">'
            + login + '</strong><small>' + time
            + '</small></div><div class="col-10 mb-1 small">'
            + message + '</div>';
    },

    async setNewPM(result)
    {
        msg.lastId = parseInt(result['lastid']);
        for(let idx = 0; idx < result['count']; idx++)
        {
            msg.setPM(
                result['msgids'][idx],
                result[result['msgids'][idx]]['login'],
                result[result['msgids'][idx]]['message'],
                result[result['msgids'][idx]]['time'],
                result[result['msgids'][idx]]['isOwner']
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
                result[result['msgids'][idx]]['time']
            );
        }
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

    /* Метод, обновляющий сообщения */
    async update(form, toUserId)
    {
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

        /* Ставим новые сообщения */
        msg.setNewPM(result);
    },

    /* Метод, обновляющий статус переписок */
    async updateAllPM(form)
    {
        /* Заполняем данные формы */
        let formData = new FormData(form);

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
