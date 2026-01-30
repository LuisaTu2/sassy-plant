import "./Menu.css";

interface MenuProps {
  showSettings: boolean;
  setShowSettings: React.Dispatch<React.SetStateAction<boolean>>;
}

const Menu = ({ showSettings, setShowSettings }: MenuProps) => {
  return (
    <>
      <button
        className={`menu-button ${showSettings ? "open" : ""}`}
        onClick={() => setShowSettings(!showSettings)}
      >
        <span></span>
        <span></span>
        <span></span>
      </button>
    </>
  );
};

export default Menu;
