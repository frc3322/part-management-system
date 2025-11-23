// Tab Management Module
// Handles tab switching and navigation

import { appState, loadAllParts, loadPartsForCategory } from "./state.js";

/**
 * Switch to a specific tab
 * @param {string} tab - The tab to switch to
 */
export async function switchTab(tab) {
    appState.currentTab = tab;

    // Reset UI
    for (const t of ["review", "cnc", "hand", "completed"]) {
        const btn = document.getElementById(`tab-${t}`);
        const content = document.getElementById(`content-${t}`);

        if (t === tab) {
            btn.classList.add("active-tab", "text-blue-400");
            btn.classList.remove("text-gray-400");
            content.classList.remove("hidden");
            if (t === "cnc") content.classList.add("grid");
            else content.classList.remove("grid"); // ensuring grid is only on CNC
        } else {
            btn.classList.remove("active-tab", "text-blue-400");
            btn.classList.add("text-gray-400");
            content.classList.add("hidden");
            content.classList.remove("grid");
        }
    }

    // Fetch fresh data from server
    try {
        if (tab === "review") {
            // Load all parts for review tab to ensure proper categorization
            await loadAllParts();
        } else {
            // Load fresh data for specific category
            await loadPartsForCategory(tab);
        }
    } catch (error) {
        console.error(`Failed to load ${tab} data:`, error);
        // Still render with current data if fetch fails
    }
}

/**
 * Handle search functionality
 * @param {string} query - The search query
 */
export function handleSearch(query) {
    appState.searchQuery = query;
    // Re-render current tab
    const currentTab = getCurrentTab();
    if (currentTab === "review") renderReview();
    else if (currentTab === "cnc") renderCNC();
    else if (currentTab === "hand") renderHandFab();
    else if (currentTab === "completed") renderCompleted();
}

/**
 * Get the current active tab
 * @returns {string} The current tab name
 */
export function getCurrentTab() {
    return appState.currentTab;
}

/**
 * Sort hand fabrication table by a specific key
 * @param {string} key - The key to sort by
 */
export function sortTable(key) {
    appState.sortDirection = appState.sortDirection === 1 ? -1 : 1;

    appState.parts.hand.sort((a, b) => {
        let valA = a[key] || "";
        let valB = b[key] || "";
        valA = valA.toString().toLowerCase();
        valB = valB.toString().toLowerCase();
        if (valA < valB) return -1 * appState.sortDirection;
        if (valA > valB) return 1 * appState.sortDirection;
        return 0;
    });

    renderHandFab();
}
