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
        /* Проверяем есть ли такая переписка */
        let newDiv = document.getElementById('user' + idx);
        if(newDiv === null)
        {
            /* Если нет, то создаем новую */
            newDiv = document.createElement('div');
            newDiv.id = 'user' + idx;
            output.append(newDiv);
        }
        /* Обновляем сообщение */
        newDiv.innerHTML = '<b><a href="messages?userid='
            + idx + '">' + login + ':</a></b> ' + message;
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
