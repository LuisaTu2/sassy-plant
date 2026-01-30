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
import "./SensorsChart.css";

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
const SensorsChart = ({ data }: StatePlotProps) => {
  return (
    <div className="sensors-chart-graph">
      <h2 className="sensors-chart-title">sensors chart</h2>

      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={data}>
          <XAxis dataKey="timestamp" tickFormatter={formatTime} />
          <YAxis />
          <Line
            type="monotone"
            dataKey="soil_moisture"
            stroke="#4caf50"
            strokeWidth={"10px"}
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

export default SensorsChart;
