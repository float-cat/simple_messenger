msg = {
    lastId: 0,

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
        /* Добавляем данные для аутентификации */
        formData.append('login', 'Test');
        formData.append('password', '1234');

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

        /* Добавляем данные для аутентификации */
        formData.append('login', userInfo.login);
        formData.append('password', userInfo.password);

        /* Выполняем POST-запрос */
        let response = await fetch('/messagesproc', {
            method: 'POST',
            body: formData
        });

        /* Получаем результат */
        let result = await response.text();

        /* Получаем новое последнее сообщение */
        let sepPos = result.indexOf('|');
        let newLast = result.slice(0, sepPos);

        /* Устанавливаем последний айди */
        msg.lastId = parseInt(newLast);

        /* Получаем сообщения */
        let messages = result.slice(sepPos+1);

        /* Добавляем сообщения в переписку */
        document.forms['receiveForm'].messages.value += messages;
    },

    /* Метод, обновляющий статус переписок */
    async updateAllPM(form)
    {
        /* Заполняем данные формы */
        let formData = new FormData(form);

        /* Добавляем данные для аутентификации */
        formData.append('login', userInfo.login);
        formData.append('password', userInfo.password);

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
