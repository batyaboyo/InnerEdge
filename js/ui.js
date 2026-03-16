/**
 * InnerEdge - UI Rendering
 * Handles all DOM manipulation and UI updates
 */

// Initialize namespace
window.InnerEdge = window.InnerEdge || {};

// Current state
var currentJournal = null;
var currentTradeId = null;

// DOM Elements cache
var elements = {};

// Initialize DOM element references
function initElements() {
    // Views
    elements.dashboardView = document.getElementById('dashboardView');
    elements.journalView = document.getElementById('journalView');
    elements.summaryView = document.getElementById('summaryView');

    // Dashboard
    elements.calendarGrid = document.getElementById('calendarGrid');
    elements.currentMonth = document.getElementById('currentMonth');
    elements.recentList = document.getElementById('recentList');
    elements.quickStats = document.getElementById('quickStats');
    elements.createTodayBtn = document.getElementById('createTodayBtn');

    // Journal
    elements.journalDate = document.getElementById('journalDate');
    elements.journalStatus = document.getElementById('journalStatus');
    elements.lockJournalBtn = document.getElementById('lockJournalBtn');
    elements.tradesList = document.getElementById('tradesList');
    elements.addTradeBtn = document.getElementById('addTradeBtn');

    // Market Awareness
    elements.session = document.getElementById('session');
    elements.marketCondition = document.getElementById('marketCondition');
    elements.bias = document.getElementById('bias');
    elements.expectation = document.getElementById('expectation');

    // Reflection
    elements.followedRulesYes = document.getElementById('followedRulesYes');
    elements.followedRulesNo = document.getElementById('followedRulesNo');
    elements.brokenRuleGroup = document.getElementById('brokenRuleGroup');
    elements.brokenRule = document.getElementById('brokenRule');
    elements.biggestMistake = document.getElementById('biggestMistake');
    elements.bestDecision = document.getElementById('bestDecision');
    elements.emotionalState = document.getElementById('emotionalState');
    elements.energyLevel = document.getElementById('energyLevel');
    elements.traderType = document.getElementById('traderType');

    // Lesson
    elements.lessonOfDay = document.getElementById('lessonOfDay');
    elements.tomorrowAdjustment = document.getElementById('tomorrowAdjustment');

    // Trade Modal
    elements.tradeModal = document.getElementById('tradeModal');
    elements.tradeModalTitle = document.getElementById('tradeModalTitle');
    elements.tradeForm = document.getElementById('tradeForm');
    elements.tradeId = document.getElementById('tradeId');
    elements.tradeAsset = document.getElementById('tradeAsset');
    elements.tradeSetup = document.getElementById('tradeSetup');
    elements.tradeTime = document.getElementById('tradeTime');
    elements.tradePlanned = document.getElementById('tradePlanned');
    elements.tradeEntry = document.getElementById('tradeEntry');
    elements.tradeSL = document.getElementById('tradeSL');
    elements.tradeTP = document.getElementById('tradeTP');
    elements.tradeResult = document.getElementById('tradeResult');
    elements.tradeR = document.getElementById('tradeR');
    elements.emotionButtons = document.getElementById('emotionButtons');
    elements.tradeReason = document.getElementById('tradeReason');
    elements.saveTrade = document.getElementById('saveTrade');
    elements.deleteTrade = document.getElementById('deleteTrade');
    elements.cancelTrade = document.getElementById('cancelTrade');
    elements.closeTradeModal = document.getElementById('closeTradeModal');

    // Lock Modal
    elements.lockModal = document.getElementById('lockModal');
    elements.lockChecklist = document.getElementById('lockChecklist');
    elements.confirmLock = document.getElementById('confirmLock');
    elements.cancelLock = document.getElementById('cancelLock');
    elements.closeLockModal = document.getElementById('closeLockModal');

    // Toast
    elements.toastContainer = document.getElementById('toastContainer');
}

// Switch between views
function showView(viewName) {
    // Update nav buttons
    var navBtns = document.querySelectorAll('.nav-btn');
    for (var i = 0; i < navBtns.length; i++) {
        var btn = navBtns[i];
        if (btn.dataset.view === viewName) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    }

    // Update views
    var views = document.querySelectorAll('.view');
    for (var j = 0; j < views.length; j++) {
        views[j].classList.remove('active');
    }

    var viewElement = document.getElementById(viewName + 'View');
    if (viewElement) {
        viewElement.classList.add('active');
    }
}

// Render dashboard
function renderDashboard() {
    renderRecentJournals();
    renderQuickStats();
}

