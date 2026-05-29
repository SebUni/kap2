// deck.gl
// SPDX-License-Identifier: MIT
// Copyright (c) vis.gl contributors
import { drawLayer } from "./deck-utils.js";
export default class MapboxLayer {
    /* eslint-disable no-this-before-super */
    constructor(props) {
        if (!props.id) {
            throw new Error('Layer must have an unique id');
        }
        this.id = props.id;
        this.type = 'custom';
        this.renderingMode = props.renderingMode || '3d';
        this.slot = props.slot;
        this.map = null;
        this.props = props;
    }
    /* Mapbox custom layer methods */
    onAdd(map, gl) {
        this.map = map;
    }
    onRemove() {
        this.map = null;
    }
    setProps(props) {
        // id cannot be changed
        Object.assign(this.props, props, { id: this.id });
    }
    render(gl, renderParameters) {
        if (!this.map)
            return;
        drawLayer(this.map.__deck, this.map, this, renderParameters);
    }
}
//# sourceMappingURL=mapbox-layer.js.map