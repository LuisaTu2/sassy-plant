import { useEffect, useState } from "react";
import { usePlantSettings } from "../contexts/PlantSettingsContext";
import "./Plant.css";

const Plant = () => {
  const {
    isTalking,
    event,
    lightState,
    plantType,
    // waterState,
    // setLightState,
    // setWaterState,
  } = usePlantSettings();

  const [animation, setAnimation] = useState<string>("");

  // const fetchPlantStates = async () => {
  //   try {
  //     const response = await fetch("http://127.0.0.1:9000/get-plant-states/", {
  //       headers: {
  //         "Content-Type": "application/json",
  //       },
  //     });

  //     if (!response.ok) {
  //       throw new Error(`HTTP error! status: ${response.status}`);
  //     }

  //     const [light, water] = await response.json();
  //     setLightState(light);
  //     setWaterState(water);
  //     // TODO: set background
  //   } catch (error) {
  //     console.error("an error occurred:", error);
  //   } finally {
  //     console.log("fetched states");
  //   }
  // };

  useEffect(() => {
    if (event === null) {
      return;
    }

    // console.log("EVENT: ", event);

    // handle light state changes
    // if (event === "good_night") {
    //   setLightState("dark");
    // } else if (event === "good_morning" || event === "take_off_sunglasses") {
    //   setLightState("ambient");
    // } else if (event === "wear_sunglasses") {
    //   setLightState("bright");
    // }

    // handle water state changes
    if (event === "watering") {
      setAnimation("watering");
      setTimeout(() => setAnimation(""), 20000);
    }
    // fetchPlantStates();
  }, [event]);

  return (
    <div className="plant-section">
      <div className={`plant-background ${lightState}`}>
        {lightState === "dark" && <div className="moon"></div>}
        {lightState === "bright" && (
          <div className={`sunglasses ${isTalking ? "jump" : ""}`}></div>
        )}
        {animation === "watering" && <div className="watercan"></div>}
        {plantType === "swiss cheese" ? (
          <div className={`plant plant-monstera ${isTalking ? "jump" : ""}`} />
        ) : (
          <div className={`plant ${isTalking ? "jump" : ""} `}>🪴</div>
        )}
        {/* <div className="plant-state-details">
          <div className="plant-state-detail"> ❤️{lightState}</div>
          <div className="plant-state-detail"> ❤️{waterState}</div>
        </div> */}
      </div>
    </div>
  );
};

export default Plant;
