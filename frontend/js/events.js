/* ==========================================================
   GLOBAL M&A TERMINAL
   events.js
   Centralized event management
   ========================================================== */

"use strict";

/* ==========================================================
   GLOBAL NAMESPACE
   ========================================================== */

window.MATerminal = window.MATerminal || {};

/* ==========================================================
   EVENT CONSTANTS
   ========================================================== */

const EVENTS = Object.freeze({

    /* ------------------------------------------------------
       Application
    ------------------------------------------------------ */

    APP_INIT: "app:init",

    APP_READY: "app:ready",

    APP_ERROR: "app:error",

    /* ------------------------------------------------------
       Deals
    ------------------------------------------------------ */

    DEALS_LOADING: "deals:loading",

    DEALS_LOADED: "deals:loaded",

    DEALS_UPDATED: "deals:updated",

    DEAL_SELECTED: "deals:selected",

    /* ------------------------------------------------------
       Filters
    ------------------------------------------------------ */

    FILTER_CHANGED: "filters:changed",

    FILTER_RESET: "filters:reset",

    SEARCH_CHANGED: "search:changed",

    /* ------------------------------------------------------
       Dashboard
    ------------------------------------------------------ */

    STATS_UPDATED: "stats:updated",

    CHARTS_UPDATED: "charts:updated",

    /* ------------------------------------------------------
       Pagination
    ------------------------------------------------------ */

    PAGE_CHANGED: "pagination:changed",

    LOAD_MORE: "pagination:loadMore",

    /* ------------------------------------------------------
       Bookmarks
    ------------------------------------------------------ */

    BOOKMARK_ADDED: "bookmark:added",

    BOOKMARK_REMOVED: "bookmark:removed",

    /* ------------------------------------------------------
       Export
    ------------------------------------------------------ */

    EXPORT_STARTED: "export:started",

    EXPORT_COMPLETED: "export:completed",

    /* ------------------------------------------------------
       UI
    ------------------------------------------------------ */

    SHOW_TOAST: "ui:toast",

    SHOW_MODAL: "ui:modal",

    HIDE_MODAL: "ui:modal:hide"

});

/* ==========================================================
   EVENT BUS
   ========================================================== */

const Events = {

    /**
     * Register an event listener.
     *
     * @param {string} eventName
     * @param {Function} handler
     */
    on(eventName, handler) {

        document.addEventListener(eventName, handler);

    },

    /**
     * Remove an event listener.
     *
     * @param {string} eventName
     * @param {Function} handler
     */
    off(eventName, handler) {

        document.removeEventListener(eventName, handler);

    },

    /**
     * Register an event listener that runs only once.
     *
     * @param {string} eventName
     * @param {Function} handler
     */
    once(eventName, handler) {

        document.addEventListener(eventName, handler, {

            once: true

        });

    },

    /**
     * Emit a custom event.
     *
     * @param {string} eventName
     * @param {*} detail
     */
    emit(eventName, detail = null) {

        document.dispatchEvent(

            new CustomEvent(eventName, {

                detail

            })

        );

    }

};

/* ==========================================================
   EXPORTS
   ========================================================== */

window.MATerminal.events = Events;

window.MATerminal.EVENTS = EVENTS;
