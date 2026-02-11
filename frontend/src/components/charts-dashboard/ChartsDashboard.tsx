import "./ChartsDashboard.css";
import SensorsChart from "./SensorsChart";
import SassyText from "./SassyText";
import { useWebSocket } from "../useWebSocket";

const ChartsDashboard = () => {
  const { sendWsMessage } = useWebSocket();

  return (
    <div className="charts-dashboard">
      <div className="charts">
        <SassyText sendWsMessage={sendWsMessage} />
        <SensorsChart />
      </div>
    </div>
  );
};

export default ChartsDashboard;