// Render recent journals list
function renderRecentJournals() {
    var models = window.InnerEdge.models;
    var storage = window.InnerEdge.storage;
    var recent = storage.getRecentJournals(5);

    if (recent.length === 0) {
        elements.recentList.innerHTML =
            '<div class="empty-state">' +
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">' +
            '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>' +
            '<polyline points="14 2 14 8 20 8"/>' +
            '</svg>' +
            '<p>No journals yet. Create your first one!</p>' +
            '</div>';
        return;
    }

    var html = '';
    for (var i = 0; i < recent.length; i++) {
        var journal = recent[i];
        var dm = models.getDayMonth(journal.id);
        var stats = models.calculateJournalStats(journal);
        var statsText = stats.totalTrades > 0
            ? stats.wins + 'W / ' + stats.losses + 'L / ' + stats.breakeven + 'BE'
            : 'No trades';

        html += '<div class="recent-item" data-date="' + journal.id + '">' +
            '<div class="recent-item-date">' +
            '<span class="recent-item-day">' + dm.day + '</span>' +
            '<span class="recent-item-month">' + dm.month + '</span>' +
            '</div>' +
            '<div class="recent-item-info">' +
            '<div class="recent-item-trades">' + stats.totalTrades + ' trade' + (stats.totalTrades !== 1 ? 's' : '') + '</div>' +
            '<div class="recent-item-stats">' + statsText + '</div>' +
            '</div>' +
            '<span class="recent-item-status ' + (journal.isLocked ? 'locked' : 'draft') + '">' +
            (journal.isLocked ? 'Locked' : 'Draft') +
            '</span>' +
            '</div>';
    }
    elements.recentList.innerHTML = html;

    // Add click handlers
    var items = elements.recentList.querySelectorAll('.recent-item');
    for (var j = 0; j < items.length; j++) {
        (function (item) {
            item.addEventListener('click', function () {
                openJournal(item.dataset.date);
            });
        })(items[j]);
    }
}

// Render quick stats for current week
function renderQuickStats() {
    var models = window.InnerEdge.models;
    var storage = window.InnerEdge.storage;
    var week = models.getWeekBoundaries();
    var weekJournals = storage.getJournalsByWeek(week.start, week.end);

    var totalTrades = 0;
    var wins = 0;
    var losses = 0;

    for (var i = 0; i < weekJournals.length; i++) {
        var stats = models.calculateJournalStats(weekJournals[i]);
        totalTrades += stats.totalTrades;
        wins += stats.wins;
        losses += stats.losses;
    }

    elements.quickStats.innerHTML =
        '<div class="stat-item">' +
        '<div class="stat-value">' + weekJournals.length + '</div>' +
        '<div class="stat-label">Trading Days</div>' +
        '</div>' +
        '<div class="stat-item">' +
        '<div class="stat-value">' + totalTrades + '</div>' +
        '<div class="stat-label">Total Trades</div>' +
        '</div>' +
        '<div class="stat-item">' +
        '<div class="stat-value win">' + wins + '</div>' +
        '<div class="stat-label">Wins</div>' +
        '</div>' +
        '<div class="stat-item">' +
        '<div class="stat-value loss">' + losses + '</div>' +
        '<div class="stat-label">Losses</div>' +
        '</div>';
}

// Open a journal for viewing/editing
function openJournal(dateId) {
    var models = window.InnerEdge.models;
    var storage = window.InnerEdge.storage;
    var journal = storage.getJournal(dateId);

    if (!journal) {
        journal = models.createDayJournal(dateId);
        storage.saveJournal(journal);
    }

    currentJournal = journal;
    renderJournalView();
    showView('journal');
}

