document.getElementById('get-imageNASA').addEventListener('click', async function() {

    const lat = document.getElementById('lat').value.trim();
    const lon = document.getElementById('lon').value.trim();
    const dim = document.getElementById('dim').value.trim();
    const date = document.getElementById('date').value.trim();
    const apiKey = 'JIeRHpyJf2QGtwttXdMrexyno2CPbhKvhZNY3fas';

    if (!lat || !lon || !date) {
        document.getElementById('image-result').innerHTML = '<p>Введите координаты (широту и долготу) и дату.</p>';
        return;
    }

    // Формируем URL для запроса
    let requestUrl = `https://api.nasa.gov/planetary/earth/imagery?lon=${lon}&lat=${lat}&date=${date}&dim=${dim}&api_key=${apiKey}`;

    // Отображаем URL запроса
    document.getElementById('image-result').innerHTML = `
        <h3>Идет запрос...</h3>
    `;

    try {
        const response = await fetch(requestUrl);

        if (!response.ok) {
            throw new Error(`Ошибка запроса: ${response.status} - ${response.statusText}`);
        }

        const data = await response;

        if (data.url) {
            document.getElementById('image-result').innerHTML = `
                <h3>Изображение</h3>
                <img src="${data.url}" alt="NASA Earth Image" width="600">
            `;
        } else {
            document.getElementById('image-result').innerHTML = `<p>Изображение не найдено для указанных координат и даты.</p>`;
        }
    } catch (error) {
        document.getElementById('image-result').innerHTML = `<p>Ошибка: ${error.message}</p>`;
    }
});
