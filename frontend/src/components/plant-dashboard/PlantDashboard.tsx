import Plant from "./Plant";
import PlantSettings from "./PlantSettings";
import "./PlantDashboard.css";
import Menu from "./Menu";

const PlantDashboard = () => {
  return (
    <div className="plant-dashboard">
      <Menu />
      <Plant />
      <PlantSettings />
    </div>
  );
};

export default PlantDashboard;
