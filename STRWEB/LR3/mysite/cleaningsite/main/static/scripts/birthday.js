
    window.onload = function() {
        document.getElementById("birthModal").style.display = "block";
    }

    function closeModal() {
        document.getElementById("birthModal").style.display = "none";
    }

    function checkAge() {
        const birthDateInput = document.getElementById("birthDate").value;
        const messageDiv = document.getElementById("message");
        messageDiv.innerHTML = "";

        if (!birthDateInput) {
            alert("Пожалуйста, введите дату рождения.");
            return;
        }

        const birthDate = new Date(birthDateInput);
        const today = new Date();

        let age = today.getFullYear() - birthDate.getFullYear();
        const monthDiff = today.getMonth() - birthDate.getMonth();
        const dayDiff = today.getDate() - birthDate.getDate();

        if (monthDiff < 0 || (monthDiff === 0 && dayDiff < 0)) {
            age--;
        }
        if (age < 0) {
            messageDiv.innerText = "Дата не является корректной! Повторите попытку ввода.";
            return;
        }

        const daysOfWeek = ["воскресенье", "понедельник", "вторник", "среда", "четверг", "пятница", "суббота"];
        const dayOfWeek = daysOfWeek[birthDate.getDay()];

        if (age >= 18) {
            messageDiv.innerHTML = `Вам <strong>${age}</strong> лет.<br>Ваш день рождения - <strong>${dayOfWeek}</strong>.<br>Добро пожаловать!`;
        } else {
            alert(`Вам ${age} лет. Для использования этого сайта необходимо разрешение родителей. Нажимая 'ОК' вы даете разрешение на использование сайта`);
            messageDiv.innerHTML = `Вам <strong>${age}</strong> лет.<br>Ваш день рождения - <strong>${dayOfWeek}</strong>.<br>Пожалуйста, предоставьте разрешение родителей.`;
        }
    }