// Render journal view
function renderJournalView() {
    var models = window.InnerEdge.models;
    if (!currentJournal) return;

    var isLocked = currentJournal.isLocked;

    // Update header
    elements.journalDate.textContent = models.formatDate(currentJournal.id);
    elements.journalStatus.textContent = isLocked ? 'Locked' : 'Draft';
    elements.journalStatus.className = 'journal-status' + (isLocked ? ' locked' : '');

    // Update lock button
    elements.lockJournalBtn.style.display = isLocked ? 'none' : 'inline-flex';

    // Update sections with locked state
    var sections = document.querySelectorAll('.journal-section');
    for (var i = 0; i < sections.length; i++) {
        if (isLocked) {
            sections[i].classList.add('locked');
        } else {
            sections[i].classList.remove('locked');
        }
    }

    // Populate Market Awareness
    elements.session.value = currentJournal.marketAwareness.session || '';
    elements.marketCondition.value = currentJournal.marketAwareness.condition || '';
    elements.bias.value = currentJournal.marketAwareness.bias || '';
    elements.expectation.value = currentJournal.marketAwareness.expectation || '';

    // Populate trades
    renderTradesList();

    // Populate Reflection
    updateToggleButtons('followedRules', currentJournal.reflection.followedRules);
    elements.brokenRuleGroup.style.display = currentJournal.reflection.followedRules === false ? 'flex' : 'none';
    elements.brokenRule.value = currentJournal.reflection.brokenRule || '';
    elements.biggestMistake.value = currentJournal.reflection.biggestMistake || '';
    elements.bestDecision.value = currentJournal.reflection.bestDecision || '';
    updateRatingButtons('emotionalState', currentJournal.reflection.emotionalState);
    updateRatingButtons('energyLevel', currentJournal.reflection.energyLevel);
    elements.traderType.value = currentJournal.reflection.traderType || '';

    // Populate Lesson
    elements.lessonOfDay.value = currentJournal.lesson.lessonOfDay || '';
    elements.tomorrowAdjustment.value = currentJournal.lesson.tomorrowAdjustment || '';

    // Disable inputs if locked
    if (isLocked) {
        disableJournalInputs();
    } else {
        enableJournalInputs();
    }
}

// Render trades list
function renderTradesList() {
    var trades = currentJournal.trades || [];

    if (trades.length === 0) {
        elements.tradesList.innerHTML =
            '<div class="empty-state">' +
            '<p>No trades recorded yet</p>' +
            '</div>';
        return;
    }

    var html = '';
    for (var i = 0; i < trades.length; i++) {
        var trade = trades[i];
        var resultClass = trade.result ? trade.result.toLowerCase().replace('-', '') : 'pending';
        var resultSymbol = trade.result === 'Win' ? '✓' : trade.result === 'Loss' ? '✗' : trade.result === 'Break-even' ? '—' : '?';
        var rValue = trade.rValue ? (trade.rValue > 0 ? '+' + trade.rValue + 'R' : trade.rValue + 'R') : '';
        var rClass = trade.rValue > 0 ? 'positive' : trade.rValue < 0 ? 'negative' : '';

        html += '<div class="trade-card" data-trade-id="' + trade.id + '">' +
            '<div class="trade-result ' + resultClass + '">' + resultSymbol + '</div>' +
            '<div class="trade-info">' +
            '<div class="trade-asset">' + (trade.asset || 'Unknown Asset') + '</div>' +
            '<div class="trade-details">' +
            (trade.setupName ? trade.setupName + ' • ' : '') +
            (trade.time || 'No time') + ' • ' +
            (trade.planned ? 'Planned' : 'Unplanned') +
            '</div>' +
            '</div>' +
            (rValue ? '<div class="trade-r ' + rClass + '">' + rValue + '</div>' : '') +
            (trade.emotion ? '<span class="trade-emotion">' + getEmotionEmoji(trade.emotion) + ' ' + trade.emotion + '</span>' : '') +
            '</div>';
    }
    elements.tradesList.innerHTML = html;

    // Add click handlers
    var cards = elements.tradesList.querySelectorAll('.trade-card');
    for (var j = 0; j < cards.length; j++) {
        (function (card) {
            card.addEventListener('click', function () {
                if (!currentJournal.isLocked) {
                    openTradeModal(card.dataset.tradeId);
                }
            });
        })(cards[j]);
    }
}

// Get emoji for emotion
function getEmotionEmoji(emotion) {
    var emojis = {
        'Calm': '😌',
        'Bored': '😐',
        'Afraid': '😰',
        'Excited': '😄',
        'Impulsive': '😤'
    };
    return emojis[emotion] || '';
}

// Update toggle buttons state
function updateToggleButtons(name, value) {
    var yesBtn = document.getElementById(name + 'Yes');
    var noBtn = document.getElementById(name + 'No');

    if (value === true) {
        yesBtn.classList.add('active');
        noBtn.classList.remove('active');
    } else if (value === false) {
        yesBtn.classList.remove('active');
        noBtn.classList.add('active');
    } else {
        yesBtn.classList.remove('active');
        noBtn.classList.remove('active');
    }
}

