import { useState, type Dispatch, type SetStateAction } from "react";
import "./Controls.css";

interface ControlsProps {
  connected: boolean;
  setConnected: Dispatch<SetStateAction<boolean>>;
}

const Controls = ({ connected, setConnected }: ControlsProps) => {
  const [value, setValue] = useState(5);

  return (
    <div className="controls-section">
      <div className="control">
        <span>enable plant state readings</span>
        <label className="toggle-switch">
          <input
            type="checkbox"
            checked={connected}
            disabled={connected}
            onChange={() => setConnected(!connected)}
          />
          <span className="slider"></span>
        </label>
      </div>
      <div className="control">
        <div className="tick-slider-container">
          <label className="tick-slider-label">sassiness level</label>
          <input
            type="range"
            min={1}
            max={10}
            step={1}
            value={value}
            onChange={(e) => setValue(parseInt(e.target.value))}
            className="tick-slider"
          />
          <div className="tick-slider-ticks">
            {Array.from({ length: 10 }, (_, i) => i + 1).map((tick) => (
              <span key={tick} onClick={() => setValue(tick)}>
                {tick}
              </span>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Controls;
