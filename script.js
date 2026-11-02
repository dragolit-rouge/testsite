document.addEventListener('DOMContentLoaded', () => {
    const enterButton = document.querySelector('.enter-button');
    const modalWindow = document.getElementById('modal-window');
    const closeModal = document.getElementById('close-modal');
    const enterInput = document.getElementById('enter-id');

    enterButton.addEventListener('click', () => {
        modalWindow.style.display = 'flex';
        enterInput.focus();
    });

    closeModal.addEventListener('click', () => {
        modalWindow.style.display = 'none';
        enterInput.value = '';
    });

    async function checkEnterId() {
        const idValue = enterInput.value.trim();

        if (idValue === '') {
            return;
        }

        try {
            const response = await fetch('https://back.smarthive.digital/api/check-enter', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ id: idValue })
            });

            const data = await response.json();

            if (data.status === 'success') {
                alert('Успешно! Открываем улей.');
                 localStorage.setItem('currentHive', JSON.stringify(data.hive));

                window.location.href = 'workspace.html';
            } else {
                alert('Пасека не найдена.');
            }

        } catch (error) {
            console.error('Ошибка:', error);
            alert('Нет связи с базой данных.');
        }
    }

    enterInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            checkEnterId();
        }
    });
});