// Update rating buttons state
function updateRatingButtons(groupId, value) {
    var group = document.getElementById(groupId);
    var btns = group.querySelectorAll('.rating-btn');
    for (var i = 0; i < btns.length; i++) {
        var btn = btns[i];
        if (parseInt(btn.dataset.value) === value) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    }
}

// Open trade modal
function openTradeModal(tradeId) {
    var models = window.InnerEdge.models;
    currentTradeId = tradeId || null;

    // Reset form
    elements.tradeForm.reset();
    var emotionBtns = elements.emotionButtons.querySelectorAll('.emotion-btn');
    for (var i = 0; i < emotionBtns.length; i++) {
        emotionBtns[i].classList.remove('active');
    }

    if (tradeId) {
        // Editing existing trade
        var trade = null;
        for (var j = 0; j < currentJournal.trades.length; j++) {
            if (currentJournal.trades[j].id === tradeId) {
                trade = currentJournal.trades[j];
                break;
            }
        }
        if (trade) {
            elements.tradeModalTitle.textContent = 'Edit Trade';
            elements.tradeId.value = trade.id;
            elements.tradeAsset.value = trade.asset || '';
            elements.tradeSetup.value = trade.setupName || '';
            elements.tradeTime.value = trade.time || '';
            elements.tradePlanned.value = trade.planned ? 'yes' : 'no';
            elements.tradeEntry.value = trade.entry || '';
            elements.tradeSL.value = trade.stopLoss || '';
            elements.tradeTP.value = trade.takeProfit || '';
            elements.tradeResult.value = trade.result || '';
            elements.tradeR.value = trade.rValue || '';
            elements.tradeReason.value = trade.reason || '';

            // Set emotion
            for (var k = 0; k < emotionBtns.length; k++) {
                if (emotionBtns[k].dataset.emotion === trade.emotion) {
                    emotionBtns[k].classList.add('active');
                }
            }

            elements.deleteTrade.style.display = 'inline-flex';
        }
    } else {
        // New trade
        elements.tradeModalTitle.textContent = 'Add Trade';
        elements.tradeId.value = '';
        elements.deleteTrade.style.display = 'none';

        // Set default time to current time
        var now = new Date();
        var hours = String(now.getHours()).padStart(2, '0');
        var mins = String(now.getMinutes()).padStart(2, '0');
        elements.tradeTime.value = hours + ':' + mins;
    }

    elements.tradeModal.classList.add('active');
}

// Close trade modal
function closeTradeModal() {
    elements.tradeModal.classList.remove('active');
    currentTradeId = null;
}

// Save trade
function saveTrade() {
    var models = window.InnerEdge.models;
    var storage = window.InnerEdge.storage;
    var selectedEmotion = elements.emotionButtons.querySelector('.emotion-btn.active');

    var tradeData = {
        id: elements.tradeId.value || models.generateId(),
        asset: elements.tradeAsset.value.trim(),
        setupName: elements.tradeSetup.value.trim(),
        time: elements.tradeTime.value,
        entry: elements.tradeEntry.value ? parseFloat(elements.tradeEntry.value) : null,
        stopLoss: elements.tradeSL.value ? parseFloat(elements.tradeSL.value) : null,
        takeProfit: elements.tradeTP.value ? parseFloat(elements.tradeTP.value) : null,
        planned: elements.tradePlanned.value === 'yes',
        result: elements.tradeResult.value,
        rValue: elements.tradeR.value ? parseFloat(elements.tradeR.value) : null,
        emotion: selectedEmotion ? selectedEmotion.dataset.emotion : '',
        reason: elements.tradeReason.value.trim()
    };

    if (!tradeData.asset) {
        showToast('Please enter an asset', 'error');
        return;
    }

    // Update or add trade
    var existingIndex = -1;
    for (var i = 0; i < currentJournal.trades.length; i++) {
        if (currentJournal.trades[i].id === tradeData.id) {
            existingIndex = i;
            break;
        }
    }

    if (existingIndex >= 0) {
        currentJournal.trades[existingIndex] = tradeData;
    } else {
        currentJournal.trades.push(tradeData);
    }

    storage.saveJournal(currentJournal);
    renderTradesList();
    closeTradeModal();
    showToast('Trade saved successfully', 'success');
}

// Delete trade
function deleteTrade() {
    var storage = window.InnerEdge.storage;
    if (!currentTradeId) return;

    var newTrades = [];
    for (var i = 0; i < currentJournal.trades.length; i++) {
        if (currentJournal.trades[i].id !== currentTradeId) {
            newTrades.push(currentJournal.trades[i]);
        }
    }
    currentJournal.trades = newTrades;

    storage.saveJournal(currentJournal);
    renderTradesList();
    closeTradeModal();
    showToast('Trade deleted', 'success');
}

