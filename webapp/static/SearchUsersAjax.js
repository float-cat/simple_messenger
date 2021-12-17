searchUsers = {
    /* Метод добавляет в результ поиска пользователя */
    async setUser(idx, login)
    {
        let output = document.getElementById('outputUsers');
        let newLi = document.createElement('li');
        newLi.className = "list-group-item"
        newLi.id = 'uid' + idx;
        output.append(newLi);
        /* Создаем ссылку на переписку с пользователем */
        newLi.innerHTML = '<a href="?userid=' + idx + '">'
            + login + '</a>';        
        let url = (new URL(document.location)).searchParams;
        if (url.get('chatid'))
            newLi.innerHTML = ' <input type="button" value="+" \
                onclick="searchUsers.append(this.parentNode, '
                + url.get('chatid') + ')"></input>' + newLi.innerHTML;
    },

    async setFindUsers(result)
    {
        output = document.getElementById('outputUsers');
        output.innerHTML = '';
        for(let idx = 0; idx < result['count']; idx++)
        {
            searchUsers.setUser(
                result['msgids'][idx],
                result[result['msgids'][idx]]
            );
        }
    },

    /* Метод, обновляющий результаты поиска */
    async search(form)
    {
        /* Заполняем данные формы */
        let formData = new FormData(form);
        formData.append('typeRequest', 'search');

        /* Выполняем POST-запрос */
        let response = await fetch('/searchusersproc', {
            method: 'POST',
            body: formData
        });

        /* Получаем результат в JSON */
        let result = await response.json();

        /* Выводим найденых пользователей */
        searchUsers.setFindUsers(result);
    },

    /* Метод, добавляющий пользователя к переписке */
    async append(elem, chatId)
    {
        /* Заполняем данные формы */
        let formData = new FormData(elem.form);
        formData.append('typeRequest', 'append');
        formData.append('userId', elem.id);
        formData.append('chatId', chatId);

        /* Выполняем POST-запрос */
        let response = await fetch('/searchusersproc', {
            method: 'POST',
            body: formData
        });

        /* Получаем результат в JSON */
        let result = await response.json();
    }
};
