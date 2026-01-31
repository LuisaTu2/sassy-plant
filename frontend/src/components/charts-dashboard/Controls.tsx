import { type Dispatch, type SetStateAction } from "react";
import "./Controls.css";

interface ControlsProps {
  connected: boolean;
  setConnected: Dispatch<SetStateAction<boolean>>;
}

const Controls = ({ connected, setConnected }: ControlsProps) => {
  return (
    <div className="controls-section">
      <div className="control">
        <span>enable sensor readings</span>
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
      <div className="control"></div>
    </div>
  );
};

export default Controls;
