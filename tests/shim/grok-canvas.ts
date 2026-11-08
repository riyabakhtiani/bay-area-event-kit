export { useState, useEffect, useRef, useMemo } from "react";
export type { CSSProperties, ChangeEvent, KeyboardEvent } from "react";
export function useGrokTheme(){return {bg:{base:"#fff",subtle:"#f6f6f6",elevated:"#fff"},text:{primary:"#111",secondary:"#555",tertiary:"#888"},border:{default:"#ddd",subtle:"#eee"},dataviz:{categorical:["#36c"]},fill:{accentSubtle:"#eef",hover:"#f0f0f0"},font:{family:"system-ui"}};}
