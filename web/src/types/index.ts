import { SVGProps } from "react";

export type IconSvgProps = SVGProps<SVGSVGElement> & {
  size?: number;
};

export type Track = {
  url: string;
  name: string;
  album: string;
  artist: string;
  date: string;
};