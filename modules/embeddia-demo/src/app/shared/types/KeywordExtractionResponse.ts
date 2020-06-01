export interface KeywordExtractionResponse {
  text: string;
  tags: { tag: string; source: string }[];
  entities: { entity: string; type: string; source: string }[];
  language: string;
  analyzers: string[];
}
