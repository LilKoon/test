function setActive(menu) {
    document.querySelectorAll(".menu-item").forEach(m => m.classList.remove("active"));
    menu.classList.add("active");
}

/* PAGE TITLES */
const pageTitles = {
    home: "Trang chủ",
    account: "Quản lý tài khoản",
    salary: "Xem bảng lương",
    shift: "Ca làm việc",
    logout: "Đăng xuất"
};

/* LOAD PAGE FROM pages/*.html */
function loadPage(page) {
    document.getElementById("headerTitle").innerText = pageTitles[page] || "";

    fetch(`pages/${page}.html`)
        .then(res => res.text())
        .then(html => {
            document.getElementById("contentBox").innerHTML = html;

            if (page === "shift") initCalendar();
        });
}

window.onload = () => loadPage("home");

/* ==== ACCOUNT === */
function editAccount() {
    document.getElementById("viewMode").style.display = "none";
    document.getElementById("editMode").style.display = "block";
}

function cancelEdit() {
    document.getElementById("editMode").style.display = "none";
    document.getElementById("viewMode").style.display = "block";
}

function saveAccount() {
    alert("Đã lưu (DEMO)");
    cancelEdit();
}

/* ==== CALENDAR ==== */
let currentMonth = new Date().getMonth();
let currentYear = new Date().getFullYear();

const shiftData = {
    "2025-11-05": { shift: "Ca sáng", note: "Có mặt 7h", color:"#fef3c7", done:true },
    "2025-11-12": { shift: "Ca chiều", note:"Họp team 14h", color:"#d1fae5", done:false },
    "2025-11-19": { shift: "Ca tối", note:"Tăng ca", color:"#ede9fe", done:true }
};

function initCalendar() {
    generateCalendar();
}

function generateCalendar() {
    const tb = document.querySelector("#calendarTable tbody");
    const lbl = document.getElementById("calendarMonth");

    tb.innerHTML = "";
    lbl.innerText = `Tháng ${currentMonth + 1} / ${currentYear}`;

    const firstDay = new Date(currentYear, currentMonth, 1).getDay();
    const days = new Date(currentYear, currentMonth + 1, 0).getDate();

    let row = document.createElement("tr");
    for (let i=0; i<firstDay; i++) row.appendChild(document.createElement("td"));

    for (let d=1; d<=days; d++) {
        const key = `${currentYear}-${String(currentMonth+1).padStart(2,"0")}-${String(d).padStart(2,"0")}`;
        let cell = document.createElement("td");
        cell.style.height = "75px";
        cell.style.cursor = "pointer";
        let html = `<b>${d}</b><br>`;

        if (shiftData[key]) {
            let s = shiftData[key];
            html += `
            <div style="
                margin-top:6px;
                padding:4px;
                border-radius:6px;
                background:${s.color};
                font-size:12px;">
                ${s.shift} ${s.done?"✔":""}
            </div>`;
            cell.onclick = () => openPopup(key);
        }

        cell.innerHTML = html;
        row.appendChild(cell);

        if ((firstDay + d) % 7 === 0) {
            tb.appendChild(row);
            row = document.createElement("tr");
        }
    }
    tb.appendChild(row);
}

function prevMonth() {
    currentMonth--;
    if (currentMonth < 0) { currentMonth = 11; currentYear--; }
    generateCalendar();
}

function nextMonth() {
    currentMonth++;
    if (currentMonth > 11) { currentMonth = 0; currentYear++; }
    generateCalendar();
}

function openPopup(key) {
    const d = shiftData[key];
    document.getElementById("popupDate").innerText = key;
    document.getElementById("popupShift").innerText = d.shift;
    document.getElementById("popupNote").innerText = d.note;
    document.getElementById("shiftPopup").style.display = "flex";
}

function closePopup() {
    document.getElementById("shiftPopup").style.display = "none";
}
