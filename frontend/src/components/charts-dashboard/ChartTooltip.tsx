import "./ChartTooltip.css";

const ChartTooltip = ({
  active,
  payload,
}: {
  active?: boolean;
  payload?: readonly any[];
}) => {
  if (!active || !payload || payload.length === 0) return null;

  const point = payload[0].payload;

  return (
    <div className="tooltip-wrapper">
      <div>
        <strong>Time:</strong>{" "}
        {/* {new Date(point.timestamp).toLocaleTimeString("en-US", {
          hour12: false,
          fractionalSecondDigits: 1,
        })} */}
        {point.timestamp}
      </div>
      <div>
        <strong>Soil Moisture:</strong> {point.soil_moisture.toFixed(2)}
      </div>
    </div>
  );
};

export default ChartTooltip;
