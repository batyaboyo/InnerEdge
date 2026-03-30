# InnerEdge Frontend

React-based frontend for the InnerEdge CFD trader SaaS platform.

## Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend will run on `http://localhost:3000` and proxy API requests to `http://localhost:8000`.

## Architecture

- **React 18** with TypeScript
- **Vite** for fast development
- **Zustand** for state management
- **TailwindCSS** for styling
- **Recharts** for data visualization
- **Axios** for API requests

## Features

- **Authentication**: Login/logout with Django token auth
- **Dashboard**: Trade summary, P/L, win rate
- **Trade Journal**: View, filter, and manage trades
- **Alerts**: Real-time alerts and notifications
- **Billing**: Plan selection and subscription management
- **Responsive Design**: Mobile-friendly layout

## Project Structure

```text
frontend/
├── src/
│   ├── components/      # Reusable React components
│   ├── pages/           # Page components (Dashboard, TradeJournal, etc.)
│   ├── store/           # Zustand state stores
│   ├── lib/             # Utility functions
│   ├── App.tsx          # Root component
│   ├── main.tsx         # Entry point
│   └── index.css        # Global styles
├── public/              # Static assets
├── package.json         # Dependencies
├── vite.config.ts       # Vite configuration
├── tsconfig.json        # TypeScript configuration
└── tailwind.config.ts   # Tailwind configuration
```

## Environment

Create a `.env` file in the frontend directory if needed:

```dotenv
VITE_API_URL=http://localhost:8000/api
```

## Building

```bash
npm run build
```

Output will be in the `dist/` directory ready for production deployment.

## Quality Gates

Run the full frontend quality pipeline:

```bash
npm run verify
```

This runs:
- `npm run lint`
- `npm run type-check`
- `npm run build`
