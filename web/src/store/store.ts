import { Blasting, Popular, Track } from '@/types'
import { atom } from 'nanostores'

export const $tracks = atom<Track[]>([])
export function setTracks(tracks: Track[]) {
  $tracks.set(tracks);
}

export const $mostPopular = atom<Popular[]>([])
export function setMostPopular(tracks: Popular[]) {
  $mostPopular.set(tracks);
}

export const $nonstopBlashing =  atom<Blasting[]>([])
export function setNonstopBlashing(tracks: Blasting[]) {
  $nonstopBlashing.set(tracks);
}