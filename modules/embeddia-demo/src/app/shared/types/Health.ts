export interface Disk {
  free: number;
  total: number;
  used: number;
  unit: string;
}

export interface Memory {
  free: number;
  total: number;
  used: number;
  unit: string;
}

export interface Cpu {
  percent: number;
}

export interface Services {
  [key: string]: boolean;
}

export interface Health {
  service: string;
  disk: Disk;
  memory: Memory;
  cpu: Cpu;
  services: Services;
}


