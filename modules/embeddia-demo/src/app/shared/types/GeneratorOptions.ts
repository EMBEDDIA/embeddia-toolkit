export interface Choice {
  value: string;
  display_name: string;
}

export interface Dataset {
  type: string;
  required: boolean;
  read_only: boolean;
  label: string;
  choices: Choice[];
}

export interface Choice2 {
  value: string;
  display_name: string;
}

export interface Location {
  type: string;
  required: boolean;
  read_only: boolean;
  label: string;
  choices: Choice2[];
}

export interface Choice3 {
  value: string;
  display_name: string;
}

export interface Language {
  type: string;
  required: boolean;
  read_only: boolean;
  label: string;
  choices: Choice3[];
}

export interface POST {
  dataset: Dataset;
  location: Location;
  language: Language;
}

export interface Actions {
  POST: POST;
}

export interface GeneratorOptions {
  name: string;
  description: string;
  renders: string[];
  parses: string[];
  actions: Actions;
}
