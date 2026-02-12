import { useState } from "react";
import "./App.css";
import ChartsDashboard from "./components/charts-dashboard/ChartsDashboard";
import { ChartSettingsProvider } from "./components/contexts/ChartSettingsContextProvider";
import { PlantSettingsProvider } from "./components/contexts/PlantSettingsContextProvider";
import PlantDashboard from "./components/plant-dashboard/PlantDashboard";
import Notes from "./components/Notes";

function App() {
  const [showNotes, setShowNotes] = useState<boolean>(false);
  return (
    <PlantSettingsProvider>
      <ChartSettingsProvider>
        <div className="app">
          <div className="title">the &middot; sassy &middot; plant</div>
          <div className="dashboard">
            <PlantDashboard />
            <ChartsDashboard />
          </div>
        </div>
        <div className="footer">
          made with 💚 in
          <span onClick={() => setShowNotes(!showNotes)} className="maple-leaf">
            {" "}
            🍁{" "}
          </span>
          by <a href="https://github.com/LuisaTu2"> 🐰</a>
          {showNotes && <Notes setShowNotes={setShowNotes} />}
        </div>
      </ChartSettingsProvider>
    </PlantSettingsProvider>
  );
}

export default App;
