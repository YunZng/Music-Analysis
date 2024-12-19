import { SVGProps } from "react";

export type IconSvgProps = SVGProps<SVGSVGElement> & {
  size?: number;
};

export interface Track {
  url: string;
  name: string;
  album: string;
  artist: string;
  date: string;
}

export interface Popular {
  url: string;
  name: string;
  artist: string;
  popularity: string;
}

export interface QueryParams {
  order?: "DESC" | "ASC";
  startDate?: string;
  endDate?: string;
  artist?: string;
  trackName?: string;
  popularity?: string;
  danceability?: string;
  energy?: string;
  genres?: string[];
}

export interface Blasting{
  id: string;
  album: string;
  artist: string;
  duration: string;
}