import "./App.css";
import ChartsDashboard from "./components/charts-dashboard/ChartsDashboard";
import { ChartSettingsProvider } from "./components/contexts/ChartSettingsContextProvider";
import { PlantSettingsProvider } from "./components/contexts/PlantSettingsContextProvider";
import PlantDashboard from "./components/plant-dashboard/PlantDashboard";

function App() {
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
          made with 💚 in 🍁 by <a href="https://github.com/LuisaTu2">🐰 </a>
        </div>
      </ChartSettingsProvider>
    </PlantSettingsProvider>
  );
}

export default App;
