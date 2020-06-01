export interface Text {
  type: string;
  required: boolean;
  read_only: boolean;
  label: string;
}

export interface Choice {
  value: string;
  display_name: string;
}

export interface Analyzers {
  type: string;
  required: boolean;
  read_only: boolean;
  label: string;
  choices: Choice[];
}

export interface POST {
  text: Text;
  analyzers: Analyzers;
}

export interface Actions {
  POST: POST;
}

export interface AnalyzersOptions {
  name: string;
  description: string;
  renders: string[];
  parses: string[];
  actions: Actions;
}
