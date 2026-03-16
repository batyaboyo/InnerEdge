/**
 * InnerEdge - Weekly Summary Module
 * Analytics, patterns, and insights
 */

// Initialize namespace
window.InnerEdge = window.InnerEdge || {};

var currentWeekStart = null;

// Initialize summary
function initSummary() {
    var models = window.InnerEdge.models;
    var week = models.getWeekBoundaries();
    currentWeekStart = week.start;

    // Event listeners
    document.getElementById('prevWeek').addEventListener('click', function () {
        currentWeekStart = new Date(currentWeekStart);
        currentWeekStart.setDate(currentWeekStart.getDate() - 7);
        renderSummary();
    });

    document.getElementById('nextWeek').addEventListener('click', function () {
        currentWeekStart = new Date(currentWeekStart);
        currentWeekStart.setDate(currentWeekStart.getDate() + 7);
        renderSummary();
    });
}

// Render full summary
function renderSummary() {
    var models = window.InnerEdge.models;
    var storage = window.InnerEdge.storage;

    var weekEnd = new Date(currentWeekStart);
    weekEnd.setDate(weekEnd.getDate() + 6);

    // Update week label
    document.getElementById('currentWeek').textContent = models.formatWeekRange(currentWeekStart, weekEnd);

    // Get week's journals
    var journals = storage.getJournalsByWeek(currentWeekStart, weekEnd);

    // Calculate stats
    var stats = calculateWeeklyStats(journals);

    // Render all sections
    renderSummaryStats(stats);
    renderResultsChart(stats);
    renderPatterns(stats);
    renderEmotionsChart(stats);
    renderInsights(stats, journals);
    renderMistakes(stats);
}

// Calculate weekly statistics
function calculateWeeklyStats(journals) {
    var stats = {
        tradingDays: journals.length,
        totalTrades: 0,
        wins: 0,
        losses: 0,
        breakeven: 0,
        totalR: 0,
        emotions: {},
        mistakes: {},
        unplannedTrades: 0,
        unplannedLosses: 0,
        lowEnergyDays: 0,
        lowEnergyLosses: 0,
        brokenRules: 0,
        followedRules: 0
    };

    for (var i = 0; i < journals.length; i++) {
        var journal = journals[i];

        // Trades
        for (var j = 0; j < journal.trades.length; j++) {
            var trade = journal.trades[j];
            stats.totalTrades++;

            if (trade.result === 'Win') stats.wins++;
            else if (trade.result === 'Loss') stats.losses++;
            else if (trade.result === 'Break-even') stats.breakeven++;

            if (trade.rValue) stats.totalR += parseFloat(trade.rValue);

            // Emotions
            if (trade.emotion) {
                stats.emotions[trade.emotion] = (stats.emotions[trade.emotion] || 0) + 1;
            }

            // Unplanned trades
            if (!trade.planned) {
                stats.unplannedTrades++;
                if (trade.result === 'Loss') {
                    stats.unplannedLosses++;
                }
            }
        }

        // Mistakes
        if (journal.reflection.biggestMistake) {
            var mistake = journal.reflection.biggestMistake.toLowerCase().trim();
            if (mistake) {
                stats.mistakes[mistake] = (stats.mistakes[mistake] || 0) + 1;
            }
        }

        // Energy and losses correlation
        if (journal.reflection.energyLevel && journal.reflection.energyLevel <= 2) {
            stats.lowEnergyDays++;
            for (var k = 0; k < journal.trades.length; k++) {
                if (journal.trades[k].result === 'Loss') {
                    stats.lowEnergyLosses++;
                }
            }
        }

        // Rule following
        if (journal.reflection.followedRules === true) {
            stats.followedRules++;
        } else if (journal.reflection.followedRules === false) {
            stats.brokenRules++;
        }
    }

    // Find most common emotion
    var maxEmotionCount = 0;
    stats.mostCommonEmotion = 'None';
    for (var emotion in stats.emotions) {
        if (stats.emotions[emotion] > maxEmotionCount) {
            maxEmotionCount = stats.emotions[emotion];
            stats.mostCommonEmotion = emotion;
        }
    }

    // Find most common mistakes
    var sortedMistakes = [];
    for (var m in stats.mistakes) {
        sortedMistakes.push([m, stats.mistakes[m]]);
    }
    sortedMistakes.sort(function (a, b) { return b[1] - a[1]; });
    stats.topMistakes = sortedMistakes.slice(0, 3);

    return stats;
}

