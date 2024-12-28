document.getElementById('get-image').addEventListener('click', async function() {
    // Формируем URL для запроса
    const apiKey = 'JIeRHpyJf2QGtwttXdMrexyno2CPbhKvhZNY3fas'; // Ваш API-ключ
    let requestUrl = `https://api.nasa.gov/planetary/apod?api_key=${apiKey}`;

    // Отображаем URL запроса
    document.getElementById('image-result').innerHTML = `
        <h3>Идет запрос</h3>
    `;

    try {
        // Выполняем запрос к API
        const response = await fetch(requestUrl);

        // Проверяем успешность запроса
        if (!response.ok) {
            throw new Error('Ошибка запроса');
        }

        // Получаем данные
        const data = await response.json();

        // Если URL изображения получен успешно, отображаем изображение
        if (data.url) {
            document.getElementById('image-result').innerHTML = `
                <h3>Изображение</h3>
                <img src="${data.url}" alt="NASA Image" width="600">
            `;
        } else {
            document.getElementById('image-result').innerHTML = `<p>Изображение не найдено.</p>`;
        }
    } catch (error) {
        document.getElementById('image-result').innerHTML = `<p>Ошибка: ${error.message}</p>`;
    }
});
