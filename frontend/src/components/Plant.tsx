import "./Plant.css";

interface PlantProps {
  isTalking: boolean;
}

const Plant = ({ isTalking }: PlantProps) => {
  return (
    <div className="notifications-section">
      <span className={isTalking ? "plant jump" : "plant"}>🪴</span>
    </div>
  );
};

export default Plant;
