document.addEventListener('DOMContentLoaded', () => {
    
    // Получение JSON-строки из localStorage по ключу авторизации
    const rawData = localStorage.getItem('currentHive');

    // Проверка наличия сессии. При отсутствии данных — редирект на корневой индекс
    if (!rawData) {
        window.location.href = 'index.html';
        return;
    }

    // Десериализация JSON-строки в массив объектов данных
    const hiveHistory = JSON.parse(rawData);

    // Соответствие системных идентификаторов вкладок отображаемым заголовкам h2
    const tabTitles = {
        hum: "Показатели влажности",
        temp: "Показатели температуры",
        sounds: "Анализ звука в улье",
        analysis: "Общий анализ"
    };

    // Функция фильтрации массива данных и рендеринга строк таблицы
    function renderTableData(activeTab) {
        const tableBody = document.getElementById('dynamic-table-body');
        const tableTitle = document.getElementById('table-title');
        
        // Обновление текстового контента заголовка h2
        if (tabTitles[activeTab]) {
            tableTitle.innerText = tabTitles[activeTab];
        }

        // Очистка содержимого контейнера tbody перед перерисовкой
        tableBody.innerHTML = '';

        // Приведение структуры данных к единому массиву (обработка одиночных объектов)
        const dataArray = Array.isArray(hiveHistory) ? hiveHistory : [hiveHistory];

        // Фильтрация элементов массива по соответствию поля type активному табу
        const filteredData = dataArray.filter(item => item.type === activeTab);

        // Цикл генерации HTML-структуры строк таблицы на основе отфильтрованных данных
        filteredData.forEach(item => {
            const row = document.createElement('tr');
            
            // Наполнение 4 фиксированных колонок: Улей, Значение, Единица измерения, Время
            row.innerHTML = `
                <td>${item.hive_id ?? '—'}</td>
                <td><strong>${item.value ?? '—'}</strong></td>
                <td>${item.unit ?? '—'}</td>
                <td>${item.time ?? '—'}</td>
            `;
            
            // Добавление сформированного узла tr в DOM-дерево таблицы
            tableBody.appendChild(row);
        });
    }

    // Инициализация слушателей событий клика для элементов навигации панелей
    document.querySelectorAll('.tab-btn').forEach(button => {
        button.addEventListener('click', () => {
            // Переключение класса активности на целевую кнопку
            document.querySelector('.tab-btn.active').classList.remove('active');
            button.classList.add('active');

            // Чтение значения дата-атрибута data-tab нажатого элемента
            const selectedTab = button.getAttribute('data-tab');
            
            // Вызов функции рендеринга для выбранного сегмента данных
            renderTableData(selectedTab);
        });
    });

    // Первичный запуск рендеринга для дефолтной вкладки 'humidity' при загрузке DOM
    renderTableData('hum');
});
