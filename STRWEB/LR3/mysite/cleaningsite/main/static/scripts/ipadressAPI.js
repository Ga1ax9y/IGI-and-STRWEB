    // Функция для выполнения запроса и отображения результата
    async function getGeoData() {
        const ip = document.getElementById('ip-input').value.trim();

        if (!ip) {
            document.getElementById('result').innerHTML = '<p>Please enter an IP address.</p>';
            return;
        }

        // Формируем URL для запроса
        const requestUrl = `http://ip-api.com/json/${ip}`;

        try {
            // Делаем запрос
            const response = await fetch(requestUrl);

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            // Преобразуем ответ в формат JSON
            const data = await response.json();

            // Проверка, если данные вернулись с ошибкой
            if (data.status === 'fail') {
                document.getElementById('result').innerHTML = `<p>Error: ${data.message}</p>`;
                return;
            }

            // Отображаем результат
            document.getElementById('result').innerHTML = `
                <h2>IP Information:</h2>
                <p><strong>IP:</strong> ${data.query}</p>
                <p><strong>Country:</strong> ${data.country}</p>
                <p><strong>Region:</strong> ${data.regionName}</p>
                <p><strong>City:</strong> ${data.city}</p>
                <p><strong>Zip:</strong> ${data.zip}</p>
                <p><strong>Timezone:</strong> ${data.timezone}</p>
            `;
        } catch (error) {
            // Обработка ошибок
            document.getElementById('result').innerHTML = `<p>Error: ${error.message}</p>`;
        }
    }

    // Добавляем обработчик на кнопку
    document.getElementById('get-location').addEventListener('click', getGeoData);
