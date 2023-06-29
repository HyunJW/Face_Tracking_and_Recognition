function init() {
  const currentDateElement = document.querySelector(".current-date");
  const daysTag = document.querySelector(".days");
  const prevNextIcon = document.querySelectorAll(".icons span");

  let currentDate = new Date();
  let currentYear = currentDate.getFullYear();
  let currentMonth = currentDate.getMonth();
  let currentDay = currentDate.getDate();
  let selectedDate = currentDate;
  let offset = currentDate.getTimezoneOffset() * 60000;
  const months = [
    "1월",
    "2월",
    "3월",
    "4월",
    "5월",
    "6월",
    "7월",
    "8월",
    "9월",
    "10월",
    "11월",
    "12월",
  ];

  const renderCalendar = () => {
    let firstDayOfMonth = new Date(currentYear, currentMonth, 1).getDay();
    let lastDateOfMonth = new Date(currentYear, currentMonth + 1, 0).getDate();
    let lastDayOfMonth = new Date(
      currentYear,
      currentMonth,
      lastDateOfMonth
    ).getDay();
    let lastDateOfLastMonth = new Date(currentYear, currentMonth, 0).getDate();
    let liTag = "";

    for (let i = firstDayOfMonth; i > 0; i--) {
      liTag += `<li class="inactive1">${lastDateOfLastMonth - i + 1}</li>`;
    }

    for (let i = 1; i <= lastDateOfMonth; i++) {
      let isToday =
        i === currentDay && currentMonth === currentDate.getMonth() && currentYear === currentDate.getFullYear()
          ? "current-day"
          : "";

      liTag += `<li class="${isToday}">${i}</li>`;
    }

    for (let i = lastDayOfMonth; i < 6; i++) {
      liTag += `<li class="inactive2">${i - lastDayOfMonth + 1}</li>`;

    }
    currentDateElement.innerText = `${currentYear} ${months[currentMonth]}`;

    daysTag.innerHTML = liTag;

    // 현재 날짜에 해당하는 요소에 항상 색을 표시
    const dayElements = daysTag.querySelectorAll("li");
    dayElements.forEach((dayElement) => {
      const day = parseInt(dayElement.textContent);
        if(dayElement.className=='inactive1'){
            nowMonth=currentMonth-1;
        }
        if(dayElement.className=='inactive2'){
            nowMonth=currentMonth+1;
        }

      if (day === currentDay && currentMonth === currentDate.getMonth()
      && currentYear === currentDate.getFullYear()
      && (dayElement.className!='inactive1' && dayElement.className!='inactive2')) {
        dayElement.classList.add("current-day");
      } else {
        dayElement.classList.remove("current-day");
      }

      dayElement.addEventListener("click", (event) => {
      const clickedDay = event.target;
      const clickedDayValue = parseInt(clickedDay.innerText);

        // 클릭된 날짜의 정보를 저장
        if(dayElement.className=='inactive1'){
            selectedDate = new Date(currentYear, currentMonth-1, day);
        }else if(dayElement.className=='inactive2'){
            selectedDate = new Date(currentYear, currentMonth+1, day);
        }else {
            selectedDate = new Date(currentYear, currentMonth, day);
        }
        selectedDate = new Date(selectedDate - offset);

        const selectedDay = daysTag.querySelector(".selected");
          if (selectedDay) {
            selectedDay.classList.remove("selected");
          }
          clickedDay.classList.add("selected");

        // AJAX를 사용하여 서버로 데이터 전송
        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/home_selected/', true);
        xhr.setRequestHeader('Content-Type', 'application/json');
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4 && xhr.status === 200) {
                document.getElementById("table1").innerHTML=xhr.responseText;
            }
        };
        const data = {
            selectedDate: selectedDate.toISOString()  // 선택된 날짜를 ISO 형식으로 변환하여 전송
        };
        xhr.send(JSON.stringify(data));


      });
    });
  };

  renderCalendar();

  prevNextIcon.forEach((icon) => {
    icon.addEventListener("click", () => {
      currentMonth = icon.id === "prev" ? currentMonth - 1 : currentMonth + 1;

      if (currentMonth < 0 || currentMonth > 11) {
        currentDate = new Date(currentYear, currentMonth);
        currentYear = currentDate.getFullYear();
        currentMonth = currentDate.getMonth();
      } else {
        currentDate = new Date();
      }
      renderCalendar();
    });
  });

  // 초기화 후 첫 화면에서 디폴트 테이블을 불러오도록 AJAX 요청
  const xhr = new XMLHttpRequest();
  xhr.open('POST', '/home_selected/', true);
  xhr.setRequestHeader('Content-Type', 'application/json');
  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4 && xhr.status === 200) {
      document.getElementById("table1").innerHTML = xhr.responseText;
    }
  };
  const data = {
    selectedDate: selectedDate.toISOString()  // 선택된 날짜를 ISO 형식으로 변환하여 전송
  };
  xhr.send(JSON.stringify(data));

}
