(function() {
    const summerMonths = ['June', 'July', 'August', 'Июнь', 'Июль', 'Август'];
    const winterMonths = ['December', 'January', 'February', 'Декабрь', 'Январь', 'Февраль'];


    function DateBase(month, day) {
        this.month = month;
        this.day = day;
    }

    // Геттеры и сеттеры
    DateBase.prototype.getDayOfMonth = function() {
        return this.day;
    };

    DateBase.prototype.getMonthOfYear = function() {
        return this.month;
    };

    DateBase.prototype.setDayOfMonth = function(day) {
        if (day < 1 || day > 31) throw new Error('День должен быть от 1 до 31');
        this.day = day;
    };

    DateBase.prototype.setMonthOfYear = function(month) {
        this.month = month;
    };

    // Метод для вывода полной даты
    DateBase.prototype.getFullDate = function() {
        return `Месяц: ${this.month} День: ${this.day}`;
    };

    // Метод для проверки летних месяцев
    DateBase.prototype.isSummer = function() {
        return summerMonths.includes(this.month);
    };

    // Метод для проверки зимних месяцев
    DateBase.prototype.isWinter = function() {
        return winterMonths.includes(this.month);
    };


    function ExtendedDate(month, day) {
        DateBase.call(this, month, day);
    }

    // Настройка прототипа для наследования
    ExtendedDate.prototype = Object.create(DateBase.prototype);
    ExtendedDate.prototype.constructor = ExtendedDate;

    // Статический метод для добавления даты через форму
    ExtendedDate.addProtoDate = function(resultId) {
        const month = document.getElementById('protoMonth').value.trim();
        const day = parseInt(document.getElementById('protoDay').value.trim());

        if (month && day) {
            const dateObj = new ExtendedDate(month, day);
            protoDates.push(dateObj);
            ExtendedDate.displayDates(protoDates, resultId);
            ExtendedDate.displayAllDates(protoDates);
            document.getElementById('protoMonth').value = '';
            document.getElementById('protoDay').value = '';
        } else {
            alert("Введите корректные данные.");
        }
    };

    // Статический метод для отображения дат
    ExtendedDate.displayDates = function(dates, resultId) {
        const summerDates = dates.filter(date => date.isSummer()).map(date => `${date.month} ${date.day}`);
        const winterDates = dates.filter(date => date.isWinter()).map(date => `${date.month} ${date.day}`);

        document.getElementById(resultId).innerHTML = `
            <h3>Летние даты</h3>
            <ul>${summerDates.map(date => `<li>${date}</li>`).join('')}</ul>
            <h3>Зимние даты</h3>
            <ul>${winterDates.map(date => `<li>${date}</li>`).join('')}</ul>
        `;
    };
    // Статический метод для вывода всех введённых дат
    ExtendedDate.displayAllDates = function(dates) {
        const allDates = dates.map(date => `${date.month} ${date.day}`).join(', ');
        document.getElementById('allDates2').innerHTML = `
            <h4>Все введённые даты:</h4>
            <p>${allDates}</p>
        `;
    };

    const protoDates = [];


    window.addProtoDate = function() {
        ExtendedDate.addProtoDate('protoResult');
    };


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
