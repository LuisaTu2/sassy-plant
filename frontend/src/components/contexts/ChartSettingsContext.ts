import {
  createContext,
  useContext,
  type Dispatch,
  type SetStateAction,
} from "react";
import { type PlantState } from "../types";

export interface ChartSettings {
  connected: boolean;
  data: PlantState[];
  setConnected: Dispatch<SetStateAction<boolean>>;
  setData: Dispatch<SetStateAction<PlantState[]>>;
}

const noopConnected: Dispatch<SetStateAction<boolean>> = () => {};
const noopData: Dispatch<SetStateAction<PlantState[]>> = () => {};

const defaultSettings = {
  connected: false,
  data: [],
  setConnected: noopConnected,
  setData: noopData,
};
export const ChartSettingsContext =
  createContext<ChartSettings>(defaultSettings);

export const useChartSettings = () => {
  const ctx = useContext(ChartSettingsContext);
  if (!ctx)
    throw new Error(
      "useChartSettings must be used inside a ChartSettingsProvider",
    );
  return ctx;
};