// Open lock modal
function openLockModal() {
    var models = window.InnerEdge.models;
    var status = models.getJournalCompletionStatus(currentJournal);

    var checkIcon = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>';
    var uncheckIcon = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/></svg>';

    elements.lockChecklist.innerHTML =
        '<div class="lock-check-item ' + (status.marketAwareness ? 'complete' : 'incomplete') + '">' +
        (status.marketAwareness ? checkIcon : uncheckIcon) +
        '<span>Market Awareness filled</span>' +
        '</div>' +
        '<div class="lock-check-item ' + (status.trades ? 'complete' : 'incomplete') + '">' +
        (status.trades ? checkIcon : uncheckIcon) +
        '<span>At least one trade recorded</span>' +
        '</div>' +
        '<div class="lock-check-item ' + (status.reflection ? 'complete' : 'incomplete') + '">' +
        (status.reflection ? checkIcon : uncheckIcon) +
        '<span>Reflection completed</span>' +
        '</div>' +
        '<div class="lock-check-item ' + (status.lesson ? 'complete' : 'incomplete') + '">' +
        (status.lesson ? checkIcon : uncheckIcon) +
        '<span>Lesson & Adjustment written</span>' +
        '</div>';

    elements.lockModal.classList.add('active');
}

// Close lock modal
function closeLockModal() {
    elements.lockModal.classList.remove('active');
}

// Confirm lock
function confirmLock() {
    var storage = window.InnerEdge.storage;
    currentJournal.isLocked = true;
    storage.saveJournal(currentJournal);
    renderJournalView();
    closeLockModal();
    showToast('Journal locked successfully', 'success');
}

// Save journal fields
function saveJournalField(section, field, value) {
    var storage = window.InnerEdge.storage;
    if (!currentJournal || currentJournal.isLocked) return;

    if (section === 'marketAwareness') {
        currentJournal.marketAwareness[field] = value;
    } else if (section === 'reflection') {
        currentJournal.reflection[field] = value;
    } else if (section === 'lesson') {
        currentJournal.lesson[field] = value;
    }

    storage.saveJournal(currentJournal);
}

// Disable journal inputs
function disableJournalInputs() {
    var inputs = document.querySelectorAll('.journal-section .form-input, .journal-section .form-select, .journal-section .form-textarea');
    for (var i = 0; i < inputs.length; i++) {
        inputs[i].disabled = true;
    }
}

// Enable journal inputs
function enableJournalInputs() {
    var inputs = document.querySelectorAll('.journal-section .form-input, .journal-section .form-select, .journal-section .form-textarea');
    for (var i = 0; i < inputs.length; i++) {
        inputs[i].disabled = false;
    }
}

// Show toast notification
function showToast(message, type) {
    if (!type) type = 'success';
    var toast = document.createElement('div');
    toast.className = 'toast ' + type;
    toast.innerHTML = '<span class="toast-message">' + message + '</span>';

    elements.toastContainer.appendChild(toast);

    setTimeout(function () {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100%)';
        setTimeout(function () {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 300);
    }, 3000);
}

// Toggle section collapse
function toggleSection(section) {
    var content = section.querySelector('.section-content');
    var toggle = section.querySelector('.section-toggle');
    var isExpanded = toggle.getAttribute('aria-expanded') === 'true';

    toggle.setAttribute('aria-expanded', !isExpanded);
    if (isExpanded) {
        content.classList.add('collapsed');
    } else {
        content.classList.remove('collapsed');
    }
}

// Get current journal
function getCurrentJournal() {
    return currentJournal;
}

// Set current journal
function setCurrentJournal(journal) {
    currentJournal = journal;
}

// Export UI functions
window.InnerEdge.ui = {
    initElements: initElements,
    showView: showView,
    renderDashboard: renderDashboard,
    openJournal: openJournal,
    renderJournalView: renderJournalView,
    openTradeModal: openTradeModal,
    closeTradeModal: closeTradeModal,
    saveTrade: saveTrade,
    deleteTrade: deleteTrade,
    openLockModal: openLockModal,
    closeLockModal: closeLockModal,
    confirmLock: confirmLock,
    saveJournalField: saveJournalField,
    showToast: showToast,
    toggleSection: toggleSection,
    getCurrentJournal: getCurrentJournal,
    setCurrentJournal: setCurrentJournal
};
