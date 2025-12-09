// Tab Management Module
// Handles tab switching and navigation

import { appState, loadAllParts, loadPartsForCategory } from "./state.js";
import { renderReview } from "./review.js";
import { renderCNC } from "./cnc.js";
import { renderHandFab } from "./handFab.js";
import { renderCompleted } from "./completed.js";
import { saveCurrentTab } from "./persistence.js";

// Debounce timer for search
let searchDebounceTimer = null;

/**
 * Switch to a specific tab
 * @param {string} tab - The tab to switch to
 */
export async function switchTab(tab) {
  appState.currentTab = tab;

  // Save current tab to localStorage
  saveCurrentTab(tab);

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
 * Handle search functionality with debouncing
 * @param {string} query - The search query
 */
export function handleSearch(query) {
  appState.searchQuery = query;

  // Clear existing timer
  if (searchDebounceTimer) {
    clearTimeout(searchDebounceTimer);
  }

  // Set new timer to debounce search
  searchDebounceTimer = setTimeout(async () => {
    // Re-render current tab after debounce delay
    const currentTab = getCurrentTab();

    if (currentTab === "review") {
      renderReview();
    } else if (currentTab === "cnc") {
      renderCNC();
    } else if (currentTab === "hand") {
      renderHandFab();
    } else if (currentTab === "completed") {
      renderCompleted();
    }

    searchDebounceTimer = null;
  }, 300); // 300ms debounce delay
}

/**
 * Get the current active tab
 * @returns {string} The current tab name
 */
export function getCurrentTab() {
  return appState.currentTab;
}

function getSortValue(part, key) {
  if (key === "partId") return part.partId || part.id || part.name || "";
  if (key === "name") return part.name || part.partId || part.id || "";
  if (key === "assigned") return part.assigned || "";
  if (key === "status") return part.status || "";
  if (key === "subsystem") return part.subsystem || "";
  if (key === "material") return part.material || "";
  if (key === "type") return part.type || "";
  if (key === "file") return part.file || "";
  if (key === "notes") return part.notes || "";
  if (key === "amount") {
    const amount = Number(part.amount);
    return Number.isFinite(amount) ? amount : 0;
  }
  return part[key] || "";
}

function updateSortState(category, key) {
  const current = appState.sortState?.[category] || { key: null, direction: 1 };
  const direction = current.key === key ? current.direction * -1 : 1;
  appState.sortState[category] = { key, direction };
  appState.sortDirection = direction;
  return direction;
}

function updateSortIndicators(category, activeKey, direction) {
  const indicators = document.querySelectorAll(
    `[data-sort-category="${category}"] .sort-icon`
  );
  indicators.forEach((icon) => {
    const iconKey = icon.dataset.sortKey;
    icon.classList.remove("fa-sort-up", "fa-sort-down", "text-blue-300");
    icon.classList.add("fa-sort");
    if (iconKey === activeKey) {
      icon.classList.remove("fa-sort");
      icon.classList.add(direction === 1 ? "fa-sort-up" : "fa-sort-down");
      icon.classList.add("text-blue-300");
    }
  });
}

function sortParts(category, key, direction) {
  const parts = appState.parts[category] || [];
  parts.sort((a, b) => {
    const valA = getSortValue(a, key);
    const valB = getSortValue(b, key);
    if (typeof valA === "number" && typeof valB === "number") {
      return (valA - valB) * direction;
    }
    const normalizedA = valA.toString().toLowerCase();
    const normalizedB = valB.toString().toLowerCase();
    if (normalizedA < normalizedB) return -1 * direction;
    if (normalizedA > normalizedB) return 1 * direction;
    return 0;
  });
}

function renderSortedCategory(category) {
  if (category === "hand") {
    renderHandFab();
  } else if (category === "review") {
    renderReview();
  } else if (category === "completed") {
    renderCompleted();
  }
}

/**
 * Sort a table by category and key
 * @param {string} category - The tab category
 * @param {string} key - The key to sort by
 */
export async function sortTable(category, key) {
  const direction = updateSortState(category, key);
  sortParts(category, key, direction);
  updateSortIndicators(category, key, direction);
  renderSortedCategory(category);
}
