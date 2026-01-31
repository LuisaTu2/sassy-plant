import { usePlantSettings } from "../contexts/PlantSettingsContext";
import "./Menu.css";

const Menu = () => {
  const { isTalking, isFormOpen, setIsFormOpen } = usePlantSettings();
  return (
    <>
      <button
        className={`menu-button ${isFormOpen ? "open" : ""}`}
        onClick={() => setIsFormOpen(!isFormOpen)}
        disabled={isTalking}
      >
        <span></span>
        <span></span>
        <span></span>
      </button>
    </>
  );
};

export default Menu;
