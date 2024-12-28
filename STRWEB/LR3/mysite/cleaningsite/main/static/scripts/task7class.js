(function() {
    // Летние и зимние месяцы
    const summerMonths = ['June', 'July', 'August', 'Июнь', 'Июль', 'Август'];
    const winterMonths = ['December', 'January', 'February', 'Декабрь', 'Январь', 'Февраль'];

    // Базовый класс для работы с датами
    class DateBase {
        constructor(month, day) {
            this.month = month;
            this.day = day;
        }

        // Геттеры и сеттеры
        get dayofmonth() {
            return this.day;
        }

        get monthofyear() {
            return this.month;
        }

        set dayofmonth(day) {
            if (day < 1 || day > 31) throw new Error('День должен быть от 1 до 31');
            this.day = day;
        }

        set monthofyear(month) {
            this.month = month;
        }

        // Полная дата
        get fullDate() {
            return `Месяц: ${this.month} День: ${this.day}`;
        }

        // Проверка на лето
        isSummer() {
            return summerMonths.includes(this.month);
        }

        // Проверка на зиму
        isWinter() {
            return winterMonths.includes(this.month);
        }
    }

    // Расширенный класс для работы с датами
    class ExtendedDate extends DateBase {
        constructor(month, day) {
            super(month, day);
        }

        // Статический метод для добавления даты через форму
        static addClassDate(resultId) {
            const month = document.getElementById('classMonth').value.trim();
            const day = parseInt(document.getElementById('classDay').value.trim());

            if (month && day) {
                const dateObj = new ExtendedDate(month, day);
                classDates.push(dateObj);
                ExtendedDate.displayDates(classDates, resultId);
                ExtendedDate.displayAllDates(classDates); // Выводим все введённые даты
                document.getElementById('classMonth').value = '';  // Очистка поля месяца
                document.getElementById('classDay').value = '';    // Очистка поля дня
            } else {
                alert("Введите корректные данные.");
            }
        }

        // Статический метод для отображения дат
        static displayDates(dates, resultId) {
            const summerDates = dates.filter(date => date.isSummer()).map(date => `${date.month} ${date.day}`);
            const winterDates = dates.filter(date => date.isWinter()).map(date => `${date.month} ${date.day}`);

            document.getElementById(resultId).innerHTML = `
                <h3>Летние даты</h3>
                <ul>${summerDates.map(date => `<li>${date}</li>`).join('')}</ul>
                <h3>Зимние даты</h3>
                <ul>${winterDates.map(date => `<li>${date}</li>`).join('')}</ul>
            `;
        }

        // Статический метод для вывода всех введённых дат
        static displayAllDates(dates) {
            const allDates = dates.map(date => `${date.month} ${date.day}`).join(', ');
            document.getElementById('allDates').innerHTML = `
                <h4>Все введённые даты:</h4>
                <p>${allDates}</p>
            `;
        }
    }

    // Массив для хранения дат
    const classDates = [];

    // Обработчик для добавления даты через форму
    window.addClassDate = function() {
        ExtendedDate.addClassDate('classResult');
    };

    // Обработка загруженного файла
    window.handleFileUpload = function(event, method) {
        const file = event.target.files[0];
        if (!file) return;

        const reader = new FileReader();
        reader.onload = function(e) {
            const lines = e.target.result.split('\n');
            const dates = [];

            lines.forEach(line => {
                const [month, day] = line.split(',');
                if (month && day) {
                    dates.push(new ExtendedDate(month.trim(), parseInt(day.trim())));
                }
            });

            saveDatesToFile(dates, method);
        };
        reader.readAsText(file);
    };

    // Сохранение летних и зимних дат в файлы
    function saveDatesToFile(dates, method) {
        const summerDates = dates.filter(date => date.isSummer()).map(date => `${date.month},${date.day}`).join('\n');
        const winterDates = dates.filter(date => date.isWinter()).map(date => `${date.month},${date.day}`).join('\n');

        downloadFile(summerDates, `${method}_summer.txt`);
        downloadFile(winterDates, `${method}_winter.txt`);
    }

    // Функция для скачивания файла
    function downloadFile(content, filename) {
        const blob = new Blob([content], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }

})();
