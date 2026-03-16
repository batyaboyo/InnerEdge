/**
 * InnerEdge - Main Application Controller
 * Initializes all modules and handles global events
 */

document.addEventListener('DOMContentLoaded', function () {
    var models = window.InnerEdge.models;
    var storage = window.InnerEdge.storage;
    var ui = window.InnerEdge.ui;
    var calendar = window.InnerEdge.calendar;
    var summary = window.InnerEdge.summary;

    // Initialize UI elements
    ui.initElements();

    // Initialize theme
    var savedTheme = storage.getTheme();
    document.documentElement.setAttribute('data-theme', savedTheme);

    // Initialize modules
    calendar.initCalendar();
    summary.initSummary();

    // Initial render
    ui.renderDashboard();

    // ========================
    // Navigation Events
    // ========================

    var navBtns = document.querySelectorAll('.nav-btn');
    for (var i = 0; i < navBtns.length; i++) {
        (function (btn) {
            btn.addEventListener('click', function () {
                var view = btn.dataset.view;
                ui.showView(view);

                if (view === 'dashboard') {
                    ui.renderDashboard();
                    calendar.renderCalendar();
                } else if (view === 'journal') {
                    var todayId = models.getTodayId();
                    ui.openJournal(todayId);
                } else if (view === 'summary') {
                    summary.renderSummary();
                }
            });
        })(navBtns[i]);
    }

    // ========================
    // Dashboard Events
    // ========================

    document.getElementById('createTodayBtn').addEventListener('click', function () {
        var todayId = models.getTodayId();
        ui.openJournal(todayId);
    });

    // ========================
    // Journal Events
    // ========================

    // Back to dashboard
    document.getElementById('backToDashboard').addEventListener('click', function () {
        ui.showView('dashboard');
        ui.renderDashboard();
        calendar.renderCalendar();
    });

    // Section toggles
    var sectionHeaders = document.querySelectorAll('.section-header');
    for (var s = 0; s < sectionHeaders.length; s++) {
        (function (header) {
            header.addEventListener('click', function (e) {
                if (!e.target.closest('.section-toggle')) {
                    var section = header.closest('.journal-section');
                    ui.toggleSection(section);
                }
            });
        })(sectionHeaders[s]);
    }

    var sectionToggles = document.querySelectorAll('.section-toggle');
    for (var t = 0; t < sectionToggles.length; t++) {
        (function (toggle) {
            toggle.addEventListener('click', function () {
                var section = toggle.closest('.journal-section');
                ui.toggleSection(section);
            });
        })(sectionToggles[t]);
    }

    // Market Awareness auto-save
    var marketFields = ['session', 'marketCondition', 'bias'];
    var fieldMap = { session: 'session', marketCondition: 'condition', bias: 'bias' };
    for (var m = 0; m < marketFields.length; m++) {
        (function (id) {
            document.getElementById(id).addEventListener('change', function (e) {
                ui.saveJournalField('marketAwareness', fieldMap[id], e.target.value);
            });
        })(marketFields[m]);
    }

    document.getElementById('expectation').addEventListener('input', debounce(function (e) {
        ui.saveJournalField('marketAwareness', 'expectation', e.target.value);
    }, 500));

    // Reflection auto-save
    document.getElementById('followedRulesYes').addEventListener('click', function () {
        var journal = ui.getCurrentJournal();
        if (!journal || journal.isLocked) return;

        document.getElementById('followedRulesYes').classList.add('active');
        document.getElementById('followedRulesNo').classList.remove('active');
        document.getElementById('brokenRuleGroup').style.display = 'none';
        ui.saveJournalField('reflection', 'followedRules', true);
    });

    document.getElementById('followedRulesNo').addEventListener('click', function () {
        var journal = ui.getCurrentJournal();
        if (!journal || journal.isLocked) return;

        document.getElementById('followedRulesYes').classList.remove('active');
        document.getElementById('followedRulesNo').classList.add('active');
        document.getElementById('brokenRuleGroup').style.display = 'flex';
        ui.saveJournalField('reflection', 'followedRules', false);
    });

    document.getElementById('brokenRule').addEventListener('input', debounce(function (e) {
        ui.saveJournalField('reflection', 'brokenRule', e.target.value);
    }, 500));

    document.getElementById('biggestMistake').addEventListener('input', debounce(function (e) {
        ui.saveJournalField('reflection', 'biggestMistake', e.target.value);
    }, 500));

    document.getElementById('bestDecision').addEventListener('input', debounce(function (e) {
        ui.saveJournalField('reflection', 'bestDecision', e.target.value);
    }, 500));

    // Rating buttons
    var emotionalBtns = document.getElementById('emotionalState').querySelectorAll('.rating-btn');
    for (var e = 0; e < emotionalBtns.length; e++) {
        (function (btn) {
            btn.addEventListener('click', function () {
                var journal = ui.getCurrentJournal();
                if (!journal || journal.isLocked) return;

                var allBtns = document.getElementById('emotionalState').querySelectorAll('.rating-btn');
                for (var x = 0; x < allBtns.length; x++) {
                    allBtns[x].classList.remove('active');
                }
                btn.classList.add('active');
                ui.saveJournalField('reflection', 'emotionalState', parseInt(btn.dataset.value));
            });
        })(emotionalBtns[e]);
    }

    var energyBtns = document.getElementById('energyLevel').querySelectorAll('.rating-btn');
    for (var n = 0; n < energyBtns.length; n++) {
        (function (btn) {
            btn.addEventListener('click', function () {
                var journal = ui.getCurrentJournal();
                if (!journal || journal.isLocked) return;

                var allBtns = document.getElementById('energyLevel').querySelectorAll('.rating-btn');
                for (var x = 0; x < allBtns.length; x++) {
                    allBtns[x].classList.remove('active');
                }
                btn.classList.add('active');
                ui.saveJournalField('reflection', 'energyLevel', parseInt(btn.dataset.value));
            });
        })(energyBtns[n]);
    }

    document.getElementById('traderType').addEventListener('input', debounce(function (e) {
        ui.saveJournalField('reflection', 'traderType', e.target.value);
    }, 500));

    // Lesson auto-save
    document.getElementById('lessonOfDay').addEventListener('input', debounce(function (e) {
        ui.saveJournalField('lesson', 'lessonOfDay', e.target.value);
    }, 500));

    document.getElementById('tomorrowAdjustment').addEventListener('input', debounce(function (e) {
        ui.saveJournalField('lesson', 'tomorrowAdjustment', e.target.value);
    }, 500));

    // ========================
    // Trade Modal Events
    // ========================

    document.getElementById('addTradeBtn').addEventListener('click', function () {
        ui.openTradeModal();
    });

    document.getElementById('closeTradeModal').addEventListener('click', function () {
        ui.closeTradeModal();
    });

    document.getElementById('cancelTrade').addEventListener('click', function () {
        ui.closeTradeModal();
    });

    document.getElementById('tradeModal').addEventListener('click', function (e) {
        if (e.target === document.getElementById('tradeModal')) {
            ui.closeTradeModal();
        }
    });

    // Emotion buttons in trade modal
    var emotionBtns = document.getElementById('emotionButtons').querySelectorAll('.emotion-btn');
    for (var b = 0; b < emotionBtns.length; b++) {
        (function (btn) {
            btn.addEventListener('click', function () {
                var allBtns = document.getElementById('emotionButtons').querySelectorAll('.emotion-btn');
                for (var x = 0; x < allBtns.length; x++) {
                    allBtns[x].classList.remove('active');
                }
                btn.classList.add('active');
            });
        })(emotionBtns[b]);
    }

    document.getElementById('saveTrade').addEventListener('click', function () {
        ui.saveTrade();
    });

    document.getElementById('deleteTrade').addEventListener('click', function () {
        ui.deleteTrade();
    });

    // ========================
    // Lock Modal Events
    // ========================

    document.getElementById('lockJournalBtn').addEventListener('click', function () {
        ui.openLockModal();
    });

    document.getElementById('closeLockModal').addEventListener('click', function () {
        ui.closeLockModal();
    });

    document.getElementById('cancelLock').addEventListener('click', function () {
        ui.closeLockModal();
    });

    document.getElementById('confirmLock').addEventListener('click', function () {
        ui.confirmLock();
    });

    document.getElementById('lockModal').addEventListener('click', function (e) {
        if (e.target === document.getElementById('lockModal')) {
            ui.closeLockModal();
        }
    });

    // ========================
    // Theme Toggle
    // ========================

    document.getElementById('themeToggle').addEventListener('click', function () {
        var currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
        var newTheme = currentTheme === 'light' ? 'dark' : 'light';
        storage.setTheme(newTheme);
    });

    // ========================
    // Keyboard Shortcuts
    // ========================

    document.addEventListener('keydown', function (e) {
        // Escape to close modals
        if (e.key === 'Escape') {
            ui.closeTradeModal();
            ui.closeLockModal();
        }

        // Ctrl+S to save (prevent default)
        if (e.ctrlKey && e.key === 's') {
            e.preventDefault();
            ui.showToast('All changes saved automatically', 'success');
        }
    });

    console.log('InnerEdge initialized successfully');
});

// Debounce helper function
function debounce(func, wait) {
    var timeout;
    return function () {
        var context = this;
        var args = arguments;
        var later = function () {
            clearTimeout(timeout);
            func.apply(context, args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}
