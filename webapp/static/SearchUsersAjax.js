searchUsers = {
    /* Метод добавляет в результ поиска пользователя */
    async setUser(idx, login)
    {
        output = document.getElementById('outputUsers');
        newDiv = document.createElement('div');
        newDiv.id = 'message' + idx;
        output.append(newDiv);
        /* Создаем ссылку на переписку с пользователем */
        newDiv.innerHTML = '<a href="?userid=' + idx + '"><b>' + login + '</b></a>';
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

        /* Выполняем POST-запрос */
        let response = await fetch('/searchusersproc', {
            method: 'POST',
            body: formData
        });

        /* Получаем результат в JSON */
        let result = await response.json();

        /* Выводим найденых пользователей */
        searchUsers.setFindUsers(result);
    }
};
