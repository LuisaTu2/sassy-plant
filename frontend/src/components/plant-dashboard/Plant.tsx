import "./Plant.css";

interface PlantProps {
  isTalking: boolean;
}

const Plant = ({ isTalking }: PlantProps) => {
  return (
    <div className="plant-section">
      <div className={isTalking ? "plant jump" : "plant"}>🪴</div>
      <div className="plant-greetings">Hello!</div>
    </div>
  );
};

export default Plant;
