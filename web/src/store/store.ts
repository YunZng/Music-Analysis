import { Blasting, Popular } from "@/types";
import { atom } from "nanostores";

export const $queryResult = atom<any>([]);
export function setQueryResult(queryResult: any) {
  $queryResult.set(queryResult);
}

export const $mostPopular = atom<Popular[]>([]);
export function setMostPopular(tracks: Popular[]) {
  $mostPopular.set(tracks);
}

export const $nonstopBlashing = atom<Blasting[]>([]);
export function setNonstopBlashing(tracks: Blasting[]) {
  $nonstopBlashing.set(tracks);
}

export const $analysis = atom<string>("");
export function setAnalysis(analysis: string) {
  $analysis.set(analysis);
}
