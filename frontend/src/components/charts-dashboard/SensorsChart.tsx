import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Legend,
  ReferenceArea,
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
    // hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    // fractionalSecondDigits: 1,
  });

interface StatePlotProps {
  data: Point[];
}

// Dashboard component as a constant arrow function
const SensorsChart = ({ data }: StatePlotProps) => {
  return (
    <div className="sensors-chart-graphs">
      <div className="sensors-chart-title">water & light monitoring</div>

      <ResponsiveContainer width="90%" height={300} className={"sensors-chart"}>
        <LineChart data={data}>
          <defs>
            {/* Gradient for happy state */}
            <linearGradient id="happyGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#daf5eb" stopOpacity={0.4} />
              <stop offset="50%" stopColor="#64daaf" stopOpacity={0.6} />
              <stop offset="100%" stopColor="#daf5eb" stopOpacity={0.4} />
            </linearGradient>
          </defs>
          <XAxis dataKey="timestamp" tickFormatter={formatTime} />
          <YAxis domain={[0, 1]} />
          <ReferenceArea
            y1={0.2}
            y2={0.8}
            fill="url(#happyGradient)"
            stroke="none"
          />
          <Line
            type="monotone"
            dataKey="soil_moisture"
            stroke="#15bac6"
            strokeWidth={"3px"}
            dot={false}
            isAnimationActive={false}
          />
          <Line
            type="monotone"
            dataKey="light"
            stroke="#f3ae36"
            strokeWidth={"3px"}
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
