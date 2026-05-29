import type { Map, CustomLayerInterface } from "./types.js";
import type { Deck, Layer } from '@deck.gl/core';
type MapWithDeck = Map & {
    __deck: Deck;
};
export type MapboxLayerProps<LayerT extends Layer> = Partial<LayerT['props']> & {
    id: string;
    renderingMode?: '2d' | '3d';
    slot?: 'bottom' | 'middle' | 'top';
};
export default class MapboxLayer<LayerT extends Layer> implements CustomLayerInterface {
    id: string;
    type: 'custom';
    renderingMode: '2d' | '3d';
    slot?: 'bottom' | 'middle' | 'top';
    map: MapWithDeck | null;
    props: MapboxLayerProps<LayerT>;
    constructor(props: MapboxLayerProps<LayerT>);
    onAdd(map: MapWithDeck, gl: WebGL2RenderingContext): void;
    onRemove(): void;
    setProps(props: MapboxLayerProps<LayerT>): void;
    render(gl: any, renderParameters: any): void;
}
export {};
//# sourceMappingURL=mapbox-layer.d.ts.map