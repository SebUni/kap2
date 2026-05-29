import type { LayersList } from '@deck.gl/core';
import type { Map } from "./types.js";
/** Group Deck layers into buckets (by beforeId or slot) and insert them
 *  into the mapbox Map according to the user-defined order
 **/
export declare function resolveLayerGroups(map?: Map, oldLayers?: LayersList, newLayers?: LayersList): void;
//# sourceMappingURL=resolve-layer-groups.d.ts.map