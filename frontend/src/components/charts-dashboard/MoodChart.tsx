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
import "./MoodChart.css";

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

const moodEmojiMap: Record<number, string> = {
  0.2: "😢",
  0.4: "😐",
  0.6: "🙂",
  0.8: "😄",
  1: "🤩",
};
// Custom Y-axis tick renderer
const EmojiYAxisTick: React.FC<any> = ({ x, y, payload }) => {
  const emoji = moodEmojiMap[payload.value] ?? payload.value;
  return (
    <text x={x} y={y} textAnchor="end" dominantBaseline="middle" fontSize={16}>
      {emoji}
    </text>
  );
};

// Dashboard component as a constant arrow function
const MoodChart = ({ data }: StatePlotProps) => {
  return (
    <div className="mood-chart-wrapper">
      <div className="mood-chart-title">MOOD CHART</div>

      <ResponsiveContainer width="90%" height={400} className={"mood-chart"}>
        <LineChart data={data}>
          <XAxis dataKey="timestamp" tickFormatter={formatTime} />
          <YAxis
            type="number"
            domain={[0, 1]}
            ticks={[0.2, 0.4, 0.6, 0.8, 1]} // force all ticks to render
            tick={<EmojiYAxisTick />}
          />
          <Line
            type="monotone"
            dataKey="mood"
            stroke="#9d23c6"
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

export default MoodChart;
