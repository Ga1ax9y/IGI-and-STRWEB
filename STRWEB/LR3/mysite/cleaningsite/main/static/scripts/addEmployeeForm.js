
    document.getElementById('addEmployeeBtn').addEventListener('click', function() {
        document.getElementById('employeeForm').style.display = 'block';
    });
    document.getElementById('cancelBtn').addEventListener('click', function() {
        document.getElementById('employeeForm').style.display = 'none';
    });

    // Функция для проверки почты
    function validateEmail(email) {
        const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
        return emailPattern.test(email);
    }

    // Функция для проверки телефона
    function validatePhone(phone) {
        const phonePattern = /^(?:\+375\s?\(?\d{2}\)?|\(?8\s?\(?\d{3}\)?)\)?[\s\-]?\d{3}([\s\-]?\d{2}[\s\-]?\d{2}|\d{7})$/;
        return phonePattern.test(phone);
    }


    function validateField(field, validateFn) {
        const value = field.value.trim();
        if (!validateFn(value)) {
            field.style.borderColor = 'red';
            field.style.backgroundColor = '#f8d7da';
        } else {
            field.style.borderColor = '';
            field.style.backgroundColor = '';
        }
    }


    document.getElementById('id_work_email').addEventListener('input', function() {
        validateField(this, validateEmail);
    });

    document.getElementById('id_work_phone').addEventListener('input', function() {
        validateField(this, validatePhone);
    });


    function toggleSubmitButton() {
        const emailValid = validateEmail(document.getElementById('id_work_email').value);
        const phoneValid = validatePhone(document.getElementById('id_work_phone').value);


        document.getElementById('employeeFormSubmit').disabled = !(emailValid && phoneValid);
    }

    // Обновляем статус кнопки отправки при вводе в любое из полей
    document.getElementById('id_work_email').addEventListener('input', toggleSubmitButton);
    document.getElementById('id_work_phone').addEventListener('input', toggleSubmitButton);

    
    toggleSubmitButton();
