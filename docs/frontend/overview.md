# Part Management System - Source Code Overview

## Overview

This document provides a comprehensive overview of the `src/` directory structure and organization for the Part Management System. This is a web-based application built with modern JavaScript, designed to manage engineering parts through their lifecycle from design review to completion.

## Directory Structure

```
src/
├── main.js                 # Application entry point and initialization
├── style.css              # Global styles and Tailwind configuration
├── components/            # Reusable UI components
│   └── threeDViewer.js    # 3D model visualization component (future)
├── html/                  # HTML templates for UI sections
│   ├── header.html        # Application header
│   ├── tabs.html          # Navigation tabs
│   ├── *-content.html     # Content templates for each tab
│   └── *-modal.html       # Modal dialog templates
├── modules/               # Core application logic (modular architecture)
│   ├── auth.js            # Authentication management
│   ├── state.js           # Central state management
│   ├── tabs.js            # Tab navigation and switching
│   ├── partActions.js     # Part manipulation operations
│   ├── formHandler.js     # Form submission handling
│   ├── modals.js          # Modal management
│   ├── review.js          # Review tab logic
│   ├── cnc.js             # CNC machining tab logic (includes STEP download)
│   ├── handFab.js         # Hand fabrication tab logic
│   └── completed.js       # Completed parts tab logic
├── utils/                 # Utility functions
│   └── partsApi.js        # API communication utilities
└── components/            # Specialized components
    └── threeDViewer.js    # 3D model visualization (future implementation)
```

## Architecture Overview

The application follows a **modular architecture** with clear separation of concerns:

- **Entry Point**: `main.js` initializes the application and sets up global event handlers
- **State Management**: Centralized in `state.js` with typed data structures
- **UI Components**: HTML templates in `html/` rendered dynamically by modules
- **Business Logic**: Organized by feature in `modules/` directory
- **Utilities**: Shared helper functions in `utils/` directory
- **Components**: Specialized UI components like 3D viewers

## Key Features

- **Authentication System**: API key-based authentication with modal login
- **Multi-tab Interface**: Review, CNC, Hand Fabrication, and Completed parts
- **Part Lifecycle Management**: From design review through completion
- **File Management**: STEP file upload and download capabilities
- **Search and Filtering**: Global search across all parts
- **3D Visualization**: Planned Three.js components for model viewing
- **Responsive Design**: Modern neumorphic UI with Tailwind CSS
- **Modal Management**: Dynamic forms and confirmation dialogs

## Technology Stack

- **Frontend**: Vanilla JavaScript (ES6+ modules)
- **Styling**: Tailwind CSS with custom neumorphic design system
- **API Communication**: Fetch API with custom utilities
- **Authentication**: Modal-based API key management
- **File Handling**: Browser File API for uploads and downloads
- **3D Graphics**: Three.js (planned for future implementation)
- **Icons**: Font Awesome
- **Build Tool**: Vite

## Development Notes

- Uses ES6 modules for clean imports/exports
- Follows Google-style docstrings for documentation
- Implements TypeScript-style JSDoc type annotations
- Modular design enables easy testing and maintenance
- Authentication system integrated throughout the application
- API communication abstracted into reusable utilities
- No external state management libraries (vanilla JS approach)

## Related Documentation

- [Architecture Details](architecture.md) - Deep dive into system architecture
- [Modules Overview](modules.md) - Detailed breakdown of each module
- [UI Components](ui-components.md) - HTML templates and interface components
- [State Management](state-management.md) - How application state is handled
- [Utilities](utilities.md) - Helper functions and utilities

## Getting Started

The application initializes through `main.js`, which:
1. Sets up Tailwind configuration
2. Imports all necessary modules
3. Initializes application state with mock data
4. Sets up global event handlers for UI interactions

See individual module documentation for implementation details.
