import { useState, type Dispatch, type SetStateAction } from "react";
import Menu from "./Menu";
import Plant from "./Plant";
import PlantSettings from "./PlantSettings";
import "./PlantDashboard.css";

interface PlantDashboardProps {
  isTalking: boolean;
  setIsTalking: Dispatch<SetStateAction<boolean>>;
}

const PlantDashboard = ({ isTalking, setIsTalking }: PlantDashboardProps) => {
  const [showSettings, setShowSettings] = useState<boolean>(false);
  return (
    <div className="plant-dasboard">
      <Plant isTalking={isTalking} />
      <Menu showSettings={showSettings} setShowSettings={setShowSettings} />
      <PlantSettings
        showSettings={showSettings}
        setShowSettings={setShowSettings}
      />
    </div>
  );
};

export default PlantDashboard;
