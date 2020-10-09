import {Recommendations} from './Recommendations';

export interface MovieDetails {
  movieID: number;
  title: string;
  year: number;
  rating: number;
  description: string;
  genre: string[];
  director: string[];
  cast: string[];
  recommendations: Recommendations[];
  reviews: any[];
}
