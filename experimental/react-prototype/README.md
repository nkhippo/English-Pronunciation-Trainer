# React + Vite CEFR filter prototype

This isolated Track B prototype checks whether the existing CEFR multi-select UI can be expressed as a small React component without changing the production SPA. It renders six CEFR toggles (A1–C2), keeps the selected levels in component state, reports changes to the parent, and shows the parent's state as JSON.

## Run locally

Use Node.js 20.19+ or 22.12+ as required by Vite 8, then run:

```bash
npm install
npm run dev
```

Open the localhost URL printed by Vite.

Create a production build with:

```bash
npm run build
```

## Phase 1 decisions

- **TypeScript:** The prototype uses TypeScript so component props, CEFR values, and parent/child state boundaries are explicit before a larger migration begins.
- **Local scope:** Dependencies, build output, and `.gitignore` stay under `experimental/react-prototype/`. The production build and Vercel configuration remain unchanged.
- **State model:** `CEFRFilter` uses a `Set` internally for independent multi-select toggles. It emits a stable, CEFR-ordered array through `onChange`, which gives the parent a serialization-friendly value.
- **No state library:** `useState` covers both component and parent state in this prototype. Adding a state library before cross-screen state and persistence requirements are known would not provide useful evidence.
- **Minimal Vite setup:** Vite handles TSX through its built-in transform. The React plugin, ESLint, UI frameworks, and testing libraries are intentionally deferred so this phase measures the smallest viable stack.
- **Initial selection:** A1 and A2 mirror the current setup defaults. C1 and C2 are included only to exercise the requested A1–C2 UI skeleton; they do not change the production data contract.

## Phase 2 and later questions

- Map the six-language i18n schema into typed React message access without duplicating keys.
- Define the React boundary for the TTS client, cache, accent selection, and GAS-to-backend migration.
- Preserve the Runtime data contract paths while deciding whether fetches belong in hooks, services, or route loaders.
- Decide how the React build output integrates with the existing language-specific Vercel build and URL structure.
- Inventory production CEFR behavior and data coverage before treating C1/C2 as functional filters.
- Choose persistence and shared-state boundaries for `prev_settings_v1`, session state, and cross-screen filters.
- Add a deliberate linting, unit-test, browser-test, and visual-regression strategy.
- Plan incremental component migration and rollback so the production SPA remains usable throughout Track B.
