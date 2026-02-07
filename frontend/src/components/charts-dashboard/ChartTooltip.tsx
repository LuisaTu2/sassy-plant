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
        <strong>time:</strong>{" "}
        {new Date(
          point.timestamp.replace(" ", "T").slice(0, 23),
        ).toLocaleString("en-US", {
          hour12: false,
          year: "numeric",
          month: "2-digit",
          day: "2-digit",
          hour: "2-digit",
          minute: "2-digit",
          second: "2-digit",
        })}
      </div>
      <div>
        <strong>soil moisture: </strong>
        {point.soil_moisture}
      </div>
    </div>
  );
};

export default ChartTooltip;
