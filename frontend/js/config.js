/* ==========================================================
   GLOBAL M&A TERMINAL
   config.js
   Global configuration & application constants
   ========================================================== */

"use strict";

/* ==========================================================
   GLOBAL NAMESPACE
   ========================================================== */

window.MATerminal = window.MATerminal || {};

/* ==========================================================
   APPLICATION CONFIGURATION
   ========================================================== */

const CONFIG = Object.freeze({

    APP_NAME: "Global M&A Terminal",

    VERSION: "1.0.0",

    ENVIRONMENT: "production",

    /* ------------------------------------------------------ */
    /* Supabase                                                */
    /* ------------------------------------------------------ */

    SUPABASE: Object.freeze({

        URL: "https://YOUR_PROJECT.supabase.co",

        ANON_KEY: "YOUR_SUPABASE_ANON_KEY",

        TABLE_NAME: "ma_news"

    }),

    /* ------------------------------------------------------ */
    /* Pagination                                              */
    /* ------------------------------------------------------ */

    PAGINATION: Object.freeze({

        PAGE_SIZE: 20,

        MAX_PAGE_SIZE: 100

    }),

    /* ------------------------------------------------------ */
    /* Dashboard                                               */
    /* ------------------------------------------------------ */

    DASHBOARD: Object.freeze({

        MAX_TRENDING_COMPANIES: 10,

        MAX_TOP_ACQUIRERS: 10,

        MAX_TOP_TARGETS: 10,

        MAX_MEGA_DEALS: 10,

        MAX_NEWS_SOURCES: 8,

        MAX_CHART_ITEMS: 10

    }),

    /* ------------------------------------------------------ */
    /* Auto Refresh                                            */
    /* ------------------------------------------------------ */

    REFRESH: Object.freeze({

        ENABLED: true,

        INTERVAL_MS: 5 * 60 * 1000

    }),

    /* ------------------------------------------------------ */
    /* Date Formatting                                         */
    /* ------------------------------------------------------ */

    DATE: Object.freeze({

        LOCALE: "en-US",

        TIME_ZONE: "UTC"

    }),

    /* ------------------------------------------------------ */
    /* Local Storage                                           */
    /* ------------------------------------------------------ */

    STORAGE: Object.freeze({

        BOOKMARKS: "ma_terminal_bookmarks",

        FILTERS: "ma_terminal_filters",

        THEME: "ma_terminal_theme"

    }),

    /* ------------------------------------------------------ */
    /* Export                                                  */
    /* ------------------------------------------------------ */

    EXPORT: Object.freeze({

        FILE_PREFIX: "Global_MA_Deals"

    }),

    /* ------------------------------------------------------ */
    /* UI                                                      */
    /* ------------------------------------------------------ */

    UI: Object.freeze({

        TOAST_DURATION: 3000,

        ANIMATION_DURATION: 200

    })

});

/* ==========================================================
   APPLICATION CONSTANTS
   ========================================================== */

const CONSTANTS = Object.freeze({

    DEAL_TYPES: Object.freeze([

        "Acquisition",
        "Merger",
        "Investment",
        "Private Equity",
        "Joint Venture",
        "Asset Purchase",
        "Minority Stake",
        "Strategic Partnership"

    ]),

    REGIONS: Object.freeze([

        "North America",
        "Europe",
        "Asia",
        "Middle East",
        "Africa",
        "South America",
        "Oceania"

    ]),

    SORT_OPTIONS: Object.freeze({

        LATEST: "latest",
        OLDEST: "oldest",
        LARGEST: "largest",
        SMALLEST: "smallest"

    }),

    DOM_IDS: Object.freeze({

        GLOBAL_SEARCH: "globalSearch",

        DEAL_GRID: "dealGrid",

        DEAL_MODAL: "dealModal",

        TOAST: "toast",

        INDUSTRY_FILTER: "industryFilter",

        REGION_FILTER: "regionFilter",

        DEAL_TYPE_FILTER: "dealTypeFilter",

        SOURCE_FILTER: "sourceFilter",

        LOAD_MORE_BUTTON: "loadMoreDeals"

    })

});

/* ==========================================================
   SUPABASE CLIENT
   ========================================================== */

const supabase = window.supabase.createClient(

    CONFIG.SUPABASE.URL,

    CONFIG.SUPABASE.ANON_KEY

);

/* ==========================================================
   EXPORTS
   ========================================================== */

window.MATerminal.config = CONFIG;

window.MATerminal.constants = CONSTANTS;

window.MATerminal.supabase = supabase;
