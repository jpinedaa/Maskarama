export interface Entity {
  id: string;
  state: string;
  inputs: string[];
  currentOutput: string;
  perception?: string;
}

export interface Environment {
  id: string;
  boundaries?: {
    ConnectedEnvironmentID: string;
    TransitionCondition: string;
  }[];
  state?: {
    OverallState: string;
    EntitySpecificStates?: Record<string, string>;
  };
  entities: Record<string, Entity>;
  exitEntities?: Record<string, string>;
  narrative?: string;
}

export interface SimulationState {
  environments: Record<string, Environment>;
  perspective: string;
  currentEnvironment: string;
}
