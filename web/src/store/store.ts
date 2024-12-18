import { Track } from '@/types'
import { atom } from 'nanostores'

export const $tracks = atom<Track[]>([])

export function setTracks(tracks: Track[]) {
  $tracks.set(tracks);
}