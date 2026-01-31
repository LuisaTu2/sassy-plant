import { type ReactNode, useState } from "react";
import { type PlantState } from "../types";
import { ChartSettingsContext } from "./ChartSettingsContext";

export const ChartSettingsProvider = ({
  children,
}: {
  children: ReactNode;
}) => {
  const [connected, setConnected] = useState<boolean>(false);
  const [data, setData] = useState<PlantState[]>([]);

  return (
    <ChartSettingsContext.Provider
      value={{
        connected,
        data,
        setConnected,
        setData,
      }}
    >
      {children}
    </ChartSettingsContext.Provider>
  );
};
