msg = {
    lastId: 0,

    /* Метод добавляет новое сообщение в чат */
    async setPM(idx, login, message)
    {
        output = document.getElementById('receiveDiv');
        /* Проверяем есть ли такая переписка */
        /* Если нет, то создаем новую */
        newDiv = document.createElement('div');
        newDiv.id = 'message' + idx;
        output.append(newDiv);
        /* Обновляем сообщение */
        newDiv.innerHTML = '<b>' + login + ':</b> ' + message;
    },

    /* Метод обновляет или добавляет новую переписку */
    async setPMInfo(idx, login, message)
    {
        output = document.getElementById('messagesAllOutput');
        /* Проверяем есть ли такая переписка (div заменен на a) */
        let newA = document.getElementById('user' + idx);
        let url = (new URL(document.location)).searchParams;

        if(newA === null)
        {
            /* Если нет, то создаем новую */
            newA = document.createElement('a');
            newA.setAttribute("href", "messages1?userid=" + idx);
            if ( idx == url.get('userid'))
            {
            newA.className = 'list-group-item list-group-item-action active py-3 lh-tight';
            newA.setAttribute("aria-current", "true");}
            else { newA.className = 'list-group-item list-group-item-action py-3 lh-tight';
            }
            newA.id = 'user' + idx;
            output.append(newA);
        }
        /* Обновляем сообщение */
        newA.innerHTML ='<div class="d-flex w-100 align-items-center justify-content-between"><strong class="mb-1">'
        + login + '</strong><small>tut_time</small></div><div class="col-10 mb-1 small">'
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
                result[result['msgids'][idx]]['message']
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
                result[result['msgids'][idx]]['message']
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
