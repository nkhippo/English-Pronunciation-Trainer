import { useState } from "react";
import CEFRFilter, {
  type CEFRLevel,
} from "./components/CEFRFilter";

const INITIAL_LEVELS: CEFRLevel[] = ["A1", "A2"];

export default function App() {
  const [selectedLevels, setSelectedLevels] =
    useState<CEFRLevel[]>(INITIAL_LEVELS);

  return (
    <main className="prototype">
      <h1>CEFR filter prototype</h1>
      <p>
        Toggle one or more levels. The parent component receives the current
        selection.
      </p>

      <CEFRFilter
        initialSelected={INITIAL_LEVELS}
        onChange={setSelectedLevels}
      />

      <section className="debug-output" aria-live="polite">
        <h2>Selected levels</h2>
        <pre>{JSON.stringify(selectedLevels, null, 2)}</pre>
      </section>
    </main>
  );
}
