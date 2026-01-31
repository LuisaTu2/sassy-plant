import { usePlantSettings } from "../contexts/PlantSettingsContext";
import "./Plant.css";

const Plant = () => {
  const { name, isTalking } = usePlantSettings();

  return (
    <div className="plant-section">
      <div className={isTalking ? "plant jump" : "plant"}>🪴</div>
      <div className="plant-greetings">
        {name ? `Hello, I'm ${name}!` : "Hi, there!"}
      </div>
    </div>
  );
};

export default Plant;

// export const useTypewriter = (text: string, speed = 120) => {
//   const [displayed, setDisplayed] = useState("");
//   console.log("OUTSIDE: ", text);

//   useEffect(() => {
//     if (!text) return;

//     const words = text.split(" ");
//     let index = 0;

//     setDisplayed("");
//     console.log("TEXT: ", text);
//     const interval = setInterval(() => {
//       setDisplayed((prev) =>
//         index === 0 ? words[index] : prev + " " + words[index],
//       );
//       index++;

//       if (index >= words.length) {
//         clearInterval(interval);
//       }
//     }, speed);

//     return () => clearInterval(interval);
//   }, [text, speed]);

//   return displayed;
// };
