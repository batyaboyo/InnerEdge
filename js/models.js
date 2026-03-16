/**
 * InnerEdge - Data Models
 * Defines the structure for journal entries and trades
 */

// Initialize namespace
window.InnerEdge = window.InnerEdge || {};

// Generate unique IDs
function generateId() {
    return Date.now().toString(36) + Math.random().toString(36).substr(2);
}

// Get today's date in YYYY-MM-DD format
function getTodayId() {
    return new Date().toISOString().split('T')[0];
}

// Format date for display
function formatDate(dateStr) {
    const date = new Date(dateStr + 'T00:00:00');
    return date.toLocaleDateString('en-US', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

// Format short date
function formatShortDate(dateStr) {
    const date = new Date(dateStr + 'T00:00:00');
    return date.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric'
    });
}

// Get day and month from date
function getDayMonth(dateStr) {
    const date = new Date(dateStr + 'T00:00:00');
    return {
        day: date.getDate(),
        month: date.toLocaleDateString('en-US', { month: 'short' })
    };
}

// Create a new Day Journal
function createDayJournal(dateId) {
    if (!dateId) {
        dateId = getTodayId();
    }
    return {
        id: dateId,
        createdAt: Date.now(),
        updatedAt: Date.now(),
        isLocked: false,
        marketAwareness: {
            session: '',
            condition: '',
            bias: '',
            expectation: ''
        },
        trades: [],
        reflection: {
            followedRules: null,
            brokenRule: '',
            biggestMistake: '',
            bestDecision: '',
            emotionalState: null,
            energyLevel: null,
            traderType: ''
        },
        lesson: {
            lessonOfDay: '',
            tomorrowAdjustment: ''
        }
    };
}

// Create a new Trade
function createTrade() {
    return {
        id: generateId(),
        asset: '',
        setupName: '',
        time: '',
        entry: null,
        stopLoss: null,
        takeProfit: null,
        planned: true,
        result: '',
        rValue: null,
        emotion: '',
        reason: ''
    };
}

// Calculate trade statistics for a journal
function calculateJournalStats(journal) {
    const trades = journal.trades || [];
    const stats = {
        totalTrades: trades.length,
        wins: 0,
        losses: 0,
        breakeven: 0,
        totalR: 0
    };

    trades.forEach(function (trade) {
        if (trade.result === 'Win') stats.wins++;
        else if (trade.result === 'Loss') stats.losses++;
        else if (trade.result === 'Break-even') stats.breakeven++;

        if (trade.rValue) {
            stats.totalR += parseFloat(trade.rValue);
        }
    });

    return stats;
}

// Check journal completion status
function getJournalCompletionStatus(journal) {
    var checks = {
        marketAwareness: !!(
            journal.marketAwareness.session &&
            journal.marketAwareness.condition &&
            journal.marketAwareness.bias
        ),
        trades: journal.trades.length > 0,
        reflection: !!(
            journal.reflection.followedRules !== null &&
            journal.reflection.emotionalState !== null &&
            journal.reflection.energyLevel !== null
        ),
        lesson: !!(
            journal.lesson.lessonOfDay &&
            journal.lesson.lessonOfDay.trim() &&
            journal.lesson.tomorrowAdjustment &&
            journal.lesson.tomorrowAdjustment.trim()
        )
    };

    checks.complete = checks.marketAwareness && checks.trades && checks.reflection && checks.lesson;

    return checks;
}

// Get week boundaries for a date
function getWeekBoundaries(date) {
    if (!date) date = new Date();
    var d = new Date(date);
    var day = d.getDay();
    var diff = d.getDate() - day + (day === 0 ? -6 : 1); // Adjust for Monday start

    var monday = new Date(d.setDate(diff));
    monday.setHours(0, 0, 0, 0);

    var sunday = new Date(monday);
    sunday.setDate(monday.getDate() + 6);
    sunday.setHours(23, 59, 59, 999);

    return {
        start: monday,
        end: sunday,
        startId: monday.toISOString().split('T')[0],
        endId: sunday.toISOString().split('T')[0]
    };
}

// Format week range for display
function formatWeekRange(start, end) {
    var startDate = new Date(start);
    var endDate = new Date(end);
    var startMonth = startDate.toLocaleDateString('en-US', { month: 'short' });
    var endMonth = endDate.toLocaleDateString('en-US', { month: 'short' });
    var year = endDate.getFullYear();

    if (startMonth === endMonth) {
        return startMonth + ' ' + startDate.getDate() + ' - ' + endDate.getDate() + ', ' + year;
    }
    return startMonth + ' ' + startDate.getDate() + ' - ' + endMonth + ' ' + endDate.getDate() + ', ' + year;
}

// Export functions for use in other modules
window.InnerEdge.models = {
    generateId: generateId,
    getTodayId: getTodayId,
    formatDate: formatDate,
    formatShortDate: formatShortDate,
    getDayMonth: getDayMonth,
    createDayJournal: createDayJournal,
    createTrade: createTrade,
    calculateJournalStats: calculateJournalStats,
    getJournalCompletionStatus: getJournalCompletionStatus,
    getWeekBoundaries: getWeekBoundaries,
    formatWeekRange: formatWeekRange
};
