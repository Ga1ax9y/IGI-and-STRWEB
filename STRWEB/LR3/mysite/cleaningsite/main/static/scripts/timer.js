
  const countdownDuration = 3600000;
  const countdownDisplay = document.getElementById("time-remaining");
  const resetButton = document.getElementById("reset-timer");

  let timer;

  function startCountdown() {
      let startTime = localStorage.getItem("countdownStartTime");

      // Если стартовое время не сохранено, установим текущее время как стартовое
      if (!startTime) {
          startTime = Date.now();
          localStorage.setItem("countdownStartTime", startTime);
      }

      const endTime = parseInt(startTime) + countdownDuration;

      // Функция для обновления оставшегося времени
      function updateCountdown() {
          const now = Date.now();
          const remainingTime = endTime - now;


          if (remainingTime <= 0) {
              countdownDisplay.textContent = "Обратный отсчёт завершен";
              clearInterval(timer);
              localStorage.removeItem("countdownStartTime"); // Удалить сохраненное время
          } else {
              const hours = Math.floor((remainingTime / (1000 * 60 * 60)) % 24);
              const minutes = Math.floor((remainingTime / (1000 * 60)) % 60);
              const seconds = Math.floor((remainingTime / 1000) % 60);
              countdownDisplay.textContent = `${hours}ч ${minutes}м ${seconds}с`;
          }
      }

      // Очищаем предыдущий таймер перед запуском нового
      clearInterval(timer);
      updateCountdown();
      timer = setInterval(updateCountdown, 1000);
  }

  // Функция для перезапуска таймера
  function resetCountdown() {

      localStorage.removeItem("countdownStartTime");

      
      startCountdown();
  }


  resetButton.addEventListener("click", resetCountdown);


  startCountdown();
