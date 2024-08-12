/* eslint-disable @typescript-eslint/no-unsafe-call */

import { atomWithStorage } from "jotai/utils";

export const isDyslexic = atomWithStorage<boolean>("dyslexic", true);
