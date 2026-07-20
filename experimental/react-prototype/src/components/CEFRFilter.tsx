import { useState } from "react";

export const CEFR_LEVELS = ["A1", "A2", "B1", "B2", "C1", "C2"] as const;

export type CEFRLevel = (typeof CEFR_LEVELS)[number];

type CEFRFilterProps = {
  initialSelected?: readonly CEFRLevel[];
  onChange: (selectedLevels: CEFRLevel[]) => void;
};

export default function CEFRFilter({
  initialSelected = [],
  onChange,
}: CEFRFilterProps) {
  const [selectedLevels, setSelectedLevels] = useState(
    () => new Set<CEFRLevel>(initialSelected),
  );

  const toggleLevel = (level: CEFRLevel) => {
    const nextLevels = new Set(selectedLevels);

    if (nextLevels.has(level)) {
      nextLevels.delete(level);
    } else {
      nextLevels.add(level);
    }

    setSelectedLevels(nextLevels);
    onChange(CEFR_LEVELS.filter((candidate) => nextLevels.has(candidate)));
  };

  return (
    <fieldset className="cefr-filter">
      <legend>CEFR level</legend>
      <div className="cefr-buttons">
        {CEFR_LEVELS.map((level) => {
          const isSelected = selectedLevels.has(level);

          return (
            <button
              aria-pressed={isSelected}
              className="cefr-button"
              key={level}
              onClick={() => toggleLevel(level)}
              type="button"
            >
              {level}
            </button>
          );
        })}
      </div>
    </fieldset>
  );
}