// Render summary stats
function renderSummaryStats(stats) {
    var winRate = stats.totalTrades > 0
        ? ((stats.wins / stats.totalTrades) * 100).toFixed(1)
        : 0;

    document.getElementById('summaryStats').innerHTML =
        '<div class="stat-item">' +
        '<div class="stat-value">' + stats.tradingDays + '</div>' +
        '<div class="stat-label">Trading Days</div>' +
        '</div>' +
        '<div class="stat-item">' +
        '<div class="stat-value">' + stats.totalTrades + '</div>' +
        '<div class="stat-label">Total Trades</div>' +
        '</div>' +
        '<div class="stat-item">' +
        '<div class="stat-value win">' + stats.wins + '</div>' +
        '<div class="stat-label">Wins</div>' +
        '</div>' +
        '<div class="stat-item">' +
        '<div class="stat-value loss">' + stats.losses + '</div>' +
        '<div class="stat-label">Losses</div>' +
        '</div>' +
        '<div class="stat-item">' +
        '<div class="stat-value breakeven">' + stats.breakeven + '</div>' +
        '<div class="stat-label">Break-even</div>' +
        '</div>' +
        '<div class="stat-item">' +
        '<div class="stat-value ' + (stats.totalR >= 0 ? 'win' : 'loss') + '">' + (stats.totalR >= 0 ? '+' : '') + stats.totalR.toFixed(1) + 'R</div>' +
        '<div class="stat-label">Total R</div>' +
        '</div>' +
        '<div class="stat-item">' +
        '<div class="stat-value">' + winRate + '%</div>' +
        '<div class="stat-label">Win Rate</div>' +
        '</div>' +
        '<div class="stat-item">' +
        '<div class="stat-value">' + stats.followedRules + '/' + stats.tradingDays + '</div>' +
        '<div class="stat-label">Rules Followed</div>' +
        '</div>';
}

// Render results chart
function renderResultsChart(stats) {
    var maxValue = Math.max(stats.wins, stats.losses, stats.breakeven, 1);
    var scale = 120; // Max height in pixels

    document.getElementById('resultsChart').innerHTML =
        '<div class="chart-bar">' +
        '<div class="chart-bar-value">' + stats.wins + '</div>' +
        '<div class="chart-bar-fill win" style="height: ' + ((stats.wins / maxValue) * scale) + 'px"></div>' +
        '<div class="chart-bar-label">Wins</div>' +
        '</div>' +
        '<div class="chart-bar">' +
        '<div class="chart-bar-value">' + stats.losses + '</div>' +
        '<div class="chart-bar-fill loss" style="height: ' + ((stats.losses / maxValue) * scale) + 'px"></div>' +
        '<div class="chart-bar-label">Losses</div>' +
        '</div>' +
        '<div class="chart-bar">' +
        '<div class="chart-bar-value">' + stats.breakeven + '</div>' +
        '<div class="chart-bar-fill breakeven" style="height: ' + ((stats.breakeven / maxValue) * scale) + 'px"></div>' +
        '<div class="chart-bar-label">BE</div>' +
        '</div>';
}

// Render patterns
function renderPatterns(stats) {
    var emotionEmojis = {
        'Calm': '😌',
        'Bored': '😐',
        'Afraid': '😰',
        'Excited': '😄',
        'Impulsive': '😤',
        'None': '🤷'
    };

    document.getElementById('patternsList').innerHTML =
        '<div class="pattern-item">' +
        '<div class="pattern-icon">' + (emotionEmojis[stats.mostCommonEmotion] || '🤷') + '</div>' +
        '<div class="pattern-info">' +
        '<div class="pattern-label">Most Common Emotion</div>' +
        '<div class="pattern-value">' + stats.mostCommonEmotion + '</div>' +
        '</div>' +
        '</div>' +
        '<div class="pattern-item">' +
        '<div class="pattern-icon">📊</div>' +
        '<div class="pattern-info">' +
        '<div class="pattern-label">Unplanned Trades</div>' +
        '<div class="pattern-value">' + stats.unplannedTrades + ' of ' + stats.totalTrades + '</div>' +
        '</div>' +
        '</div>' +
        '<div class="pattern-item">' +
        '<div class="pattern-icon">📋</div>' +
        '<div class="pattern-info">' +
        '<div class="pattern-label">Rules Broken</div>' +
        '<div class="pattern-value">' + stats.brokenRules + ' day' + (stats.brokenRules !== 1 ? 's' : '') + '</div>' +
        '</div>' +
        '</div>';
}

