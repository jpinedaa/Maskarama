import { atom } from "jotai";
// import { SimulationState, Environment, Entity } from "~/types/gameModel";
export interface Entity {
  id: string;
  state: string;
  inputs: string[];
  currentOutput: string;
  perception?: string;
}

export interface Environment {
  id: string;
  boundaries: {
    ConnectedEnvironmentID: string;
    TransitionCondition: string;
  }[];
  state: {
    OverallState: string;
    EntitySpecificStates: Record<string, string>;
  };
  entities: Record<string, Entity>;
  exitEntities: Record<string, string>;
  narrative: string;
}

export interface GameState {
  environments: Record<string, Environment>;
  perspective: string;
  currentEnvironment: string;
}

export const simulationStartedAtom = atom<boolean>(false);
export const currentEnvironmentAtom = atom<string | null>(null);
export const perspectiveAtom = atom<string | null>(null);
export const environmentsAtom = atom<Record<string, Environment>>({});
export const entitiesAtom = atom<Record<string, Entity>>({});
export const currentPhaseAtom = atom<number>(0);
export const turnCountAtom = atom<number>(0);

export enum characterEntity {
  zeus = "zeus01",
  hermes = "hermes01",
  artemis = "artemis01",
  poseidon = "poseidon01",
  apollo = "apollo01",
  athena = "athena01",
}

export enum itemEntity {
  throneZeus = "throneOfZeus01",
  judmentTable = "judmentTable01",
  table = "table01",
  statue = "statue01",
}

export enum roomEntity {
  "palaceCourt01",
  "throneRoom01",
  "hallsOfJudgment01",
}

export interface Character {
  name: string;
  id: string;
  portrait: string;
}
export const characters: Character[] = [
  {
    name: "Zeus",
    id: "zeus01",
    portrait: "/mp4/characters/zeus.mp4",
  },
  {
    name: "Poseidon",
    id: "poseidon01",
    portrait: "/mp4/characters/poseidon.mp4",
  },
  // { name: "Hera", id: "hera01", portrait: "/mp4/characters/hera.mp4" },
  {
    name: "Demeter",
    id: "demeter01",
    portrait: "/mp4/characters/demeter.mp4",
  },
  {
    name: "Hephaestus",
    id: "hephaestus01",
    portrait: "/mp4/characters/hephaestus.mp4",
  },
  {
    name: "Athena",
    id: "athena01",
    portrait: "/mp4/characters/athena.mp4",
  },
  {
    name: "Hermes",
    id: "hermes01",
    portrait: "/mp4/characters/hermes.mp4",
  },
  {
    name: "Aphrodite",
    id: "aphrodite01",
    portrait: "/mp4/characters/aphrodite.mp4",
  },
  {
    name: "Ares",
    id: "ares01",
    portrait: "/mp4/characters/ares.mp4",
  },
  {
    name: "Hestia",
    id: "hestia01",
    portrait: "/mp4/characters/hestia.mp4",
  },
  {
    name: "Artemis",
    id: "artemis01",
    portrait: "/mp4/characters/artemis.mp4",
  },
  // {
  //   name: "apollo01",
  //   id: "apollo01",
  //   portrait: "/mp4/characters/apollo.mp4",
  // },
];

export interface Item {
  id: string;
  isItem: boolean;
  description: string;
}

export const items: Item[] = [
  {
    id: "Throne of Zeus",
    description: "The throne of Zeus",
    isItem: true,
  },
];
export interface Room {
  id: string;
  name: string;
  roomImage: string;
}
export const rooms: Room[] = [
  {
    id: "throneRoom01",
    name: "Throne Room",
    roomImage: "/webp/rooms/throneRoom01.webp",
  },
  {
    id: "libraryAthena01",
    name: "Library of Athena",
    roomImage: "/webp/rooms/libraryAthena01.webp",
  },
  {
    id: "bathhouseAphrodite01",
    name: "Bath House ofAphrodite",
    roomImage: "/webp/rooms/bathHouseAphrodite01.webp",
  },
  {
    id: "hearthHestia01",
    name: "Hearth of Hestia",
    roomImage: "/webp/rooms/hestiasHearth01.webp",
  },
  {
    id: "forgeOfHephaestus01",
    name: "Forge of Hephaestus",
    roomImage: "/webp/rooms/forgeHephaestus01.webp",
  },
  {
    id: "gardensDemeter01",
    name: "Gardens of Demeter",
    roomImage: "/webp/rooms/gardensDemeter01.webp",
  },

  {
    id: "huntinggroundsArtemis01",
    name: "Hunting Grounds of Artemis",
    roomImage: "/webp/rooms/huntingGroundsArtemis01.webp",
  },
  {
    id: "armoryAres01",
    name: "Armory of Ares",
    roomImage: "/webp/rooms/armoryAres01.webp",
  },
  {
    id: "hermesQuarters01",
    name: "Hermes' Quarters",
    roomImage: "/webp/rooms/hermesQuarters01.webp",
  },
];

export const charactersAtom = atom<characterEntity[]>([]);
export const currentCharacterAtom = atom<Character>();
export const currentCharsInRoomAtom = atom<Character[]>([]);
export const roomsAtom = atom<roomEntity[]>([]);
export const currentRoomAtom = atom<Room>();

export const itemsAtom = atom<Item[]>([]);

export const gameStartedAtom = atom<boolean>(false);
