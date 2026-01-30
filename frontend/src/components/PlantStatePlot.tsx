import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";
import ChartTooltip from "./ChartTooltip";
import "./PlantStatePlot.css";

type Point = {
  timestamp: string;
  soil_moisture: number;
};

// Tick formatter as a constant
const formatTime = (t: string) =>
  new Date(t).toLocaleTimeString("en-US", {
    hour12: false,
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    fractionalSecondDigits: 1,
  });

interface StatePlotProps {
  data: Point[];
}

// Dashboard component as a constant arrow function
const PlantStatePlot = ({ data }: StatePlotProps) => {
  return (
    <div className="plant-state-graph">
      <h2 className="plant-state-graph-title">plant state tracker</h2>

      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={data}>
          <XAxis dataKey="timestamp" tickFormatter={formatTime} />
          <YAxis />
          <Line
            type="monotone"
            dataKey="soil_moisture"
            stroke="#4caf50"
            dot={false}
            isAnimationActive={false}
          />
          <Tooltip content={<ChartTooltip />} />
          <Legend />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};

export default PlantStatePlot;
