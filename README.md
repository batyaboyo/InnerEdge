# InnerEdge - Daily Trading Journal

> 🧠 A reflective trading journal designed to make you a better trader through honest self-assessment, not just record-keeping.

![InnerEdge](https://img.shields.io/badge/version-1.0.0-blue) ![License](https://img.shields.io/badge/license-MIT-green) ![Offline](https://img.shields.io/badge/offline-first-purple)

## Overview

InnerEdge is a clean, responsive web application that organizes your trading journey by day, not just by trade. Each trading day has a single journal page with four purposeful sections designed to transform your daily trading into a step toward mastery.

## Features

### 📊 Day-Based Organization
- Calendar navigation with visual indicators for journal entries
- Quick access to recent journals
- "Create Today's Journal" one-click action

### 📝 Four Reflective Sections

1. **Market Awareness** (Before Trading)
   - Session selection (Asia/London/New York)
   - Market condition assessment
   - Bias/expectation setting
   - Pre-trade mindset capture

2. **Trades Taken** (During the Day)
   - Multiple trades per day
   - Full trade details: asset, setup, entry/SL/TP
   - Planned vs unplanned tracking
   - Emotion at entry (Calm, Bored, Afraid, Excited, Impulsive)
   - R-value tracking

3. **Trader Reflection** (After Trading)
   - Rule adherence tracking
   - Mistake and best decision logging
   - Emotional and energy state (1-5 scale)
   - Self-assessment prompt

4. **Lesson & Adjustment**
   - Daily lesson capture
   - Tomorrow's adjustment planning

### 📈 Weekly Summary
- Trading activity statistics
- Win/Loss/BE distribution chart
- Emotional patterns visualization
- Rule-based insights:
  - "Losses often happen on low-energy days"
  - "Unplanned trades correlate with losses"
- Common mistake tracking

### ⚡ Additional Features
- 🔒 End-of-day lock encourages completing reflections
- 🌙 Light/Dark mode toggle
- 💾 Offline-first with LocalStorage
- ⌨️ Keyboard shortcuts (Esc to close modals)
- 📱 Fully responsive design

## Getting Started

### Option 1: Open Directly
Simply open `index.html` in your browser:
```
file:///path/to/InnerEdge/index.html
```

### Option 2: Use a Local Server
For the best experience, run a local server:
```bash
# Python 3
python -m http.server 8000

# Node.js (if you have npx)
npx serve .
```
Then visit `http://localhost:8000`

## Usage

1. **Start Your Day**: Click "Create Today's Journal" or navigate using the calendar
2. **Set Market Awareness**: Before trading, capture your session, market condition, and bias
3. **Log Trades**: Add each trade with full details including your emotional state
4. **Reflect**: After trading, honestly assess your rule-following, mistakes, and wins
5. **Learn**: Write your lesson and tomorrow's adjustment
6. **Lock**: Lock your journal to mark the day complete

## File Structure

```
InnerEdge/
├── index.html          # Main application
├── css/
│   └── styles.css      # Design system & styles
├── js/
│   ├── models.js       # Data structures
│   ├── storage.js      # LocalStorage manager
│   ├── ui.js           # UI rendering
│   ├── calendar.js     # Calendar navigation
│   ├── summary.js      # Weekly analytics
│   └── app.js          # Main controller
└── README.md           # Documentation
```

## Data Storage

All data is stored in your browser's LocalStorage. To export your data:
1. Open browser DevTools (F12)
2. Go to Application → Local Storage
3. Find and copy `inneredge_journals`

## Philosophy

InnerEdge is built on the belief that **trading success comes from self-awareness**, not just strategy. Every feature is designed to:

- Force honest reflection
- Reveal behavioral patterns
- Connect actions to outcomes
- Turn each day into a learning opportunity

> *"The market is a mirror. InnerEdge helps you see what it reflects."*

## License

MIT License - Feel free to modify and use for your trading journey.

---

Built with 💻 and ☕ for traders who want to grow.
