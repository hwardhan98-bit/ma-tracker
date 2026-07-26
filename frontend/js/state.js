/* ==========================================================
   GLOBAL M&A TERMINAL
   state.js
   Centralized application state management
   ========================================================== */

"use strict";

/* ==========================================================
   GLOBAL NAMESPACE
   ========================================================== */

window.MATerminal = window.MATerminal || {};

/* ==========================================================
   PRIVATE STATE
   ========================================================== */

const DEFAULT_FILTERS = Object.freeze({

    keyword: "",

    industry: "",

    region: "",

    dealType: "",

    source: "",

    startDate: "",

    endDate: "",

    minDealValue: null,

    maxDealValue: null,

    sortBy: "latest"

});

const DEFAULT_STATS = Object.freeze({

    totalDeals: 0,

    dealsToday: 0,

    dealsThisWeek: 0,

    dealsThisMonth: 0,

    totalDealValue: 0,

    averageDealValue: 0,

    largestDeal: null,

    topIndustry: null,

    topRegion: null

});

const DEFAULT_PAGINATION = Object.freeze({

    page: 1,

    pageSize: window.MATerminal.config.PAGINATION.PAGE_SIZE,

    totalPages: 1,

    totalRecords: 0,

    hasMore: false

});

const DEFAULT_CHARTS = Object.freeze({

    industry: null,

    region: null,

    trend: null,

    dealValue: null,

    dealType: null

});

const state = {

    /* ------------------------------------------------------
       Deal Data
    ------------------------------------------------------ */

    deals: [],

    filteredDeals: [],

    /* ------------------------------------------------------
       Dashboard
    ------------------------------------------------------ */

    stats: structuredClone(DEFAULT_STATS),

    /* ------------------------------------------------------
       Filters
    ------------------------------------------------------ */

    filters: structuredClone(DEFAULT_FILTERS),

    /* ------------------------------------------------------
       Charts
    ------------------------------------------------------ */

    charts: structuredClone(DEFAULT_CHARTS),

    /* ------------------------------------------------------
       Pagination
    ------------------------------------------------------ */

    pagination: structuredClone(DEFAULT_PAGINATION),

    /* ------------------------------------------------------
       User Data
    ------------------------------------------------------ */

    bookmarks: [],

    selectedDeal: null,

    /* ------------------------------------------------------
       Application Status
    ------------------------------------------------------ */

    loading: false,

    initialized: false,

    lastRefresh: null

};

/* ==========================================================
   STATE MANAGER
   ========================================================== */

const State = {

    /* ======================================================
       GETTERS
    ====================================================== */

    getState() {

        return state;

    },

    getDeals() {

        return [...state.deals];

    },

    getFilteredDeals() {

        return [...state.filteredDeals];

    },

    getFilters() {

        return { ...state.filters };

    },

    getStats() {

        return { ...state.stats };

    },

    getPagination() {

        return { ...state.pagination };

    },

    getBookmarks() {

        return [...state.bookmarks];

    },

    getSelectedDeal() {

        return state.selectedDeal;

    },

    getChart(name) {

        return state.charts[name] || null;

    },

    isLoading() {

        return state.loading;

    },

    isInitialized() {

        return state.initialized;

    },

    getLastRefresh() {

        return state.lastRefresh;

    },

    /* ======================================================
       SETTERS
    ====================================================== */

    setDeals(deals = []) {

        state.deals = [...deals];

    },

    setFilteredDeals(deals = []) {

        state.filteredDeals = [...deals];

    },

    setFilters(filters = {}) {

        state.filters = {

            ...state.filters,

            ...filters

        };

    },

    resetFilters() {

        state.filters = structuredClone(DEFAULT_FILTERS);

    },

    setStats(stats = {}) {

        state.stats = {

            ...state.stats,

            ...stats

        };

    },

    setPagination(values = {}) {

        state.pagination = {

            ...state.pagination,

            ...values

        };

    },

    resetPagination() {

        state.pagination = structuredClone(DEFAULT_PAGINATION);

    },

    setBookmarks(bookmarks = []) {

        state.bookmarks = [...bookmarks];

    },

    setSelectedDeal(deal = null) {

        state.selectedDeal = deal;

    },

    setChart(name, chart) {

        state.charts[name] = chart;

    },

    setLoading(value) {

        state.loading = Boolean(value);

    },

    setInitialized(value) {

        state.initialized = Boolean(value);

    },

    updateLastRefresh() {

        state.lastRefresh = new Date();

    },

    /* ======================================================
       CHART MANAGEMENT
    ====================================================== */

    destroyCharts() {

        Object.values(state.charts).forEach(chart => {

            if (chart && typeof chart.destroy === "function") {

                chart.destroy();

            }

        });

        state.charts = structuredClone(DEFAULT_CHARTS);

    },

    /* ======================================================
       APPLICATION RESET
    ====================================================== */

    reset() {

        state.deals = [];

        state.filteredDeals = [];

        state.filters = structuredClone(DEFAULT_FILTERS);

        state.stats = structuredClone(DEFAULT_STATS);

        state.pagination = structuredClone(DEFAULT_PAGINATION);

        state.bookmarks = [];

        state.selectedDeal = null;

        state.loading = false;

        state.initialized = false;

        state.lastRefresh = null;

        this.destroyCharts();

    }

};

/* ==========================================================
   EXPORT
   ========================================================== */

window.MATerminal.state = State;
