/**
 * InnerEdge - LocalStorage Manager
 * Handles all data persistence operations
 */

// Initialize namespace
window.InnerEdge = window.InnerEdge || {};

var STORAGE_KEY = 'inneredge_journals';
var SETTINGS_KEY = 'inneredge_settings';

// Get all journals from storage
function getAllJournals() {
    try {
        var data = localStorage.getItem(STORAGE_KEY);
        return data ? JSON.parse(data) : {};
    } catch (error) {
        console.error('Error reading journals:', error);
        return {};
    }
}

// Save all journals to storage
function saveAllJournals(journals) {
    try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(journals));
        return true;
    } catch (error) {
        console.error('Error saving journals:', error);
        return false;
    }
}

// Get a specific journal by date ID
function getJournal(dateId) {
    var journals = getAllJournals();
    return journals[dateId] || null;
}

// Save or update a journal
function saveJournal(journal) {
    var journals = getAllJournals();
    journal.updatedAt = Date.now();
    journals[journal.id] = journal;
    return saveAllJournals(journals);
}

// Delete a journal
function deleteJournal(dateId) {
    var journals = getAllJournals();
    delete journals[dateId];
    return saveAllJournals(journals);
}

// Get journals for a specific week
function getJournalsByWeek(startDate, endDate) {
    var journals = getAllJournals();
    var weekJournals = [];

    var start = new Date(startDate);
    var end = new Date(endDate);

    Object.keys(journals).forEach(function (key) {
        var journal = journals[key];
        var journalDate = new Date(journal.id + 'T00:00:00');
        if (journalDate >= start && journalDate <= end) {
            weekJournals.push(journal);
        }
    });

    return weekJournals.sort(function (a, b) {
        return new Date(a.id) - new Date(b.id);
    });
}

// Get journals for a specific month
function getJournalsByMonth(year, month) {
    var journals = getAllJournals();
    var monthJournals = [];

    Object.keys(journals).forEach(function (key) {
        var journal = journals[key];
        var journalDate = new Date(journal.id + 'T00:00:00');
        if (journalDate.getFullYear() === year && journalDate.getMonth() === month) {
            monthJournals.push(journal);
        }
    });

    return monthJournals.sort(function (a, b) {
        return new Date(a.id) - new Date(b.id);
    });
}

// Get recent journals (last N entries)
function getRecentJournals(limit) {
    if (!limit) limit = 5;
    var journals = getAllJournals();
    var journalList = Object.keys(journals).map(function (key) {
        return journals[key];
    });
    return journalList
        .sort(function (a, b) {
            return new Date(b.id) - new Date(a.id);
        })
        .slice(0, limit);
}

// Check if a journal exists for a date
function hasJournal(dateId) {
    var journals = getAllJournals();
    return !!journals[dateId];
}

// Get app settings
function getSettings() {
    try {
        var data = localStorage.getItem(SETTINGS_KEY);
        return data ? JSON.parse(data) : { theme: 'light' };
    } catch (error) {
        return { theme: 'light' };
    }
}

// Save app settings
function saveSettings(settings) {
    try {
        localStorage.setItem(SETTINGS_KEY, JSON.stringify(settings));
        return true;
    } catch (error) {
        console.error('Error saving settings:', error);
        return false;
    }
}

// Get theme preference
function getTheme() {
    var settings = getSettings();
    return settings.theme || 'light';
}

// Set theme preference
function setTheme(theme) {
    var settings = getSettings();
    settings.theme = theme;
    saveSettings(settings);
    document.documentElement.setAttribute('data-theme', theme);
}

// Export storage functions
window.InnerEdge.storage = {
    getAllJournals: getAllJournals,
    getJournal: getJournal,
    saveJournal: saveJournal,
    deleteJournal: deleteJournal,
    getJournalsByWeek: getJournalsByWeek,
    getJournalsByMonth: getJournalsByMonth,
    getRecentJournals: getRecentJournals,
    hasJournal: hasJournal,
    getSettings: getSettings,
    saveSettings: saveSettings,
    getTheme: getTheme,
    setTheme: setTheme
};
