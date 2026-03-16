/**
 * InnerEdge - Calendar Module
 * Handles calendar rendering and navigation
 */

// Initialize namespace
window.InnerEdge = window.InnerEdge || {};

var currentCalendarDate = new Date();

// Initialize calendar
function initCalendar() {
    renderCalendar();

    // Event listeners
    document.getElementById('prevMonth').addEventListener('click', function () {
        currentCalendarDate.setMonth(currentCalendarDate.getMonth() - 1);
        renderCalendar();
    });

    document.getElementById('nextMonth').addEventListener('click', function () {
        currentCalendarDate.setMonth(currentCalendarDate.getMonth() + 1);
        renderCalendar();
    });
}

// Render calendar grid
function renderCalendar() {
    var models = window.InnerEdge.models;
    var storage = window.InnerEdge.storage;
    var ui = window.InnerEdge.ui;

    var year = currentCalendarDate.getFullYear();
    var month = currentCalendarDate.getMonth();

    // Update header
    var monthNames = ['January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'];
    document.getElementById('currentMonth').textContent = monthNames[month] + ' ' + year;

    // Get journals for this month
    var monthJournals = storage.getJournalsByMonth(year, month);
    var journalDates = {};
    var lockedDates = {};
    for (var i = 0; i < monthJournals.length; i++) {
        journalDates[monthJournals[i].id] = true;
        if (monthJournals[i].isLocked) {
            lockedDates[monthJournals[i].id] = true;
        }
    }

    // Get calendar data
    var firstDay = new Date(year, month, 1);
    var lastDay = new Date(year, month + 1, 0);
    var startingDay = firstDay.getDay() || 7; // Convert Sunday (0) to 7 for Monday start
    var daysInMonth = lastDay.getDate();

    // Get today
    var todayId = models.getTodayId();

    // Build calendar HTML
    var html = '';

    // Day headers
    var dayNames = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
    for (var d = 0; d < dayNames.length; d++) {
        html += '<div class="calendar-header">' + dayNames[d] + '</div>';
    }

    // Previous month days
    var prevMonth = new Date(year, month, 0);
    var prevMonthDays = prevMonth.getDate();
    for (var p = startingDay - 1; p > 0; p--) {
        var pDay = prevMonthDays - p + 1;
        html += '<div class="calendar-day other-month">' + pDay + '</div>';
    }

    // Current month days
    for (var day = 1; day <= daysInMonth; day++) {
        var monthStr = String(month + 1).padStart(2, '0');
        var dayStr = String(day).padStart(2, '0');
        var dateId = year + '-' + monthStr + '-' + dayStr;
        var isToday = dateId === todayId;
        var hasJournal = journalDates[dateId];
        var isLocked = lockedDates[dateId];

        var classes = 'calendar-day';
        if (isToday) classes += ' today';
        if (hasJournal) classes += ' has-journal';
        if (isLocked) classes += ' locked';

        html += '<div class="' + classes + '" data-date="' + dateId + '">' + day + '</div>';
    }

    // Next month days
    var totalCells = Math.ceil((startingDay - 1 + daysInMonth) / 7) * 7;
    var remainingCells = totalCells - (startingDay - 1 + daysInMonth);
    for (var n = 1; n <= remainingCells; n++) {
        html += '<div class="calendar-day other-month">' + n + '</div>';
    }

    document.getElementById('calendarGrid').innerHTML = html;

    // Add click handlers
    var dayElements = document.querySelectorAll('.calendar-day:not(.other-month):not(.empty)');
    for (var j = 0; j < dayElements.length; j++) {
        (function (dayEl) {
            dayEl.addEventListener('click', function () {
                var clickedDateId = dayEl.dataset.date;
                if (clickedDateId) {
                    ui.openJournal(clickedDateId);
                }
            });
        })(dayElements[j]);
    }
}

// Navigate to specific month
function goToMonth(year, month) {
    currentCalendarDate = new Date(year, month, 1);
    renderCalendar();
}

// Navigate to today
function goToToday() {
    currentCalendarDate = new Date();
    renderCalendar();
}

// Export calendar functions
window.InnerEdge.calendar = {
    initCalendar: initCalendar,
    renderCalendar: renderCalendar,
    goToMonth: goToMonth,
    goToToday: goToToday
};