// Render emotions chart
function renderEmotionsChart(stats) {
    var emotions = ['Calm', 'Bored', 'Afraid', 'Excited', 'Impulsive'];
    var maxCount = 1;
    for (var e in stats.emotions) {
        if (stats.emotions[e] > maxCount) maxCount = stats.emotions[e];
    }

    var html = '';
    for (var i = 0; i < emotions.length; i++) {
        var emotion = emotions[i];
        var count = stats.emotions[emotion] || 0;
        var percentage = (count / maxCount) * 100;

        html += '<div class="emotion-bar-container">' +
            '<div class="emotion-bar-label">' + emotion + '</div>' +
            '<div class="emotion-bar-track">' +
            '<div class="emotion-bar-fill" style="width: ' + percentage + '%"></div>' +
            '</div>' +
            '<div class="emotion-bar-count">' + count + '</div>' +
            '</div>';
    }
    document.getElementById('emotionsChart').innerHTML = html;
}

// Render insights
function renderInsights(stats, journals) {
    var insights = [];

    // Low energy correlation
    if (stats.lowEnergyDays > 0 && stats.lowEnergyLosses > 0 && stats.losses > 0) {
        var lossRate = ((stats.lowEnergyLosses / stats.losses) * 100).toFixed(0);
        if (lossRate > 30) {
            insights.push({
                type: 'warning',
                text: '<strong>' + lossRate + '%</strong> of your losses happened on low-energy days. Consider resting when energy is below 3.'
            });
        }
    }

    // Unplanned trades correlation
    if (stats.unplannedTrades > 0 && stats.unplannedLosses > 0) {
        var unplannedLossRate = ((stats.unplannedLosses / stats.unplannedTrades) * 100).toFixed(0);
        if (unplannedLossRate > 50) {
            insights.push({
                type: 'danger',
                text: '<strong>' + unplannedLossRate + '%</strong> of unplanned trades resulted in losses. Stick to your trading plan.'
            });
        }
    }

    // Rule following insight
    if (stats.brokenRules > 0 && stats.tradingDays > 0) {
        var brokenRate = ((stats.brokenRules / stats.tradingDays) * 100).toFixed(0);
        if (brokenRate > 30) {
            insights.push({
                type: 'warning',
                text: 'You broke your rules on <strong>' + brokenRate + '%</strong> of trading days. Review your rules and commitment.'
            });
        }
    }

    // Positive insight
    if (stats.followedRules === stats.tradingDays && stats.tradingDays > 0) {
        insights.push({
            type: 'success',
            text: '<strong>Great discipline!</strong> You followed your rules every trading day this week.'
        });
    }

    // Win rate insight
    if (stats.totalTrades >= 5) {
        var winRate = (stats.wins / stats.totalTrades) * 100;
        if (winRate >= 60) {
            insights.push({
                type: 'success',
                text: 'Strong win rate of <strong>' + winRate.toFixed(0) + '%</strong> this week. Keep doing what works!'
            });
        }
    }

    // Default insight
    if (insights.length === 0) {
        if (stats.totalTrades === 0) {
            insights.push({
                type: 'info',
                text: 'No trades recorded this week. Start journaling to see insights!'
            });
        } else {
            insights.push({
                type: 'info',
                text: 'Keep journaling consistently to unlock more insights about your trading patterns.'
            });
        }
    }

    var html = '';
    for (var i = 0; i < insights.length; i++) {
        html += '<div class="insight-item ' + insights[i].type + '">' +
            '<div class="insight-text">' + insights[i].text + '</div>' +
            '</div>';
    }
    document.getElementById('insightsList').innerHTML = html;
}

// Render common mistakes
function renderMistakes(stats) {
    if (stats.topMistakes.length === 0) {
        document.getElementById('mistakesList').innerHTML =
            '<div class="empty-state">' +
            '<p>No mistakes recorded this week</p>' +
            '</div>';
        return;
    }

    var html = '';
    for (var i = 0; i < stats.topMistakes.length; i++) {
        var mistake = stats.topMistakes[i][0];
        var count = stats.topMistakes[i][1];
        html += '<div class="mistake-item">' +
            '<div class="mistake-count">' + count + '</div>' +
            '<div class="mistake-text">' + mistake.charAt(0).toUpperCase() + mistake.slice(1) + '</div>' +
            '</div>';
    }
    document.getElementById('mistakesList').innerHTML = html;
}

// Export summary functions
window.InnerEdge.summary = {
    initSummary: initSummary,
    renderSummary: renderSummary,
    calculateWeeklyStats: calculateWeeklyStats
};
