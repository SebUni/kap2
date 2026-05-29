// deck.gl
// SPDX-License-Identifier: MIT
// Copyright (c) vis.gl contributors
import { clamp } from '@math.gl/core';
import Controller from "./controller.js";
import { MapState } from "./map-controller.js";
import { mod } from "../utils/math-utils.js";
import LinearInterpolator from "../transitions/linear-interpolator.js";
import { zoomAdjust } from "../viewports/globe-viewport.js";
import { MAX_LATITUDE } from '@math.gl/web-mercator';
class GlobeState extends MapState {
    constructor(options) {
        const { startPanPos, ...mapStateOptions } = options;
        super(mapStateOptions);
        if (startPanPos !== undefined) {
            this._state.startPanPos = startPanPos;
        }
    }
    panStart({ pos }) {
        const { latitude, longitude, zoom } = this.getViewportProps();
        return this._getUpdatedState({
            startPanLngLat: [longitude, latitude],
            startPanPos: pos,
            startZoom: zoom
        });
    }
    pan({ pos, startPos }) {
        const state = this.getState();
        const startPanLngLat = state.startPanLngLat || this._unproject(startPos);
        if (!startPanLngLat)
            return this;
        const startZoom = state.startZoom ?? this.getViewportProps().zoom;
        const startPanPos = state.startPanPos || startPos;
        const coords = [startPanLngLat[0], startPanLngLat[1], startZoom];
        const viewport = this.makeViewport(this.getViewportProps());
        const newProps = viewport.panByPosition(coords, pos, startPanPos);
        return this._getUpdatedState(newProps);
    }
    panEnd() {
        return this._getUpdatedState({
            startPanLngLat: null,
            startPanPos: null,
            startZoom: null
        });
    }
    zoom({ scale }) {
        // In Globe view zoom does not take into account the mouse position
        const startZoom = this.getState().startZoom || this.getViewportProps().zoom;
        const zoom = startZoom + Math.log2(scale);
        return this._getUpdatedState({ zoom });
    }
    applyConstraints(props) {
        // Ensure zoom is within specified range
        const { longitude, latitude, maxZoom, minZoom, zoom } = props;
        const ZOOM0 = zoomAdjust(0);
        const zoomAdjustment = zoomAdjust(latitude) - ZOOM0;
        props.zoom = clamp(zoom, minZoom + zoomAdjustment, maxZoom + zoomAdjustment);
        if (longitude < -180 || longitude > 180) {
            props.longitude = mod(longitude + 180, 360) - 180;
        }
        props.latitude = clamp(latitude, -MAX_LATITUDE, MAX_LATITUDE);
        return props;
    }
}
export default class GlobeController extends Controller {
    constructor() {
        super(...arguments);
        this.ControllerState = GlobeState;
        this.transition = {
            transitionDuration: 300,
            transitionInterpolator: new LinearInterpolator(['longitude', 'latitude', 'zoom'])
        };
        this.dragMode = 'pan';
    }
    setProps(props) {
        super.setProps(props);
        // TODO - support pitching?
        this.dragRotate = false;
        this.touchRotate = false;
    }
}
//# sourceMappingURL=globe-controller.js.map