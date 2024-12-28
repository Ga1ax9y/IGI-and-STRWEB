document.getElementById('bonusBtn').addEventListener('click', function() {

    document.getElementById('loader').style.display = 'flex';


    setTimeout(function() {

        const selectedEmployees = Array.from(document.querySelectorAll('input[name="selected_employees"]:checked'))
            .map(checkbox => checkbox.closest('tr').querySelector('td:nth-child(2)').innerText); // Берем значение из ячейки с ФИО


        const bonusMessage = selectedEmployees.length
            ? `Премированы следующие сотрудники: ${selectedEmployees.join(', ')}.`
            : 'Никто не выбран для премирования.';

        
        document.getElementById('loader').style.display = 'none';

        document.getElementById('bonusMessage').style.display = 'block';
        document.getElementById('bonusMessage').innerText = bonusMessage;
    }, 2500);
});
