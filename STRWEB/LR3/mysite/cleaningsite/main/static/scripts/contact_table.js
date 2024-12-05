const table = document.getElementById("employeeTable");
const searchInput = document.getElementById("searchInput");
const searchBtn = document.getElementById("searchBtn");
const tbody = document.getElementById("employeeTbody");
const employeeDetails = document.getElementById("employeeDetails");

let currentPage = 1;
const rowsPerPage = 3;
let filteredRows = [];  // Массив отфильтрованных строк
let allRows = [];       // Все строки таблицы
let currentSortColumn = null;
let currentSortDirection = 1;  // Направление сортировки (1 - по возрастанию, -1 - по убыванию)

// Сортировка таблицы по столбцам
table.onclick = function (e) {
    if (e.target.tagName !== 'TH') return;
    let th = e.target;
    let columnIndex = th.cellIndex;
    let type = th.dataset.type;

    if (currentSortColumn === columnIndex) {
        currentSortDirection *= -1;
    } else {
        currentSortColumn = columnIndex;
        currentSortDirection = 1;  // По умолчанию сортируем по возрастанию
    }

    sortTable(columnIndex, type, currentSortDirection);
    updateSortIndicators(th, currentSortDirection);
    renderTable();
};

// Функция для сортировки таблицы
function sortTable(colNum, type, direction) {
    let compare;
    switch (type) {
        case 'number':
            compare = function (rowA, rowB) {
                return direction * (rowA.cells[colNum].innerHTML - rowB.cells[colNum].innerHTML);
            };
            break;
        case 'string':
            compare = function (rowA, rowB) {
                return direction * (rowA.cells[colNum].innerHTML.localeCompare(rowB.cells[colNum].innerHTML));
            };
            break;
    }

    filteredRows.sort(compare);
}

// Обновление индикаторов сортировки
function updateSortIndicators(th, direction) {
    Array.from(table.querySelectorAll("th .sort-indicator")).forEach(indicator => {
        indicator.textContent = '';
    });

    const sortIndicator = th.querySelector(".sort-indicator");
    sortIndicator.textContent = direction === 1 ? '▲' : '▼';
}

// Фильтрация
searchBtn.addEventListener('click', () => {

    document.getElementById('loader').style.display = 'flex';

    const searchQuery = searchInput.value.toLowerCase();

    // Если строка поиска пуста, показываем все строки
    if (searchQuery === "") {
        filteredRows = allRows;
        currentPage = 1;
    } else {

        filteredRows = allRows.filter(row => {
            const fullName = row.cells[1].textContent.toLowerCase();
            const description = row.cells[3].textContent.toLowerCase();
            const workPhone = row.cells[4].textContent.toLowerCase();
            const workEmail = row.cells[5].textContent.toLowerCase();

            return fullName.includes(searchQuery) || description.includes(searchQuery) || workPhone.includes(searchQuery) || workEmail.includes(searchQuery);
        });
    }

    setTimeout(function() {
        renderTable();
        updatePagination();


        document.getElementById('loader').style.display = 'none';
    }, 2500);
});

// Обработчик клика на строку таблицы для отображения данных
tbody.addEventListener('click', function (e) {
    const row = e.target.closest('tr');

    if (!row) return;

    const fullName = row.cells[1].textContent;
    const photo = row.cells[2].querySelector('img') ? row.cells[2].querySelector('img').src : 'Нет фото';
    const description = row.cells[3].textContent;
    const phone = row.cells[4].textContent;
    const email = row.cells[5].textContent;


    document.getElementById('detailFullName').textContent = fullName;
    document.getElementById('detailPhoto').textContent = photo;
    document.getElementById('detailDescription').textContent = description;
    document.getElementById('detailPhone').textContent = phone;
    document.getElementById('detailEmail').textContent = email;


    employeeDetails.style.display = 'block';
});


function renderTable() {
    const start = (currentPage - 1) * rowsPerPage;
    const end = start + rowsPerPage;


    tbody.innerHTML = '';


    const rowsToRender = filteredRows.slice(start, end);
    rowsToRender.forEach(row => {
        tbody.appendChild(row);
    });

    updatePagination();
}

// Функция для смены страницы
function changePage(page) {
    const totalPages = Math.ceil(filteredRows.length / rowsPerPage);
    if (page < 1 || page > totalPages) return;
    currentPage = page;
    renderTable();
}


function updatePagination() {
    const totalPages = Math.ceil(filteredRows.length / rowsPerPage);
    document.getElementById('pageInfo').textContent = `Страница ${currentPage} из ${totalPages}`;


    document.getElementById('prevPage').disabled = currentPage === 1;
    document.getElementById('nextPage').disabled = currentPage === totalPages;
}

// Инициализация (при загрузке таблицы)
window.onload = () => {

    allRows = Array.from(tbody.querySelectorAll('tr'));
    filteredRows = allRows;
    renderTable();
    updatePagination();
};
