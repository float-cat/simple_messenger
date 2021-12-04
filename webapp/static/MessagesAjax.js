msg = {
    lastId: 0,
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
        formData.append('login', 'Test'); // DBG
        formData.append('password', '1234'); // DBG

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
    }
};
